import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.shortcuts import redirect, render
from core.forms import LoginForm, RegistrationForm


def get_user_by_username(username):
    try:
        db_user = User._default_manager.get(username__iexact=username)
    except User.DoesNotExist:
        db_user = None
    return db_user


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = get_user_by_username(form.cleaned_data['username'])
            if user is not None:
                # Use the case sensitive username this time.
                user = authenticate(username=user.username, password=form.cleaned_data['password'])
                if user is not None:
                    if user.is_active:
                        django.contrib.auth.login(request, user)
                        return redirect('dashboard')
                    else:
                        form._errors['username'] = ErrorList(['This user is disabled.'])
                else:
                    form._errors['username'] = ErrorList(['The username/password is wrong.'])
            else:
                form._errors['username'] = ErrorList(['This user does not exist.'])
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Searches for user in a case-insensitive fashion.
            # See http://stackoverflow.com/questions/13190758/django-case-insensitive-matching-of-username-from-auth-user.
            if get_user_by_username(form.cleaned_data['username']) is not None:
                form._errors['username'] = ErrorList(['This username is already taken.'])
            else:
                try:
                    db_user = User._default_manager.get(email__iexact=form.cleaned_data['email'])
                except User.DoesNotExist:
                    db_user = None

                if db_user is not None:
                    form._errors['email'] = ErrorList(['This email is already taken.'])
                else:
                    User.objects.create_user(
                        form.cleaned_data['username'],
                        form.cleaned_data['email'],
                        form.cleaned_data['password']
                    )
                    return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})
