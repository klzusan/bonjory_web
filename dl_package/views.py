from django.shortcuts import render

# Create your views here.
def verPost_list(request):
    return render(request, 'dl_package/verPost_list.html', {})