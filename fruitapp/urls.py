from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from fruitapp.views import *
from fruitapp.views.checkout import GetAddressView

app_name="fruitapp"

urlpatterns = [
    path(r'', ProductListView.as_view(), name="products"),
    path('products/', ProductListView.as_view(), name="products"),
    path('product/<int:id>', productDetail, name="product"),
    path('mycart/',CardView.as_view(),name='cart'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('addcart/<int:value>',Add_to_cart,name='addcart'),
    path('udpatecart/<int:value>',Update_cart,name='updatecart'),
    path('decreasecount/<int:value>',decrease_count,name='decreasecount'),
    path('addfavorite/<int:value>',Add_to_favorites,name='addfavorite'),
    path('removefavorite/<int:value>',Remove_favorites,name='removefavorite'),
    path('profile/',userprofile,name='profile'),
    path('search/',Search_func ,name='search'),
    path('home/',home_view,name='home'),
    path('categeory/<int:id>',categeory,name='categeory'),
    path('cartdelete/<int:value>',DeleteFromCart,name='cartdelete'),
    path('address/add',GetAddressView.as_view(),name="addaddress"),
    path('thankyou',thankyou,name="thankyou"),
    path('favorites',FavoriteView.as_view(),name="favorite"),
    path('remfavorite/<int:value>',Rem_favorites,name='remfavorite'),
    path('orders/',OrdersView.as_view(),name='orders'),
    path('deleteorder/<int:value>',Order_delete,name='deleteorder'),
    path('addreview/<int:id>/',ReviewView,name='addreview'),
    path('about/',AboutView.as_view(template_name="about.html"),name='about')
]