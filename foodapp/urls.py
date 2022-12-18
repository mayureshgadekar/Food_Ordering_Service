from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('billing/',views.billing,name='billing'),
    path('user_reg/',views.user_reg,name='user_reg'),
    path('restaurant_reg/',views.restaurant_reg,name='restaurant_reg'),
    path('',views.index,name='index'),
    path('user_signin/',views.user_signin,name='user_signin'),
    path('res_signin/',views.res_signin,name='res_signin'),
    path('user_signin/user_page/',views.user_page,name='user_page'),
    path('user_signin/user_page/added_to_cart',views.add_cart,name='add_cart'),
    path('user_signin/user_page/deleted_from_cart',views.delete_cart,name='delete_cart'),
    path('user_signin/user_page/search',views.search,name='search'),
    path('res_signin/restaurant_menu/',views.restaurant_menu,name='restaurant_menu'),
    path('res_signin/res_menu_page/',views.res_menu_display,name='res_menu_display'),
    path('res_signin/res_menu_page/deleted_from_cart',views.delete_res_menu_item,name='delete_res_menu_item'),
    path('res_signin/orders',views.order_sum_to_res,name='order_sum_to_res'),
    path('res_signin/orders/out_for_delivery',views.out_for_delivery,name='out_for_delivery'),
    path('payment/',views.payment,name='payment'),
    path('thank_you/',views.thankyou,name='thankyou'),
    path('',views.signout,name='signout')
]