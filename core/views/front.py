from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})