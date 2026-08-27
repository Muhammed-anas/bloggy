from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View

class register_view(View):
    def get(self, request):
        register_form = UserCreationForm()
        return render (request, 'views/registration.html',
                    {'register_form':register_form})
        
            
    def post(self, request):  
        register_form = UserCreationForm(data=request.POST)
        try:
            if register_form.is_valid():
                user = register_form.save()
                user.refresh_from_db()
                login(request, user)
                messages.success(request, f'User {user.username} registered successfully')
                return redirect ('home')
            
            else:
                messages.error(request,'There is an error occured')
        except Exception as e:
            print(e)
        return render (request, 'views/registration.html',
                    {'register_form':register_form})


class login_view(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'views/login.html',
                    {'login_form':login_form})
        
    def post(self, request):
        login_form = AuthenticationForm(request = request ,data = request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, f' User {user.username} Successfully login')
                next_url = request.GET.get('next') or request.POST.get('next')
                return redirect (next_url) if next_url else redirect ('home')
            else:
                messages.error(request, f'An error occured trying to login.')
        else:
            messages.error(request, 'An error occur while login')
        
        return render(request, 'views/login.html',
                    {'login_form':login_form})
    
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, f'You are Successfully logout ')
    return redirect('main')

