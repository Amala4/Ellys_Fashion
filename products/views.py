from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import ProductList, Category, Colour
from user_app.models import UserOrder
from user_app.models import CustomerWish
from django.core.paginator import  Paginator
from django.db.models import Q
import random
from .details import ACCOUNT_NUMBER, BANK, ACCOUNT_NAME





def product_detail(request, product_id, product_name):

    product_item = get_object_or_404(ProductList, pk=product_id)

    # Checks if there are any related products ie products with same category
    try:
        related_products = ProductList.objects.order_by('-post_date').filter(category__name= product_item.category.name).exclude(pk=product_id)
    except:
        related_products = None

    context = {
        'product_item': product_item,
        'related_products': related_products,
       
    }

    return render(request, 'products/product-detail.html', context)


# Checks if request is ajax
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def products(request):

    if request.user.is_authenticated:
        wishlistCount = CustomerWish.objects.filter(user=request.user).count()
        request.session['wishlist'] = wishlistCount

    # products
    products = ProductList.objects.order_by('-post_date').filter(is_published=True)
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    
    # gets the Categories to display on filter section
    categories = Category.objects.all()

    # Colours
    colours = Colour.objects.all()

    #Size choices
    sizechoices = [c[0] for c in ProductList.size.field.choices]


    context = {
        'products': paged_listings,
        'categories': categories,
        'colours': colours,
        'sizes': sizechoices
    }
    return render(request, 'products/products.html', context)



def Search(request):

    if request.method == 'POST':

        #Get the search keyword
        searchKeyword = request.POST['search-input']

        #Checks if keyword is empty
        if len(searchKeyword.replace(" ", "")) == 0:
            return redirect('products')

        #saves keyword in session to be used elsewhere
        request.session['search'] = searchKeyword

        # products
        products = ProductList.objects.order_by('-post_date').filter(is_published=True)
        
        #searches through description, name, categories, colours and size
        results = products.filter(Q(description__icontains = searchKeyword) | Q(name__icontains = searchKeyword) | Q(colour__name__icontains = searchKeyword) | Q(category__name__icontains = searchKeyword) | Q(size__icontains = searchKeyword))

        paginator = Paginator(results, 9)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)
        
        context = {
            'products': paged_listings,
        }
        return render(request, 'products/searchResults.html', context)


    if request.method == 'GET':

        # Gets the saved keyword from session
        searchKeyword = request.session['search']
        
        # products
        products = ProductList.objects.order_by('-post_date').filter(is_published=True)
        results = products.filter(Q(description__icontains = searchKeyword) | Q(name__icontains = searchKeyword) | Q(colour__name__icontains = searchKeyword) | Q(category__name__icontains = searchKeyword) | Q(size__icontains = searchKeyword))

        paginator = Paginator(results, 9)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)
        
        
        context = {
            'products': paged_listings,
        }
        return render(request, 'products/searchResults.html', context)


