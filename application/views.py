from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.http import HttpResponse
from eCommerce import settings
from django.db.models import Q
from itertools import chain
from cart.cart import Cart
from .forms import *
from .models import *
import requests
import random
import ast
import re
import os

 

def login(request):
    message=''

    username=request.session.get('username')

    all_products = Product.objects.all()

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

    if request.method=='POST':

        emailorphone=request.POST['emailorphone']
        password=request.POST['password']

        if emailorphone=='' and password == '':
            message="Enter Your Email or Phone Number and Password"
        elif emailorphone != '' and password == "":
            message="Enter Your Password"
        elif password != "" and emailorphone == "":
            message="Enter Your Email or Phone Number"
        else:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            phone_pattern = r'^[0-9]{10,12}$'

            if re.match(email_pattern, emailorphone):
                verifyemail=signupdata.objects.filter(emailorphone=emailorphone)

                if verifyemail:
                    verifypassword=signupdata.objects.filter(password=password)

                    if verifypassword:
                        alldata=signupdata.objects.get(emailorphone=emailorphone)
                        request.session['username']=alldata.username
                        request.session['id']=alldata.id

                        currunt_user = signupdata.objects.get(id=request.session.get('id'))
                        saved_cart = currunt_user.old_cart
                        print("Saved Cart Data:",saved_cart)

                        username=request.session.get('username')

                        all_products = Product.objects.all()
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

                        if saved_cart:

                            

                            # converted_cart = json.loads(saved_cart)
                            converted_cart = ast.literal_eval(saved_cart)
                            print("Converted Cart Data:", converted_cart)
                            cart = Cart(request)
                            for key, value in converted_cart.items():
                                print("Key:", key)
                                print("Value:", value)
                                
                                # Access quantity from the value dictionary
                                quantity = value.get('quantity')
                                print("Quantity:", quantity)
                                
                                # Access size from the value dictionary
                                size = value.get('size')
                                print("Size:", size)

                                # Access size from the value dictionary
                                color = value.get('color')
                                print("Color:", color)

                                cart = Cart(request)
                                cart.db_add(product=key, quantity=quantity, size=size, color=color)

                                message = 'Login successful.'

                        return render(request,'index.html',{'message':message,'username': username, 'noneuser': 'User',"all_products":all_products,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})
                    else:
                        message='Password is Wrong please Enter right password'
                else:
                    message="Please enter ragisterd email or phone number"

            elif re.match(phone_pattern,emailorphone):
                verifyemail=signupdata.objects.filter(emailorphone=emailorphone)

                if verifyemail:
                    verifypassword=signupdata.objects.filter(password=password)

                    if verifypassword:
                        alldata=signupdata.objects.get(emailorphone=emailorphone)
                        request.session['username']=alldata.username
                        request.session['id']=alldata.id

                        currunt_user = signupdata.objects.get(id=request.session.get('id'))
                        saved_cart = currunt_user.old_cart

                        print("Saved Cart Data:",saved_cart)

                        username=request.session.get('username')

                        all_products = Product.objects.all()
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
                        if saved_cart:
                            
                            # converted_cart = json.loads(saved_cart)
                            converted_cart = ast.literal_eval(saved_cart)
                            print("Converted Cart Data:", converted_cart)
                            cart = Cart(request)
                            for key, value in converted_cart.items():
                                print("Key:", key)
                                print("Value:", value)
                                
                                # Access quantity from the value dictionary
                                quantity = value.get('quantity')
                                print("Quantity:", quantity)
                                
                                # Access size from the value dictionary
                                size = value.get('size')
                                print("Size:", size)

                                # Access size from the value dictionary
                                color = value.get('color')
                                print("Color:", color)

                                cart = Cart(request)
                                cart.db_add(product=key, quantity=quantity, size=size, color=color)

                                message = 'Login successful.'

                        return render(request,'index.html',{'message':message,'username': username, 'noneuser': 'User',"all_products":all_products,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})
                    else:
                        message='Passeord is Wrong please Enter right password'
                else:
                    message="Please enter ragisterd email or phone number"
            else:
                message='Enter Valide Email Or Phone Number'

    return render(request,'login.html',{'message':message,'username': username, 'noneuser': 'User',"all_products":all_products,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})

