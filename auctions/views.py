from django.db.models.query import QuerySet
from django.http import request
from django.http.response import HttpResponse
from auctions.form import Createlistingform
import json
from django.db.models import Max
from json.encoder import JSONEncoder
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from datetime import date
from django.http import  HttpResponseRedirect, JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from datetime import date
from django.contrib.auth.decorators import login_required

from .models import *

def inWatchList(request, item:Item):
    inwatchlist=False
    if(request.user.is_authenticated):
        inwatchlist=Watchlist.objects.filter(user=request.user).filter(item=item).count()>0
    return inwatchlist

def inWatchListNum(view_func):
    def wrap(request:HttpRequest,*args,**kwargs):
        if not request.user.is_authenticated:
            res=view_func(request,*args,**kwargs,wlcount=None )
        else:
            wlcount=Watchlist.objects.filter(user=request.user).count()
            res=view_func(request,*args,**kwargs,wlcount=wlcount )
        return res
    return wrap

@inWatchListNum
def index(request,wlcount):
    return render(request, "auctions/index.html" , {'items':Item.objects.filter(is_active=True) , 'wlcount':wlcount})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@inWatchListNum
def categories_view(request,wlcount):
    categories=Category.objects.all()
    return render(request, "auctions/categories.html", {
                "categories": categories,
                'wlcount':wlcount
            })

@login_required
@inWatchListNum
def create_listing_view(request:HttpRequest,wlcount):
  
    if request.method=='GET':
        return render(request,'auctions/createlisting.html',{'form':Createlistingform().as_p(),'wlcount':wlcount})
    elif request.method=='POST':
        newListing=Createlistingform(request.POST)
        if newListing.is_valid():
            newListing=newListing.save(commit=False)
            newListing.created_by=request.user
            newListing.creation_time=date.today()
            newListing.current_price=newListing.initial_price
            newListing.save()
            return HttpResponseRedirect(reverse('item',args=[newListing.id]))

        else:
            return render(request,'auctions/createlisting.html',{'form':newListing ,'wlcount':wlcount})
            
            
@login_required
@inWatchListNum
def watchlist_view(request:HttpRequest,wlcount):
    
    if request.method=='GET':
        items = map(lambda wl:wl.item,Watchlist.objects.filter(user=request.user))
        return render(request, "auctions/watchlist.html", {
                    "items": items ,
                    'wlcount':wlcount              
                })
    elif request.method=='DELETE':
        print(json.loads(request.body))
        itemid=json.loads(request.body)['itemid']
        try:
            Watchlist.objects.get(user=request.user,item=itemid).delete()
            return JsonResponse({'success':True})
        except:
            return JsonResponse({'success':False})

@inWatchListNum
def category_view(request,category,wlcount):
    items=Item.objects.filter(category=category)
    return render(request, "auctions/category.html", {
                "category": category.capitalize(),
                "items": items,            
                'wlcount':wlcount    
            })
            


@inWatchListNum
def item_view(request:HttpRequest,itemid,wlcount):
    if(request.method=="GET"):
        item=Item()
        try:
            item=Item.objects.get(id=itemid)  
        except:
            return HttpResponse(status=404)
        comments=Comment.objects.filter(item=item)
        bids_count=Bid.objects.filter(item=item).count()
        owner_name=item.created_by.username

        return render(request, "auctions/item.html",{
            "item" : item,
            "inwatchlist" : inWatchList(request,item),
            "comments" : comments ,
            "bids_count" : bids_count ,
            "owner":owner_name.capitalize(),
            'wlcount':wlcount
            })
    
    elif(request.method=='POST'):
        item=Item.objects.filter(id=itemid)
        validItem=item.exists()
        item=item[0]
        validUser=request.user.is_authenticated
        response={}
        if not validUser:
            response['error']='Please login'
        elif not validItem:
            response['error']='invalid listing'
        else:
            Comment(commenter=request.user,item=item,comment=json.loads(request.body)['comment'],date=date.today()).save()
            response['success']='Done'
        return JsonResponse(response)
    
def addtowatchlist_view(request:HttpRequest,itemid):
    item=Item.objects.filter(id=itemid)
    validItem=item.exists()
    validUser=request.user.is_authenticated    
    item=item[0]
    response={}
    if not validUser:
        response['error']='Please login'
    elif not validItem:
        response['error']='invalid listing'
    elif Watchlist.objects.filter(user=request.user,item=item).count()>0:
        response['success']='already in watchlist'
    else:
        Watchlist(item=item,user=request.user).save()
        response['success']='added to watchlist'
    return JsonResponse(response)

    

def bid_view(request:HttpRequest,itemid):
    if request.method=="POST":
        try:
            bidvalue=float(json.loads(request.body)['bidvalue'])
        except:
            return JsonResponse({'error':'please enter a valid number'})
            
        item=Item.objects.filter(id=itemid)
        validItem=item.exists()
        validUser=request.user.is_authenticated

        item=item[0]
        response={}
        if not validUser:
            response['error']='Please login'
        elif not validItem:
            response['error']='invalid listing'
        elif item.current_price >= bidvalue:
            response['error']='Please increase your bid'
        elif item.created_by == request.user:
            response['error']="You Can't bid on your listing"
        else:
            Bid(item=item,user=request.user,price=bidvalue).save()
            item.current_price=bidvalue
            item.current_bid_user=request.user
            item.save() 
            response['success']='Done'
            response['value']=bidvalue
        return JsonResponse(response)

@login_required
@inWatchListNum
def mybids_view(request,wlcount):
    bids=Bid.objects.filter(user=request.user).values('item').annotate(maxp=Max('price'))
    maxbids=[]
    for bid in bids:
        maxbids.append(Bid.objects.get(user=request.user,item=bid['item'],price=bid['maxp']))
        
    return render(request,'auctions/bids.html',{'wlcount':wlcount,'bids' : maxbids})

@login_required
@inWatchListNum
def mylisting_view(request,wlcount):
    if request.method=='GET':
        items=Item.objects.filter(created_by=request.user).order_by('-is_active')
        return render(request,'auctions/mylistings.html',{'wlcount':wlcount,'items':items})
    elif request.method=='PUT':
        print('imhere')
        try:
            itemid=json.loads(request.body)['itemid']
            item=Item.objects.get(created_by=request.user,id=itemid)
            item.is_active=False
            item.save()
            return JsonResponse({'success':True})
        except:
            return JsonResponse({'success':False})


