from django.contrib import admin
from  .models import *

class signupdatashow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','emailorphone','username','password','image','old_cart']
admin.site.register(signupdata,signupdatashow)

class contactdatashow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','time','name','email','subject','message']
admin.site.register(contact,contactdatashow)

class colorshow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','name']
admin.site.register(Color,colorshow)

class productsizeshow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','name']
admin.site.register(ProductSize,productsizeshow)

class pricerangeshow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','name']
admin.site.register(PriceRange,pricerangeshow)

class maincategoryshow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','name']
admin.site.register(MainCategory,maincategoryshow)

class subcategoryshow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','name','main_category']
admin.site.register(SubCategory,subcategoryshow)

class productshow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','name','price','description','pricerange','is_sale','sale_price','unique_identifier']
admin.site.register(Product,productshow)

class subshow(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','email']

admin.site.register(Subscribe,subshow)