def signup(request):
    message=''
    if request.method=='POST':

        global email_or_phone
        email_or_phone = request.POST['emailorphone']

        if email_or_phone=='':
            message = 'Please enter an email or phone number.'
        else:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            phone_pattern = r'^[0-9]{10,12}$'

            if re.match(email_pattern, email_or_phone):   

                if signupdata.objects.filter(emailorphone=email_or_phone): 
                    message = 'This email or phone number is already registered. Please enter a different email or phone number.'
                else:
                    # Generate OTP
                    createotp=random.randint(1111,9999)

                    # Save OTP in session
                    request.session['signup_otp'] = createotp

                    # Email Sending Code 
                    subject='Your Sign Up OTP !'
                    msg=f'Your OTP is \n {createotp}'
                    from_email=settings.EMAIL_HOST_USER
                    to_email=[email_or_phone]
                    send_mail(subject=subject,message=msg,from_email=from_email,recipient_list=to_email)

                    return redirect('signupverify')

            elif re.match(phone_pattern, email_or_phone):

                if signupdata.objects.filter(emailorphone=email_or_phone): 
                    message = 'This email or phone number is already registered. Please enter a different email or phone number.'
                else:
                    # Generate OTP
                    createotp=random.randint(1111,9999)

                    # Save OTP in session
                    request.session['signup_otp'] = createotp

                    # SMS Sending Code 
                    url = "https://www.fast2sms.com/dev/bulkV2"
                    querystring = {"authorization":"FavsoRHrVAJct8lxMNwySgITjX2KzUbumqB954QifGC0P63W7Ylrqmy16VNfdQxXwvUAnWPLcoG07Yse","variables_values":f"{createotp}","route":"otp","numbers":f"{email_or_phone}"}
                    headers = {
                        'cache-control': "no-cache"
                    }
                    response = requests.request("GET", url, headers=headers, params=querystring)
                    print(response.text)    

                    return redirect('signupverify')
            else:
                message = 'Please Enter Valid Email Or Phone Number'

    return render(request,'signup.html', {'message': message})

def signupverify(request):
    message = ''
    stored_otp = request.session.get('signup_otp')
    print(stored_otp)

    if request.method == 'POST':
        user_input_otp = request.POST['otp']

        if user_input_otp == '':
            message = "Please enter the OTP."
        elif user_input_otp == str(stored_otp):
            return redirect("signupdone")
        else:
            message = "Incorrect OTP. Please try again."

    return render(request,'signupverify.html', {'message': message})

def signupdone(request):

    global email_or_phone
    message=''

    if request.method=='POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not (username and password and confirm_password):
            message = 'Please fill in all the required fields.'
        elif password != confirm_password:
            message = 'Passwords do not match.'
        else:
            form_data = {
                'emailorphone': email_or_phone,
                'username': username,
                'password': password,
            }
            signup_form = signupform(form_data, request.FILES)
            if signup_form.is_valid():
                signup_form.save()
                return redirect('login')
            else:
                message = signup_form.errors

    return render(request,'signupdone.html',{'message':message,'email_or_phone':email_or_phone})

def forgotverify(request):
    message=''
    if request.method=='POST':
        emailorphone=request.POST['emailorphone']

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'^[0-9]{10,12}$'

        if re.match(email_pattern, emailorphone):
            if signupdata.objects.filter(emailorphone=emailorphone): 

                password =  signupdata.objects.get(emailorphone=emailorphone)
                passeordsend= password.password
                print(passeordsend)

                # Email Sending Code 
                subject='Your Password!'
                msg=f'Your Password is \n {passeordsend}'
                from_email=settings.EMAIL_HOST_USER
                to_email=[emailorphone]
                print(to_email)
                send_mail(subject=subject,message=msg,from_email=from_email,recipient_list=to_email)

                return redirect('login')
            else:
                message='You have not ragisterd user please check your email or phone number'

        elif re.match(phone_pattern,emailorphone):
            message= 'Password recovery via email only. No phone number option'

    return render(request,'forgotverify.html',{'message':message})

def logoutuser(request):
    logout(request)
    message = 'Logout successful.'

    username=request.session.get('username')

    all_products = Product.objects.all()

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

    return render(request,'index.html',{'message':message,'username': username, 'noneuser': 'User',"all_products":all_products,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})


def profiledetails(request):
    username=request.session.get('username')

    # Get cart
    cart = Cart(request)
    cart_product = cart.get_prods()
    qunitites = cart.get_quants()
    totals = cart.cart_total()

    userid=request.session.get('id')
    alldata=signupdata.objects.get(id=userid)

    # modify
    maincategory_list = MainCategory.objects.all()
    main_subcategory_dict = {}

    for main_category in maincategory_list:
        subcategories = SubCategory.objects.filter(main_category=main_category)
        main_subcategory_dict[main_category] = subcategories

    return render(request,'profiledetails.html',{'username':username,'noneuser':'User','alldata':alldata,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})

