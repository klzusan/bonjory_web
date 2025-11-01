from django.shortcuts import render
from django.utils import timezone
from .models import verPost
from django.shortcuts import render, get_object_or_404
from .forms import verPostForm
from django.shortcuts import redirect

# Create your views here.
def verPost_list(request):
    posts = verPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'dl_package/verPost_list.html', {'posts': posts})

def verPost_detail(request, pk):
    post = get_object_or_404(verPost, pk=pk)
    return render(request, 'dl_package/verPost_detail.html', {'post':post})

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

def verPost_draft_list(request):
    posts = verPost.objects.filter(published_date__gt=timezone.now()).order_by('-created_date')
    return render(request, 'dl_package/verPost_draft_list.html', {'posts':posts})