from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User, auth
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            if password1!=password2:
                messages.error(request, "Passwords do not match!")
                return redirect('accounts:register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return redirect('accounts:register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect('accounts:register')
            else:
                user_created = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user_created.save();
                messages.info(request, "Thanks, user created")
                return redirect('accounts:login')
        except(ValueError):
            messages.error(request,"All fields need to be filled!")
            return redirect('accounts:register')


    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user_authentication = auth.authenticate(username=username, password=password)
        if user_authentication:
            auth.login(request, user_authentication)
            return redirect('todo:list')

        else:
            messages.error(request, "Username or Password do not match, try again!")
            return redirect('accounts:login')

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('todo:index')

