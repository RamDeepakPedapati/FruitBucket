import django,os,sys
from django.contrib.auth import logout
from django.db.models import Count
from django import forms
os.environ['DJANGO_SETTINGS_MODULE']="dummy.settings"
django.setup()
from fruitapp.models import *
from django.shortcuts import render, redirect, loader, get_object_or_404
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView



class CardView(ListView):
    model = Cart
    template_name = 'mycart.html'
    context_object_name = 'carts'
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(CardView, self).get_context_data(**kwargs)
        cart = Cart.objects.values('count','product').filter(user=self.request.user)

        carts = list(Cart.objects.filter(user=self.request.user).values_list('product',flat=True))
        context.update({'carts': cart})
        products=Product.objects.filter(id__in=carts)

        total=0
        for i in range(len(cart)):
            total=total+(cart[i]['count'])*(products[i].price)


        mylist = zip(products, cart)

        context.update({'products':mylist})
        context.update({'total':total})
        return context



def Add_to_cart(request,value):
    c_object=Cart.objects.filter(user=request.user,product=value)
    if not request.user.is_authenticated:
        return redirect("fruitapp:login")
    if list(c_object)==[]:
        c_object = Cart(user=request.user, product=Product.objects.get(id=value),count=1)
        c_object.save()
    else:
        count= c_object[0].count+1
        Cart.objects.filter(user=request.user,product=Product.objects.get(id=value)).update(count=count)
        # c_object.save()
    return redirect("fruitapp:products")





def Update_cart(request,value):
    c_object=Cart.objects.filter(user=request.user,product=value)
    if not request.user.is_authenticated:
        return redirect("fruitapp:login")
    if list(c_object)==[]:
        c_object = Cart(user=request.user, product=Product.objects.get(id=value),count=1)
        c_object.save()
    else:
        count= c_object[0].count+1
        Cart.objects.filter(user=request.user,product=Product.objects.get(id=value)).update(count=count)
    return redirect("fruitapp:cart")



def decrease_count(request,value):
    c_object=Cart.objects.filter(user=request.user,product=value)
    if not request.user.is_authenticated:
        return redirect("fruitapp:login")
    if c_object[0].count==1:
        c_object = Cart.objects.filter(product=value).delete()
        # c_object = Cart(user=request.user, product=Product.objects.get(id=value),count=1)
        # c_object.save()
    else:
        count= c_object[0].count-1
        Cart.objects.filter(user=request.user,product=Product.objects.get(id=value)).update(count=count)
    return redirect("fruitapp:cart")



def DeleteFromCart(request,value):
    c_object=Cart.objects.filter(product=value).delete()
    return redirect("fruitapp:cart")
