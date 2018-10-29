from zappyapp import views
from django.urls import path
from django.conf import settings


app_name='zappyapp'
urlpatterns = [
    path('', views.home,name='home'),
    path('registration',views.registration,name='registration'),
    path('updateprofile',views.cprofile,name='uprofile'),
    path('profile',views.profile,name='profile'),
    path('details/<id>',views.productsdetails),
    path('search',views.search,name='search'),
    path('ReadyToeat', views.rte,name='readytoeat'),
    path('ReadyToCook', views.rtc,name='readytocook'),
    path('cart/',views.cart_home,name='cart'),
    path('cartupdate',views.cart_update,name='cartupdate'),
    ]
