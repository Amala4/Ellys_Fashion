from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .models import CustomerWish, UserOrder
from products.details import ACCOUNT_NUMBER, BANK, ACCOUNT_NAME



def signup(request):

    if request.method == 'POST':

        #Get the form values
        first_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Check if passords match
        if password == password2:

            #Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username is taken, try another username')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email address already exists!')
                    return redirect('signup')
                else:
                    # Now the user can be created
                    user = User.objects.create_user(username=username, password=password, 
                    email=email, first_name=first_name)
                    user.save()
                    messages.success(request, 'Account Created Succesfully!')
                    auth.login(request, user)
                    return redirect('index')

        else:
            messages.error(request, 'Passwords do not match, Try again!')
            return redirect('signup')

        
    else:
        return render(request, 'accounts/signup.html')



def login(request):

    if request.method == 'POST':
        
        #Get the form values
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)

        #Check if user exists 
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login Succesful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Login details!')
            return redirect('login')
        
    else:
        return render(request, 'accounts/login.html')



def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out!')
    return redirect('index')



def dashboard(request):

    wishlists = CustomerWish.objects.all().filter(user=request.user)
    orders = UserOrder.objects.all().filter(customer=request.user)

    context = {
            'wishlists': wishlists,
            'orders': orders,
            'acc_number': ACCOUNT_NUMBER,
            'acc_name': ACCOUNT_NAME,
            'bank': BANK,
            
        }
    
    return render(request, 'accounts/dashboard.html', context)

