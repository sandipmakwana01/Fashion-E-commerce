from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    path('',views.index,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('signupverify/',views.signupverify,name='signupverify'),
    path('signupdone/',views.signupdone,name='signupdone'),
    path('forgotverify/',views.forgotverify,name='forgotverify'),
    path('logoutuser/',views.logoutuser),
    path('address/',views.address,name='address'),
    path('profiledetails/',views.profiledetails,name='profiledetails'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    path('updateaddress/',views.updateaddress,name='updateaddress'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('productdetails/<str:unique_identifier>',views.productdetails,name='productdetails'),
    path('search/',views.search,name='search'),
    path('filter/',views.filter,name='filter'),
    path('category/<str:maincategory>/<str:name>',views.category,name='category'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/',views.paymentdone,name='paymentdone'),
    path('check_payment_status/', views.check_payment_status, name='check_payment_status'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('faq/', views.faq, name='faq'),
    path('download_file/', views.download_file, name='download_file'),

]