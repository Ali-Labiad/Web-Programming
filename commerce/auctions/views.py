from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Auctionlist,Category,Watchlist,Comments,Bids
from datetime import date
from django.template.defaulttags import register
from django.contrib import messages
from django.db.models import Max

import itertools


from .models import User
from .forms import Listingform
from decimal import Decimal

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request):
    # Get the active list active=True
    auctionlists = Auctionlist.objects.filter(active=True)
    #Get watchlist of the given user
    watchlist_element = getwatchlist(request)
    return alllisting(request,auctionlists,watchlist_element)


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

@login_required
def create(request):
    #
    form = Listingform(request.POST or None)
    categories = Category.objects.all()
    watchlist_element = getwatchlist(request)
    #Get user data
    if request.method == 'POST' and form.is_valid:
        form = Listingform(request.POST)
        title_post = request.POST['title']
        description_post = request.POST['description']
        bid_post = request.POST['bid']
        url_post = request.POST['url']
        curent_date = date.today()
        active_post = True
        current_user = request.user
        category_post = Category.objects.filter(id=request.POST['categorie']).get()
        # Attempt to create new listing
        try:
            list = Auctionlist(title=title_post, description=description_post, bid=bid_post,url=url_post,date=curent_date,active=active_post,user=current_user,category=category_post)
            list.save()
        except Exception:
            return render(request, "auctions/create.html", {
                "message": "Error when saving",
                "categories" : categories, 
                "form" : Listingform(),
                "watchlistelement":len(watchlist_element) #refresh badge
            })
    
    return render(request, "auctions/create.html" , {
            "form" : Listingform(),
            "categories" : categories,
            "watchlistelement" : watchlist_element 
        })

def listing(request,listing_id):
    
    listing = Auctionlist.objects.get(pk=listing_id)
    numberofbids = len(Bids.objects.filter(auctionlist=listing).all())
    max_bid = Bids.objects.filter(auctionlist=listing).aggregate(Max('bid'))['bid__max']  
    if not max_bid or listing.bid > max_bid:
        currentprice = listing.bid
    else:
        currentprice = "{:10.2f}".format(float(max_bid))
    if not request.user.is_authenticated : 
        return render(request, "auctions/listing.html", {
        "listing" : listing,
        "currentprice" : currentprice,
        "numberofbids" : numberofbids
    })
    else:    
        watched = Watchlist.objects.filter(user=request.user.username).filter(auctionlist=listing).all()
        watchlist_element = getwatchlist(request)
        comments = Comments.objects.filter(auctionlist=listing).all()
        user_win = Bids.objects.filter(winner=True).filter(auctionlist=listing).filter(user=request.user)

        closelisting = False
        winner = False
        if listing.user == request.user:
            closelisting = True
        if listing.user != request.user and user_win :
            winner = True
        return render(request, "auctions/listing.html", {
            "listing" : listing, 
            "numberofbids" : numberofbids,
            "comments":comments,
            "currentprice" : currentprice,
            "watched" : watched,
            "watchlistelement" : len(watchlist_element),
            "closelisting" : closelisting,
            "winner":winner
        })

@login_required
def addcomment(request,listing_id):
    if request.method == 'POST':
        listing = Auctionlist.objects.get(pk=listing_id)
        if request.POST['newcomment'] :
            new_comment = request.POST['newcomment']
            curent_date = date.today()
            comm = Comments(comment=new_comment,date=curent_date,auctionlist=listing,user=request.user)
            comm.save()
    return HttpResponseRedirect(reverse("listing" , args=(listing.id,)))

@login_required
def addbid(request,listing_id):
    if request.method == 'POST':
        listing = Auctionlist.objects.get(pk=listing_id)
        bids=list(Bids.objects.filter(auctionlist=listing))
        max_bid = Bids.objects.filter(auctionlist=listing).aggregate(Max('bid'))['bid__max']
        
        if not max_bid :
            currentprice = listing.bid
        else:
            currentprice = max_bid

        if request.POST['amount'] and float(request.POST['amount']) != None:
            if request.user != listing.user and (Decimal(request.POST['amount']) <= currentprice or Decimal(request.POST['amount']) < listing.bid) :
                messages.success(request, "The bid must be at least as large as the starting bid, and must be greater than any other bids")
                return HttpResponseRedirect(reverse("listing" , args=(listing.id,)))
            current_bid = Decimal(request.POST['amount'])
            bid = Bids(bid=current_bid,user=request.user,auctionlist=listing)
            bid.save()
    return HttpResponseRedirect(reverse("listing" , args=(listing.id,)))

@login_required
def addwatchlist(request,listing_id):
    
    if request.method == 'POST':
        listing = Auctionlist.objects.get(pk=listing_id)
        watchlist = Watchlist.objects.filter(user=request.user.username).filter(auctionlist=listing).all()
        curent_date = date.today()
        if not watchlist :
            new_watchlist = Watchlist(date=curent_date,user=request.user.username,auctionlist=listing)
            new_watchlist.save()
        else:
            watchlist.delete()
    return HttpResponseRedirect(reverse("listing" , args=(listing.id,)))

@login_required
def watchlist(request):
    dic_active_listing={}
    watchlists = getwatchlist(request)
    for watchlist in watchlists :
         auctionlists = Auctionlist.objects.filter(active=True).filter(id=watchlist.auctionlist.id)
         dic_active_listing[watchlist.auctionlist.id] = auctionlists
    return render(request, "auctions/watchlist.html" , {
            "watchlists" : watchlists,
            "watchlistelement" : len(watchlists),
            "dic_active_listing" : dic_active_listing
        })

@login_required
def closelisting(request,listing_id):
    
    if request.method == 'POST':
        listing = Auctionlist.objects.get(pk=listing_id)
        max_bid = Bids.objects.filter(auctionlist=listing).aggregate(Max('bid'))['bid__max']
        bid_winner = Bids.objects.filter(auctionlist=listing).filter(bid=max_bid).first()
        if bid_winner:
            bid_winner.winner = True
            bid_winner.save()
        listing.active = False
        listing.save()

    return HttpResponseRedirect(reverse("index"))

def categorylist(request):
    categories = Category.objects.all()
    return render(request, "auctions/categorylist.html" , {
      "categories" : categories  
    })

def categorylisting(request,name):
    auctionlists = Auctionlist.objects.select_related('category').filter(category__name=name,active=True)
    return alllisting(request,auctionlists,[])
# Get all 
def alllisting(request,auctionlists,watchelment):
    dic_price={}
    for auction in auctionlists :
            bids=list(Bids.objects.filter(auctionlist=auction))
            if not bids:
                dic_price[auction.id] = auction.bid 
            else:
                setr = set(float(current_bid.bid) for current_bid in bids)
                setr.add(float(auction.bid))
                current_price = max(setr)
                dic_price[auction.id] = "{:10.2f}".format(current_price)
                
    return render(request, "auctions/index.html", {
            "auctionlist" : auctionlists,
            "dic_price" : dic_price,
            "watchlistelement" : len(watchelment)
    })

#Get watchlist for a given user if auctionlist is active
def getwatchlist(request):
    return Watchlist.objects.select_related('auctionlist').filter(user=request.user.username,auctionlist__active=True)




        