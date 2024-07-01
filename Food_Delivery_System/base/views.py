from django.shortcuts import render


# Create your views here.
def homepage(request):
    return render(request, template_name='base/homepage.html')


def about(request):
    return render(request, template_name="base/about.html")