# Product list when filter is applied
def ajaxproducts(request):

    # Gets the filter variables
    colourChoices = request.GET.getlist('colour[]')
    sizeChoices = request.GET.getlist('sizes[]')
    kidsCatChoices = request.GET.getlist('kidsCat[]')
    menCatChoices = request.GET.getlist('menCat[]')
    womenCatChoices = request.GET.getlist('womenCat[]')
    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    pagenum = request.GET.get('pagenum')
    minPrice = minPrice[1:]
    maxPrice = maxPrice[1:]
  
  
    
    queryset_all = ProductList.objects.order_by('-post_date').filter(is_published=True)

    #Evaluates queryset so as to cache it
    [entry for entry in queryset_all]

    main_query_list = []
    
    #Get colour related query
    colour_list = []
    if len(colourChoices):
        for i in range(len(colourChoices)):
            queryset = queryset_all.filter(colour__name=colourChoices[i])
            queryset = list(queryset)
            colour_list += queryset
    else:
        colour_list=queryset_all

  
    #Get size related query
    size_list = []
    if len(sizeChoices):
        for i in range(len(sizeChoices)):
            queryset = queryset_all.filter(size=sizeChoices[i])
            queryset = list(queryset)
            size_list += queryset
    else:
        size_list=queryset_all


    #Get kidsCat related query
    kidsCat_list = []
    if len(kidsCatChoices):
        for i in range(len(kidsCatChoices)):
            queryset = queryset_all.filter(gender="kids").filter(category__name=kidsCatChoices[i])
            queryset = list(queryset)
            kidsCat_list += queryset
    else:
        kidsCat_list=queryset_all

    #Get menCat related query
    menCat_list = []
    if len(menCatChoices):
        for i in range(len(menCatChoices)):
            queryset = queryset_all.filter(gender="male").filter(category__name=menCatChoices[i])
            queryset = list(queryset)
            menCat_list += queryset
    else:
        menCat_list=queryset_all

    #Get womenCat related query
    womenCat_list = []
    if len(womenCatChoices):
        for i in range(len(womenCatChoices)):
            queryset = queryset_all.filter(gender="female").filter(category__name=womenCatChoices[i])
            queryset = list(queryset)
            womenCat_list += queryset
    else:
        womenCat_list=queryset_all

    #Get minPrice related query
    minPrice_list = []
    minPricequeryset = queryset_all.filter(Q(price__gte=minPrice) | Q(promo_price__gte=minPrice))
    minPricequeryset = list(minPricequeryset)
    minPrice_list = minPricequeryset

    #Get maxPrice related query
    maxPrice_list = []
    maxPricequeryset = queryset_all.filter(Q(price__lte=maxPrice) | Q(promo_price__lte=maxPrice)) 
    maxPricequeryset = list(maxPricequeryset)
    maxPrice_list = maxPricequeryset
   
    
   
    #Combine everything to return the final queryset meeting all filter conditions
    #Since there are 7 conditions to AND together, max of 4 can be AND, 
    # so sub combinations is first done 

    #Combination 1
    if len(colour_list) and len(size_list):
        main_query_list1 = [value for value in colour_list if value in size_list]  
    else:
        main_query_list1 = combineList(colour_list, size_list)

    #Combination 2
    if len(kidsCat_list) and len(menCat_list):
        main_query_list2 = [value for value in kidsCat_list if value in menCat_list]  
    else:
        main_query_list2 = combineList(kidsCat_list, menCat_list)

    #Combination 3
    if len(womenCat_list) and len(minPrice_list):
        main_query_list3 = [value for value in womenCat_list if value in minPrice_list]
    else:
        main_query_list3 = combineList(womenCat_list, minPrice_list) 

    #Combination 4
    if len(maxPrice_list) and len(main_query_list3):
        main_query_list4 = [value for value in maxPrice_list if value in main_query_list3]  
    else:
        main_query_list4 = combineList(maxPrice_list, main_query_list3)


    main_query_list5 = [value for value in main_query_list1 if value in main_query_list2]

    # Final queryset
    main_query_list = [value for value in main_query_list4 if value in main_query_list5]  
   

    paginator = Paginator(main_query_list, 9)
    paged_listings = paginator.get_page(pagenum)

    
    
    # Categories
    categories = Category.objects.all()

    # Colours
    colours = Colour.objects.all()

    context = {
        'products': paged_listings,
        'categories': categories,
        'colours': colours
    }
    return render(request, 'products/productlist.html', context)



def Wishlist(request):
    if is_ajax(request):

        # For adding to wishlist
        if request.user.is_authenticated and 'addToWish' in request.GET:

            product_id = request.GET.get('product_id')

            # Checks if this user has already added this item to wishlist
            if CustomerWish.objects.all().filter(product_id=product_id, user=request.user):
                wishlistCount = CustomerWish.objects.filter(user=request.user).count()
                return JsonResponse({'saved': 'True', 'wishlist_count': wishlistCount}, status=200)

            else:
                wishlist = CustomerWish(product_id=product_id, user=request.user)
                wishlist.save()
                wishlistCount = CustomerWish.objects.filter(user=request.user).count()
                
                # Saves number of wishlist to session
                request.session['wishlist'] = wishlistCount
                return JsonResponse({'saved': 'True', 'wishlist_count': wishlistCount}, status=200)

        # For removing from wishlist
        if request.user.is_authenticated and 'remFroWish' in request.GET:
            product_id = request.GET.get('product_id')

            CustomerWish.objects.filter(product_id=product_id, user=request.user).delete()

            wishlistCount = CustomerWish.objects.filter(user=request.user).count()

            # Updates the wishlist count on session
            request.session['wishlist'] = wishlistCount
            return JsonResponse({'removed': 'True', 'wishlist_count': wishlistCount}, status=200)



