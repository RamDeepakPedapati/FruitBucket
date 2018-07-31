import django,os,sys
from requests import request

os.environ['DJANGO_SETTINGS_MODULE']="dummy.settings"
django.setup()



from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'about.html'