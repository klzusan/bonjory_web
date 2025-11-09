from django.utils import timezone
from .models import verPost
from django.shortcuts import render, get_object_or_404, redirect
from .forms import verPostForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse, Http404
import os

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

@login_required
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

@login_required
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

@login_required
def verPost_remove(request, pk):
    post = get_object_or_404(verPost, pk=pk)
    if request.method == 'POST':
        post.delete()
    return redirect('verPost_list')

@login_required
def verPost_publish(request, pk):
    post = get_object_or_404(verPost, pk=pk)
    if request.method == 'POST':
        post.publish()
    return redirect('verPost_detail', pk=pk)

@login_required
def download_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'sample1.zip')
    print(f"file_path: {file_path}")

    if not os.path.exists(file_path):
        raise Http404("File not found.")
    
    try:
        response = FileResponse(open(file_path, 'rb'))

        file_name = os.path.basename(file_path)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    
    except Exception as e:
        raise Http404(f"Error during file processing: {e}")