from django.contrib.auth import models
from django.core import validators
from django.core.exceptions import ValidationError
from .models import Item
from django.forms import models, widgets

class Createlistingform(models.ModelForm):
    class Meta:
        model=Item
        fields=['category','image_url','title','description','initial_price']
        widgets={'description': widgets.Textarea(attrs={'cols': 80, 'rows': 20 ,'class':'form-control'}),
                'category':widgets.Select(attrs={'class':"form-control form-control-sm"}),
                'image_url':widgets.TextInput(attrs={'class':"form-control" ,'required':False ,'placeholder':"Image Url ..." }),
                'title':widgets.TextInput(attrs={'class':"form-control"  ,'placeholder':"Title ..."}),
                'initial_price':widgets.NumberInput(attrs={'class':"form-control"  ,'placeholder':"price ..."}),
                }