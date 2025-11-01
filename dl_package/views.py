from django.shortcuts import render
from django.utils import timezone
from .models import verPost

# Create your views here.
def verPost_list(request):
    posts = verPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'dl_package/verPost_list.html', {'posts': posts})