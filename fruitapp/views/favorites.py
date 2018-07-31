import django,os,sys
from django.contrib.auth import logout
from django.db.models import Count
from django import forms
os.environ['DJANGO_SETTINGS_MODULE']="dummy.settings"
django.setup()
from fruitapp.models import *
from django.shortcuts import render, redirect, loader, get_object_or_404
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView


def Add_to_favorites(request,value):
    c_object=Favourite.objects.filter(user=request.user,product=value)
    if not request.user.is_authenticated:
        return redirect("fruitapp:login")
    if list(c_object)==[]:
        c_object = Favourite(user=request.user, product=Product.objects.get(id=value))
        c_object.save()
    return redirect("fruitapp:products")


def Remove_favorites(request,value):
    if not request.user.is_authenticated:
        return redirect("fruitapp:login")

    c_object = Favourite.objects.filter(product=value)
    c_object.delete()
    return redirect("fruitapp:products")


def Rem_favorites(request,value):
    if not request.user.is_authenticated:
        return redirect("fruitapp:login")
    c_object = Favourite.objects.filter(product=value)
    c_object.delete()
    return redirect("fruitapp:favorite")



class FavoriteView(ListView):
    model = Cart
    template_name = 'favorites.html'
    context_object_name = 'carts'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(FavoriteView, self).get_context_data(**kwargs)
        # favorite=list(Favourite.objects.filter(user=self.request.user))
        # cart = Cart.objects.values('count','product').filter(user=self.request.user)
        favorite= list(Favourite.objects.filter(user=self.request.user).values_list('product',flat=True))
        # context.update({'carts': cart})

        products=Product.objects.filter(id__in=favorite)
        context.update({'products':products})
        return context
