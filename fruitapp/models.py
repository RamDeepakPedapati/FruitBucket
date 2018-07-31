from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categeory(models.Model):
    name=models.CharField(max_length=128)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=128)
    description=models.CharField(max_length=128)
    price = models.DecimalField(max_digits=20,decimal_places=2)
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    image=models.ImageField(upload_to='documents/',blank=True,null=True)
    categeory=models.ForeignKey(Categeory,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class User_info(models.Model):
    email=models.CharField(max_length=128)
    user= models.OneToOneField(User, on_delete=models.CASCADE)


class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    count=models.IntegerField()

class Favourite(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)


class RateandReview(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rating=models.DecimalField(max_digits=4,decimal_places=2,default=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review=models.TextField(max_length=5000)



class Checkouts(models.Model):
    houseno=models.CharField(max_length=128,null=True)
    appartment=models.CharField(max_length=128,null=True)
    cityname=models.CharField(max_length=128,null=True)
    pincode=models.CharField(max_length=128)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.TextField(max_length=2048)
    cityname = models.CharField(max_length=128, null=True)
    pincode = models.CharField(max_length=128)

class each_order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    count = models.IntegerField()


