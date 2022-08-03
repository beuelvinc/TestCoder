from django.urls import path
from .views import *

app_name="main"

urlpatterns = [
    path('', home,name='main_page'),
    path('/privacy', privacy,name='privacy_page'),
    path('/login',login,name='login_page'),
    path('/logout',logout,name='logout_page'),
    path('/products',products,name='product_page'),
    path('/product_detail/<int:id>',product_detail,name='product_detail'),
    path('/edit_product/<int:id>',edit_product,name='edit_product'),
    path('/create_product',create_product,name='create_product'),



    path('/create_user',create_user,name='create_user_page'),

    path('/edit_profile',edit_profile,name='edit_profile_page'),
    path('/my_profile',my_profile,name='my_profile'),
    


]
