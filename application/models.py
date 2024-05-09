from django.db import models
import uuid

class signupdata(models.Model):
    emailorphone=models.CharField(max_length=50,blank=True)
    username=models.CharField(max_length=50,blank=True)
    password=models.CharField(max_length=50,blank=True)
    image = models.ImageField( blank=True,upload_to='UpdateProfile/')
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50,blank=True)
    phone  = models.CharField(max_length=15,blank=True)
    old_cart = models.TextField(blank=True)

class contact(models.Model):
    time=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    subject=models.CharField(max_length=50)
    message=models.TextField()

class MainCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name   

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class ProductSize(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class PriceRange(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    maincategory = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    description = models.CharField(max_length=250,default='',blank=True,null=True)
    colors = models.ManyToManyField(Color, blank=True)
    size =  models.ManyToManyField(ProductSize,blank=True)
    pricerange = models.ForeignKey(PriceRange,on_delete=models.CASCADE, null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    image1 = models.ImageField(upload_to='Product/')
    image2 = models.ImageField(upload_to='Product/', default='')
    image3 = models.ImageField(upload_to='Product/', default='')
    image4 = models.ImageField(upload_to='Product/', default='')
    image5 = models.ImageField(upload_to='Product/', default='')
    image6 = models.ImageField(upload_to='Product/', default='')
    unique_identifier = models.CharField(max_length=100, unique=True, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.unique_identifier:
            # Generate a unique identifier using UUID
            self.unique_identifier = str(uuid.uuid4())
        super().save(*args, **kwargs)


class Payment(models.Model):
    transaction_id = models.TextField()

class Subscribe(models.Model):
    email = models.CharField(max_length=100)