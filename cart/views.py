from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from application.models import *
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    username = request.session.get('username')

    if username:
        # Get cart
        cart = Cart(request)
        cart_product = cart.get_prods()
        qunitites = cart.get_quants()
        totals = cart.cart_total()
    
        # modify
        maincategory_list = MainCategory.objects.all()
        main_subcategory_dict = {}

        for main_category in maincategory_list:
            subcategories = SubCategory.objects.filter(main_category=main_category)
            main_subcategory_dict[main_category] = subcategories

        return render(request,'cart_summary.html',{'username': username, 'noneuser': 'User','cart_product':cart_product,'qunitites':qunitites,'totals':totals,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict})
    else:
        return redirect('login')

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Get the selected product size
        product_size = request.POST.get('product_size')  

        # Get the selected product color
        product_color = request.POST.get('product_color')  

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session                                          
        cart.add(product=product , quantity=product_qty, size=product_size, color=product_color)

        # Cart Quantity 
        cart_quantity = cart.__len__()
        # cart_quantity = len(cart)

        response_data = {
            'Product Name': product.name,
            'Product Quantity': product_qty,
            'Size': product_size,  # Include size in the response
            'Color': product_color,  # Include size in the response
            'Cart Quantity': cart_quantity
        }
    
        return JsonResponse(response_data)

def cart_update(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        
        # Get the product ID and the new quantity
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Call the update method in the cart object to update the quantity
        cart.update(product=product_id, quantity= product_qty)

        # Return a JSON response with the updated quantity
        response = JsonResponse({'qty':product_qty})
        return response
        # return redirect('cart_summary')

def cart_delete(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # call delete function in cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        return response
        # return redirect('cart_summary')


