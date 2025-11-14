from django.utils import timezone
from .models import verPost, serialNumber
from django.shortcuts import render, get_object_or_404, redirect
from .forms import verPostForm, zipUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import FileResponse, Http404
from .forms import SignUpForm, serialNumberForm, ContactForm
from django.urls import reverse
from django.core.mail import send_mail
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.http import HttpResponseForbidden, HttpResponseServerError, HttpResponseBadRequest

# Create your views here.
def matsu_fes(request):
    latest_post = verPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date').first()
    context = {
        'latest_post': latest_post,
        'matsu_fes_page': True,
    }
    return render(request, 'dl_package/matsu_fes.html', context)

def verPost_list(request):
    posts = verPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'dl_package/verPost_list.html', {'posts': posts})

def verPost_detail(request, pk):
    post = get_object_or_404(verPost, pk=pk)

    now = timezone.now()
    is_future_post = post.published_date > now
    context = {
        'post': post,
        'is_future_post': is_future_post,
    }
    return render(request, 'dl_package/verPost_detail.html', context)

@staff_member_required
def verPost_new(request):
    if request.method == "POST":
        form = verPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('verPost_detail', pk=post.pk)
    else:
        form = verPostForm()
    return render(request, 'dl_package/verPost_edit.html', {'form':form})

@staff_member_required
def verPost_edit(request, pk):
    post = get_object_or_404(verPost, pk=pk)
    if request.method == 'POST':
        form = verPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('verPost_detail', pk=post.pk)
    else:
        form = verPostForm(instance=post)
    return render(request, 'dl_package/verPost_edit.html', {'form':form})

@login_required
def verPost_draft_list(request):
    posts = verPost.objects.filter(published_date__gt=timezone.now()).order_by('-created_date')
    return render(request, 'dl_package/verPost_draft_list.html', {'posts':posts})

@staff_member_required
def verPost_remove(request, pk):
    post = get_object_or_404(verPost, pk=pk)
    if request.method == 'POST':
        post.delete()
    return redirect('verPost_list')

@staff_member_required
def verPost_publish(request, pk):
    post = get_object_or_404(verPost, pk=pk)
    if request.method == 'POST':
        post.publish()
    return redirect('verPost_detail', pk=pk)

@login_required
# def download_file(request):
#     file_path = os.path.join(settings.MEDIA_ROOT, 'games', 'Handlime.zip')
#     print(f"file_path: {file_path}")

#     if not os.path.exists(file_path):
#         raise Http404("File not found.")
    
#     try:
#         response = FileResponse(open(file_path, 'rb'))

#         file_name = os.path.basename(file_path)
#         response['Content-Disposition'] = f'attachment; filename="{file_name}"'
#         return response
    
#     except Exception as e:
#         raise Http404(f"Error during file processing: {e}")

@login_required
def download_file(request):
    # ---- ① シリアル権限チェック ----
    serial_obj = check_serial_download_permission(request)
    if serial_obj is None:
        return HttpResponseForbidden("シリアル番号が登録されていないためダウンロードできません。")

    # ---- ② どちらのファイルをダウンロードするか判定 ----
    file_type = request.GET.get('file')   # "win" または "mac"

    if file_type == 'win':
        file_id = settings.TARGET_FILE_ID_WIN
    elif file_type == 'mac':
        file_id = settings.TARGET_FILE_ID_MAC
    else:
        return HttpResponseBadRequest('不正なファイルタイプです。')

    # ---- ③ Google Drive API サービスを取得 ----
    try:
        service = get_drive_service()
    except Exception as e:
        return HttpResponseServerError(f"Drive API 初期化エラー: {e}")

    # ---- ④ webContentLink を取得 ----
    try:
        drive_file = service.files().get(
            fileId=file_id,
            fields="name, webContentLink"
        ).execute()
    except Exception as e:
        return HttpResponseServerError(f"Drive API エラー: {e}")

    download_url = drive_file.get("webContentLink")
    if not download_url:
        return HttpResponseServerError("webContentLink が取得できません。共有設定を確認してください。")

    # ---- ⑤ Google Drive のダウンロードURLへリダイレクト ----
    return redirect(download_url)
    
@staff_member_required
def zip_upload(request):
    if request.method == 'POST':
        form = zipUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('matsu_fes')
    else:
        form = zipUploadForm()
    return render(request, 'dl_package/zipUpload.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))
        
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def add_serial_number(request):
    serial_obj = serialNumber.objects.filter(user=request.user).first()
    if serial_obj:
        return render(request, 'dl_package/serial_number_display.html', {'serial': serial_obj.serial_number})
    
    if request.method == 'POST':
        form = serialNumberForm(request.POST)
        if form.is_valid():
            serial_input = form.cleaned_data['serial_number']
            serial_record = serialNumber.objects.filter(serial_number=serial_input).first()

            if serial_record is None:
                form.add_error('serial_number', 'このシリアル番号は存在しません．')
            elif serial_record.user is not None:
                form.add_error('serial_number', 'このシリアル番号は既に使用されています．')
            else:
                serial_record.user = request.user
                serial_record.save()
                return redirect('matsu_fes')
    else:
        form = serialNumberForm()

    return render(request, 'dl_package/add_serial_number.html', {'form': form})

@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            if not name:
                name = '匿名'

            full_subject = f"[Handlimeお問い合わせ] {subject}"
            full_message = f"送信元メールアドレス：{email}\n送信者名：{name}\n\n問い合わせ内容：\n{message}"

            try:
                send_mail(
                    subject=full_subject,
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=settings.MANAGERS_EMAIL,
                    fail_silently=False,
                )
                return redirect('contact_thanks')
            except Exception as e:
                print(f"メール送信エラー: {e}")

    else:
        form = ContactForm()

    return render(request, 'dl_package/contact.html', {'form': form})

def contact_thanks_view(request):
    return render(request, 'dl_package/contact_thanks.html')


# 以下Gemini生成そのまま貼り付け
def get_drive_service():
    SERVICE_ACCOUNT_FILE = settings.GOOGLE_SERVICE_ACCOUNT_FILE
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def check_serial_download_permission(request):
    """
    ログインユーザーが有効かつ未使用でないシリアル番号を持っているかチェックする。
    有効なシリアル番号オブジェクト（serialNumberモデルのインスタンス）を返す。
    権限がない場合は None を返す。
    """
    if not request.user.is_authenticated:
        return None # ログインしていない
    
    # ユーザーに紐づけられているシリアル番号レコードを取得
    serial_obj = serialNumber.objects.filter(user=request.user).first()
    
    if serial_obj:
        # ここでは、紐づけられている＝有効と判断する
        return serial_obj
    else:
        return None