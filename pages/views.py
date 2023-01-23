from django.shortcuts import render, redirect
from products.models import ProductList
from user_app.models import CustomerWish
from pages.models import Contact, Subscribers
from django.contrib import messages




def index(request):
    if request.user.is_authenticated:
        wishlistCount = CustomerWish.objects.filter(user=request.user).count()
        request.session['wishlist'] = wishlistCount

    # Gets new products and number of each categories
    gown_count = ProductList.objects.order_by('-post_date').filter(category__name="Gowns").count()
    new_gown = ProductList.objects.order_by('-id').filter(category__name="Gowns")[:1]
    two_piece_count = ProductList.objects.order_by('-post_date').filter(category__name="Two Piece").count()
    new_two_piece = ProductList.objects.order_by('-id').filter(category__name="Two Piece")[:1]
    unisex_count = ProductList.objects.order_by('-post_date').filter(category__name="Unisex").count()
    new_unisex = ProductList.objects.order_by('-id').filter(category__name="Unisex")[:1]
    cosmetics_count = ProductList.objects.order_by('-post_date').filter(category__name="Cosmetics").count()
    new_cosmetics = ProductList.objects.order_by('-id').filter(category__name="Cosmetics")[:1]
    
    # Gets the hot trends and co
    hot_trends = ProductList.objects.order_by('-post_date').filter(hot_trend=True)
    best_sellers = ProductList.objects.order_by('-post_date').filter(best_seller=True)
    featured = ProductList.objects.order_by('-post_date').filter(feature=True)

    context = {
        'new_gown': new_gown,
        'gown_count': gown_count,
        'new_two_piece': new_two_piece,
        'two_piece_count': two_piece_count,
        'new_unisex': new_unisex,
        'unisex_count': unisex_count,
        'new_cosmetics': new_cosmetics,
        'cosmetics_count': cosmetics_count,
        'hot_trend': hot_trends,
        'best_seller': best_sellers,
        'feature': featured,
        
    }
    return render(request, 'pages/index.html', context)



def terms(request):
    return render(request, 'pages/terms.html')



def privacy(request):
    return render(request, 'pages/privacy.html')



def about(request):
    return render(request, 'pages/about.html')



def contact(request):
    if request.method == 'POST':

        #Get the form values
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        contact = Contact(name=name, email=email, message=message )
        contact.save()
        
        #send email to admin
        # send_mail(
        #     'Inquiry from your website',
        #     'Sender: '+email+'\nMessage: '
        #     +message,
        #     'frankfny@gmail.com',
        #     ['frankfny@gmail.com'],
        #     fail_silently=False
        # )

        messages.success(request, 'Message sent succesfully')
        return render(request, 'pages/contact.html')


    return render(request, 'pages/contact.html')



def subscribe(request):
    if request.method == 'POST':

        #Get the form values
        email = request.POST['email']

        subscriber = Subscribers(email=email )
        subscriber.save()
        
        messages.success(request, 'You have now subscribed')
        return redirect('index')


    return render(request, 'pages/index.html')