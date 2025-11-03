from django.utils import timezone
from .models import verPost
from django.shortcuts import render, get_object_or_404, redirect
from .forms import verPostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
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