import django,os,sys
from django.contrib.auth import logout
from django.db.models import Count
from django import forms
os.environ['DJANGO_SETTINGS_MODULE']="dummy.settings"
django.setup()
from fruitapp.models import *
from django.shortcuts import render, redirect, loader, get_object_or_404
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView
from django.views import View
from django.urls import reverse_lazy


class AddressForm(forms.Form):
    address = forms.CharField(
        max_length=2048,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'})
    )
    cityname= forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City Name'})
    )

    pincode= forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'})
    )



class GetAddressView(View):

    def get(self,request):
        form = AddressForm()
        return render(request,template_name='addressform.html',context={'form':form,'title':'Signup | Online App'})

    def post(self,request):
        form =AddressForm(request.POST)
        instance=dict()
        instance['address'] = form.data['address']
        instance['cityname'] = form.data['cityname']
        instance['pincode'] = form.data['pincode']
        instance['user'] = self.request.user

        if form.is_valid():
            order= Order(**instance)
            order.save()
            added = Cart.objects.filter(user=request.user)
            for i in added:
                each=each_order(count=i.count,product=i.product,order=order)
                each.save()
            order.save()
            added = Cart.objects.filter(user=request.user).delete()
        return redirect('fruitapp:thankyou')
        # return render(redirect,template_name='thankyou.html',context={'form':form,'title':'Signup | Fruit App'})





def thankyou(request):
    return render(request, 'thankyou.html')



class OrdersView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        orders= list(Order.objects.filter(user=self.request.user))

        stringlist=[]
        for i in orders:
            products = []
            products.append(each_order.objects.filter(order=i))

            str=''
            for j in products[-1]:
                str=str+'  '+j.product.name

            stringlist.append({'products':str})
        mylist = zip(stringlist,orders)
        context.update({'products': mylist})

        return context



def Order_delete(request,value):
    if not request.user.is_authenticated:
        return redirect("fruitapp:login")
    c_object = Order.objects.filter(id=value)
    c_object.delete()
    return redirect("fruitapp:orders")