def updateprofile(request):
    message=''

    userid=request.session.get('id')
    alldata=signupdata.objects.get(id=userid)

    if request.method=='POST':
        updateform=signupform(request.POST)
        if updateform.is_valid():
            updateform=signupform(request.POST,request.FILES,instance=alldata)
            updateform.save()
            return redirect('profiledetails')
        else:
            message=updateform.errors

    return render(request,'updateprofile.html',{"alldata":alldata,'message':message})

def updateaddress(request):
    message=''

    userid=request.session.get('id')
    alldata=signupdata.objects.get(id=userid)

    if request.method=='POST':
        updateform=adsressform(request.POST)
        if updateform.is_valid():
            updateform=adsressform(request.POST,instance=alldata)
            updateform.save()
            return redirect('address')
        else:
            message=updateform.errors
    return render(request,'updateaddress.html',{"alldata":alldata,'message':message})

def address(request):
    username=request.session.get('username')
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

    userid=request.session.get('id')
    alldata=signupdata.objects.get(id=userid)

    return render(request,'address.html',{'username':username,'noneuser':'User',"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals,'alldata':alldata})

def about(request):
    username=request.session.get('username')
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
    return render(request,"about.html",{'username':username,'noneuser':'User',"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})

def contact(request):
    message=''
    username=request.session.get('username')
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

    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        get_message=request.POST['message']
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not any((name, email, subject, get_message)):
            message = 'Enter a name, email, subject and message.'
        elif not all((username, email,subject, get_message)):
            message = 'Enter all fields.'
        else:
            if re.match(email_pattern, email):
                contactf=contactform(request.POST)
                if contactf.is_valid():
                    contactf.save()
                    message='Thank you. The Mailman is on His Way :)'
                else:
                    message="Sorry, don't know what happened. Try later :("
            else:
                message="Please Enter Valid Email"

    return render(request,"contact.html",{'username':username,'noneuser':'User','message':message,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})

def index(request):
    username=request.session.get('username')

    all_products = Product.objects.all()

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

    return render(request,'index.html', {'username': username, 'noneuser': 'User',"all_products":all_products,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})

def productdetails(request, unique_identifier):
    username=request.session.get('username')

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

        product = Product.objects.filter(unique_identifier=unique_identifier).first()

        if product:
            item = product
        else:
            # Product not found, handle the case accordingly
            return render(request, 'product_not_found.html')
        
        # Perform additional operations if needed
        colors = item.colors.all()
        size = item.size.all()

        return render(request, 'productdetails.html', {'item': item,'colors':colors,'size':size,'username':username,'noneuser':'User',"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})

    else:
        return redirect('login')

def category(request,name,maincategory):
    username=request.session.get('username')
    # Get cart
    cart = Cart(request)
    cart_product = cart.get_prods()
    qunitites = cart.get_quants()
    totals = cart.cart_total()

    maincategory_list = MainCategory.objects.all()
    main_subcategory_dict = {}

    for main_category in maincategory_list:
        subcategories = SubCategory.objects.filter(main_category=main_category)
        main_subcategory_dict[main_category] = subcategories

    # Retrieve the main category object
    main_category = MainCategory.objects.get(name=maincategory)

    # Retrieve the subcategory object
    subcategory = SubCategory.objects.get(name=name, main_category=main_category)

    # Retrieve products belonging to the specified main category and subcategory
    products = Product.objects.filter(maincategory=main_category, subcategory=subcategory)

    # get all colors 
    all_colors = Color.objects.all()
    # get all price range 
    all_pricerange = PriceRange.objects.all()
    # get all subcategory
    all_subcategory = SubCategory.objects.all()
    # get all size
    all_size = ProductSize.objects.all()

    return render(request,'category.html',{"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,"products": products,'all_colors':all_colors,'all_pricerange':all_pricerange,'all_subcategory':all_subcategory,'username':username,'noneuser':'User','all_size':all_size,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})

def search(request):
    username = request.session.get('username')

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

    # search product
    search_results = []
    if request.method == 'POST':
        searched = request.POST.get('search', '')  # Use .get() method to avoid MultiValueDictKeyError

        products = Product.objects.filter(
            Q(description__icontains=searched) | 
            Q(name__icontains=searched) | 
            Q(subcategory__name__icontains=searched) | 
            Q(maincategory__name__icontains=searched) | 
            Q(size__name__icontains=searched)
        ).distinct()

        # Combine search results
        search_results.extend(list(chain(products)))

    # get all colors 
    all_colors = Color.objects.all()
    # get all price range 
    all_pricerange = PriceRange.objects.all()
    # get all subcategory
    all_subcategory = SubCategory.objects.all()
    # get all size
    all_size = ProductSize.objects.all()

    return render(request, 'search.html', {'search_results': search_results, 'username': username, 'noneuser': 'User',"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'all_colors':all_colors,'all_pricerange':all_pricerange,'all_subcategory':all_subcategory,'all_size':all_size,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})

def filter(request):
    username = request.session.get('username')

    # Get cart
    cart = Cart(request)
    cart_product = cart.get_prods()
    qunitites = cart.get_quants()
    totals = cart.cart_total()

    maincategory_list = MainCategory.objects.all()
    main_subcategory_dict = {}

    for main_category in maincategory_list:
        subcategories = SubCategory.objects.filter(main_category=main_category)
        main_subcategory_dict[main_category] = subcategories

    if request.method == 'POST':
        # Get filter parameters from the form
        subcategory = request.POST.get('subcategory', None)
        price_range = request.POST.get('price_range', None)
        color = request.POST.get('color', None)
        size = request.POST.get('size',None)
        
        # Filter products based on the selected parameters
        products = Product.objects.all()
        if subcategory:
            products = products.filter(subcategory__name=subcategory)
        if price_range:
            products = products.filter(pricerange__name=price_range)
        if color:
            products = products.filter(colors__name=color)
        if size:
            products = products.filter(size__name=size)

    # get all colors 
    all_colors = Color.objects.all()
    # get all price range 
    all_pricerange = PriceRange.objects.all()
    # get all subcategory
    all_subcategory = SubCategory.objects.all()
    # get all size
    all_size = ProductSize.objects.all()
        
    return render(request, 'category.html', {'products': products,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'all_colors':all_colors,'all_pricerange':all_pricerange,'all_subcategory':all_subcategory,'username': username,'all_size':all_size,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})
    
def checkout(request):
    username = request.session.get('username')

    if username:
        userid=request.session.get('id')
        alldata=signupdata.objects.get(id=userid)
    
        # Get cart
        cart = Cart(request)
        cart_product = cart.get_prods()
        qunitites = cart.get_quants()
        totals = cart.cart_total()

        maincategory_list = MainCategory.objects.all()
        main_subcategory_dict = {}

        for main_category in maincategory_list:
            subcategories = SubCategory.objects.filter(main_category=main_category)
            main_subcategory_dict[main_category] = subcategories

        return render(request,'checkout.html',{'cart_product':cart_product,'qunitites':qunitites,'totals':totals,'username': username, 'noneuser': 'User',"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'alldata':alldata})
    else:
        return redirect('login')

def paymentdone(request):
    return render(request,'paymentdone.html')

def check_payment_status(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        check_form = paymentform(request.POST)

        if check_form.is_valid():
            check_form.save()

        payment_completed = check_payment_completed(transaction_id)

        if payment_completed:
            # Delete cart items
            cart = Cart(request)
            cart.delete_all_items()
            return redirect('paymentdone')
        else:
            return redirect('checkout')
        
    else:
        # Only accept POST requests
        return HttpResponse(status=405)

def check_payment_completed(transaction_id):

    payment_exists = Payment.objects.filter(transaction_id=transaction_id).exists()

    # return payment_exists
    return bool(payment_exists)


def subscribe(request):
    message=''
    username=request.session.get('username')

    if username:
        all_products = Product.objects.all()

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

        if request.method == 'POST':
            email=request.POST['email']
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            if re.match(email_pattern, email):
                newsub = subform(request.POST)
                if newsub.is_valid():
                    newsub.save()
                    message = 'Subscription successful.'
                else:
                    message = 'Error: Please enter a valid email.'
            else:
                message = 'Error: Please enter a valid email.'

        return render(request,'index.html',{'message':message,'username': username, 'noneuser': 'User',"all_products":all_products,"maincategory_list":maincategory_list,"main_subcategory_dict": main_subcategory_dict,'cart_product':cart_product,'qunitites':qunitites,'totals':totals})
    else:
        return redirect('login')

def faq(request):
    return render(request,'faq.html')

def download_file(request):
    username = request.session.get('username')

    if username:

        file_path = os.path.join(settings.BASE_DIR, 'static', 'aboutuspdf.pdf')

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file_path)
                return response
        else:
            return HttpResponse("File not found", status=404)
    else:
        return redirect('login')