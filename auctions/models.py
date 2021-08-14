from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

class Category(models.Model):
    category_name=CharField(max_length=32,primary_key=True)
    def __str__(self) -> str:
        return self.category_name
class User(AbstractUser):
    pass    

class Item(models.Model):
   created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='item_creator')
   category=models.ForeignKey(Category,on_delete=CASCADE)
   creation_time=models.DateField()
   image_url=models.CharField(max_length=1024,null=True,blank=True)
   title=models.CharField(max_length=128)
   description=models.CharField(max_length=2048)
   initial_price=models.FloatField(validators=[MinValueValidator(0)])
   is_active=models.BooleanField(default=True)
   current_price=models.FloatField(validators=[MinValueValidator(0)])
   current_bid_user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True, related_name='highest_bid')
   def __str__(self) -> str:
       return self.title

class Bid(models.Model):
    user=models.ForeignKey(User,related_name='user_bid',on_delete=CASCADE)
    item=models.ForeignKey(Item,related_name='item_bid',on_delete=CASCADE)
    price=models.FloatField(validators=[MinValueValidator(0)])
    def __str__(self) -> str:
       return f"{self.user} bid with price :{self.price} on item {self.item} "
 
 
class Comment(models.Model):
    item=models.ForeignKey(Item,on_delete=CASCADE)
    commenter=models.ForeignKey(User,on_delete=CASCADE)
    date=models.DateField()
    comment=CharField(max_length=512)

class Watchlist(models.Model):
   user=models.ForeignKey(User,related_name='watchlist_user' ,on_delete=CASCADE)
   item=models.ForeignKey(Item,related_name='watchlist_item' ,on_delete=CASCADE)
