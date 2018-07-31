import django,os,sys
from django.forms import ModelForm
from django.forms import *

os.environ['DJANGO_SETTINGS_MODULE']="dummy.settings"
django.setup()
from fruitapp.models import *
from django.shortcuts import render, redirect, loader, get_object_or_404
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView
from django.views import View


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context=super(ProductListView,self).get_context_data(**kwargs)
        added=[]
        favorites=[]
        if self.request.user.is_authenticated:
            added=Cart.objects.filter(user=self.request.user)
            favorites=Favourite.objects.filter(user=self.request.user)
        else:
            return redirect("fruitapp:login")
        lis=[]
        for j in context["products"]:
            flag=0
            for i in added:
                if i.product_id == j.id:
                    lis.append({"added":1})
                    flag=1
            if flag==0:
                lis.append({"added":0})

        list1 = []
        for j in context["products"]:
            flag = 0
            for i in favorites:
                if i.product_id == j.id:
                    list1.append({"favorite":1})
                    flag = 1
            if flag == 0:
                list1.append({"favorite":0})

        mylist = zip(context["products"], lis,list1)
        context.update({'products': mylist})
        return context





def Search_func(request):
    item=request.GET['query']
    product=list(Product.objects.values_list())
    products=[]
    for i in range(len(product)):
        if item.lower() in (product[i][1]).lower():
            products.append(product[i][1])
    product = Product.objects.filter(name__in=products)


    favorites=[]
    added=[]
    if request.user.is_authenticated:
        added = Cart.objects.filter(user=request.user)
        favorites = Favourite.objects.filter(user=request.user)

    lis = []
    for j in product:
        flag = 0
        for i in added:
            if i.product_id == j.id:
                lis.append(1)
                flag = 1
        if flag == 0:
            lis.append(0)

    list1 = []
    for j in product:
        flag = 0
        for i in favorites:
            if i.product_id == j.id:
                list1.append(1)
                flag = 1
        if flag == 0:
            list1.append(0)




    return render(request,"productfilter.html",{'products': product},lis)



def productDetail(request,id):

    product = Product.objects.filter(id=id)
    rating=RateandReview.objects.filter(product=id)

    return render(request,"productDetail.html", context={'products':product,'rating':rating})



def categeory(request,id):
    product = Product.objects.filter(categeory=id)
    return render(request, "productfilter.html", {'products': product})




def home_view(request):
    c=Categeory.objects.all()
    return render(request,"categeories.html",{'categeories':c})




class AddReview(ModelForm):
    class Meta:
        model=RateandReview
        exclude={'id'}
        widgets={
            'review':Textarea(attrs={'class':'form-control','placeholder':'Review the product'}),
            'rating':DecimalField(),
        }


def ReviewView(request,id):
    str=request.POST['review']
    rate=request.POST['rating']
    product=Product.objects.filter(id=id)[0]
    rate=RateandReview(product=product,user=request.user,review=str,rating=rate)

    rate.save()
    return redirect("fruitapp:product", id)
