import django,os,sys
os.environ['DJANGO_SETTINGS_MODULE']="dummy.settings"
django.setup()
from fruitapp.models import *
from django.shortcuts import render, redirect, loader, get_object_or_404

def userprofile(request):
    user=request.user
    user_obj=User.objects.values('first_name','last_name','username').filter(id=user.id)
    user_info_obj=User_info.objects.values().filter(user=user)
    return render(request,"UserProfile.html",{'user_info_obj': user_info_obj,'user_obj': user_obj})