def Cart(request):

    # For adding to cart
    if is_ajax(request) and 'addToCart' in request.GET:

        # Gets the details from request
        product_id = request.GET.get('product_id')
        product_price = request.GET.get('product_price')
        product_name = request.GET.get('product_name')
        product_price_tot = request.GET.get('product_price_tot')
        quantity = request.GET.get('quantity')
        imageUrl = request.GET.get('imageUrl')
        
        cartItemList= []

        
        if 'cart_items' in request.session:
            # Checks if items have already been added to cart
            for elem in request.session['cart_items']:
                if ("product_id", product_id) in elem.items():

                    cartItemsCount = len(request.session['cart_items'])

                    return JsonResponse({'added': 'True', 'count': cartItemsCount}, status=200)
                    
            
            for item in request.session['cart_items']:
                cartItemList.append(item) 
            
            cartItemsDic= dict()
            cartItemsDic["product_id"] = product_id
            cartItemsDic["product_name"] = product_name
            cartItemsDic["quantity"] = quantity
            cartItemsDic["product_price_tot"] = product_price_tot
            cartItemsDic["product_price"] = product_price
            cartItemsDic["imageUrl"] = imageUrl

            cartItemList.append(cartItemsDic)

            request.session['cart_items'] = cartItemList

            cartItemsCount = str(len(cartItemList))
            request.session['cart_items_count'] = cartItemsCount

            return JsonResponse({'added': 'True', 'count': cartItemsCount}, status=200)
            
        else:
            cartItemsDic= dict()
            cartItemsDic["product_id"] = product_id
            cartItemsDic["product_name"] = product_name
            cartItemsDic["quantity"] = quantity
            cartItemsDic["product_price_tot"] = product_price_tot
            cartItemsDic["product_price"] = product_price
            cartItemsDic["imageUrl"] = imageUrl

            cartItemList.append(cartItemsDic)

            request.session['cart_items'] = cartItemList
            cartItemsCount = str(len(cartItemList))
            request.session['cart_items_count'] = cartItemsCount

            return JsonResponse({'added': 'True', 'count': cartItemsCount}, status=200)


    # For removing from cart
    elif is_ajax(request) and 'remFroCart' in request.GET:
        
        product_id = request.GET.get('product_id')
        cartItems = request.session['cart_items']
      
        for index in range(len(cartItems)):
            if int(cartItems[index]['product_id']) == int(product_id):
                del cartItems[index]
                break

        
        request.session['cart_items'] = cartItems
        cartItemsCount = str(len(cartItems))
        request.session['cart_items_count'] = cartItemsCount

        return JsonResponse({'removed': 'True', 'count': cartItemsCount}, status=200)


    # For placing order
    elif is_ajax(request) and request.user.is_authenticated and 'placeOrder' in request.GET:

        order_ids = request.GET.getlist('order_ids[]')
        order_prices = request.GET.getlist('order_prices[]')
        order_qtys = request.GET.getlist('order_qtys[]')
        phoneNo = request.GET.get('phoneNo')
        address = request.GET.get('address')
        orderTot = request.GET.get('orderTot')
        
        # Generate 4-digit Reference ID
        randNo = random.randint(1000,9999)

        # Final ref id would contain the username + the 4 digit code
        order_reference_id = str(request.user.username)+str(randNo)

        # Check if such ref_id already exists in DB
        while UserOrder.objects.all().filter(order_reference_id=order_reference_id ):

            # If it exists, generate another one
            randNo = random.randint(1000,9999)
            order_reference_id = str(request.user.username)+str(randNo)

        # Loop through all the orders and save
        for i in range(len(order_ids)):
       
            order_entry = UserOrder(
                item_ordered_id=order_ids[i], 
                item_total_price=order_prices[i], 
                quantity=order_qtys[i], 
                customer_phone_no=str(phoneNo),
                delivery_address=address,
                order_total_price=orderTot,
                customer=request.user,
                order_reference_id=order_reference_id
                )

            order_entry.save()

        # When order is placed Empty the cart in session
        del request.session['cart_items']
        request.session['cart_items_count'] = str(0)
        
        context = {
            'acc_number': ACCOUNT_NUMBER,
            'acc_name': ACCOUNT_NAME,
            'bank': BANK,
            'ref_id': order_reference_id
        }
        return render(request, '_ordersuccess.html', context)


    else:
        return render(request, 'products/shop-cart.html')



def combineList(list1, list2):
    return list(set().union(list1,list2))
