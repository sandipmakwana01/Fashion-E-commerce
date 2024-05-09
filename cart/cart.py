from application.models import *
from decimal import Decimal  # Import Decimal for handling decimal numbers
import qrcode

class Cart():
    def __init__(self, request):
        self.session = request.session 

        # get request 
        self.request = request

        # Get the current cart from session if it exists
        self.cart = self.session.get('cart', {})

        # print(self.cart)

    def db_add(self, product, quantity, size=None, color=None):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            # If the product is already in the cart, update the quantity
            self.cart[product_id]['quantity'] += int(product_qty)
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            # self.cart[product_id] = int(product_qty)
            self.cart[product_id] = {'quantity': int(product_qty), 'size': size, 'color': color}

        self.session['cart'] = self.cart
        self.session.modified = True

        # deal with logges in user 
        if self.request.session.get('id') is not None:

            # get cyrrent user profile 
            current_user = signupdata.objects.filter(id=self.request.session.get('id'))
            
            carty =str(self.cart)
            carty = carty.replace("\'","\"")

            #save carty to signupdata model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity, size=None, color=None):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            # If the product is already in the cart, update the quantity
            self.cart[product_id]['quantity'] += int(product_qty)
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            # self.cart[product_id] = int(product_qty)
            self.cart[product_id] = {'quantity': int(product_qty), 'size': size, 'color': color}

        self.session['cart'] = self.cart
        self.session.modified = True

        # deal with logges in user 
        if self.request.session.get('id') is not None:

            # get cyrrent user profile 
            current_user = signupdata.objects.filter(id=self.request.session.get('id'))
            
            carty =str(self.cart)
            carty = carty.replace("\'","\"")

            #save carty to signupdata model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # get ids form cart
        product_id = self.cart.keys()

        # use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_id)

        for product in products:
            cart_item = self.cart.get(str(product.id))
            if cart_item:
                product.cart_quantity = cart_item['quantity']
                product.cart_size = cart_item.get('size', None)
                product.cart_color = cart_item.get('color', None)

        # return looked ups products
        return products
    
    
    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Update the quantity of the product in the cart
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_qty

        # Save the updated cart to the session
        
        self.session.modified = True

        
        # deal with logges in user ######## save oldcar in db 
        if self.request.session.get('id') is not None:

            # get cyrrent user profile 
            current_user = signupdata.objects.filter(id=self.request.session.get('id'))
            
            carty =str(self.cart)
            carty = carty.replace("\'","\"")

            #save carty to signupdata model
            current_user.update(old_cart=str(carty))
        ########## save oldcar in db 

        self.session['cart'] = self.cart
        # Return the updated cart
        return self.cart
    
    def delete(self, product):
        product_id = str(product)
        # delete from dictinoray/cart
        if product_id in self.cart:
            del self.cart[product_id] 

        self.session.modified = True 


        
        # deal with logges in user ######## save oldcar in db 
        if self.request.session.get('id') is not None:

            # get cyrrent user profile 
            current_user = signupdata.objects.filter(id=self.request.session.get('id'))
            
            carty =str(self.cart)
            carty = carty.replace("\'","\"")

            #save carty to signupdata model
            current_user.update(old_cart=str(carty))
        ########## save oldcar in db 

    def cart_total(self):
        # get product ids
        product_ids = self.cart.keys()
        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Initialize total as a Decimal
        total = Decimal('0')

        for product in products:
            # Get quantity of the current product in the cart
            quantity = self.cart[str(product.id)]['quantity']

            # Calculate the total price for the current product
            if product.is_sale:
                total += product.sale_price * quantity
            else:
                total += product.price * quantity

        
        # Assuming 'total_amount' contains the total amount to be paid
        total_amount = total  # Example total amount
        payment_data = f"upi://pay?pa=7567626592@ybl&pn=E-Commerce&am={total_amount}&cu=INR"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(payment_data)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("static/images/paymentqrcode/payment_qr.png") 
        # img.save("payment_qr.png")  # Save QR code image to a file

        return total
    
   

    # payment done 
    def delete_all_items(self):
        self.cart = {}  # Clear the cart
        self.session['cart'] = {}  # Clear the cart in session
        self.session.modified = True  # Save changes to session

        # Deal with logged-in user
        if self.request.session.get('id') is not None:
            current_user = signupdata.objects.filter(id=self.request.session.get('id'))
            current_user.update(old_cart="")  # Clear old_cart field

