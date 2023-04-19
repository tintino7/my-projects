from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *

# give index page
def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all(),
        "auctions": Auction.objects.filter(highest_bid=True)
    })

# login page
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

# logout page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# new user register
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



# create new listing
@login_required(login_url='/login')
def create_new_listing(request):

    # if user request post
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        url = request.POST["url"]
        if url:

            new_listing = Listing(title=title, description=description, starting_bid=starting_bid, owner=request.user, image_url=url, category=request.POST["category"] )
            new_listing.save()
        else:
            new_listing = Listing(title=title, description=description, starting_bid=starting_bid, owner=request.user,category=request.POST["category"] )
            new_listing.save()

        get_to_auction = Auction(listing=new_listing, user=new_listing.owner, amount=new_listing.starting_bid)
        get_to_auction.save()
        return HttpResponseRedirect(reverse("index"))
    # if user request get
    else:
        categories = Listing.categories
        return render(request, "auctions/createNewListing.html",{
            "categories": categories
        })

# bidding on auction listing
@login_required(login_url='/login')
def listing(request, listing_id):
         
    # get listing
    item = Listing.objects.get(pk=listing_id)
    # current user
    current_user = request.user
    user_id = current_user.id

    # commends for this listing
    commands = Command.objects.filter(listing=listing_id)

    # total bids for this item
    total_bids = Auction.objects.filter(listing=listing_id)
    
    # in user watch list or not
    watch_list = WatchList.objects.filter(user=user_id, listing=listing_id)

    # get old high bid amount
    old_bid = Auction.objects.get(listing=item.id, highest_bid=True)
    new_bid_amount = request.POST["bid"]

    if old_bid.user.id == request.user.id:
        new_message = "Your bid is current bid"
    else:
        new_message = " "
    
    # new bid lower than old bid
    if old_bid.amount >= int(new_bid_amount):

        high = old_bid.amount
        return render(request,"auctions/listing.html",{
            "items": item,
            "commands": commands,
            "highest_bid": high,
            "watchlist": watch_list,
            "total_bids": len(total_bids),
            "message":"The new bid amount should be greater than the old bid",
            "new_message": new_message,
            "winner":old_bid
        
        })
    # valid bid amount
    else:
        old_bid.highest_bid = False
        old_bid.save()
        new_bid = Auction(listing=item, user=request.user, amount=new_bid_amount)
        new_bid.save()
        if new_bid.user.id == request.user.id:
            new_message = "Your bid is current bid"
        else:
            new_message = " "
            
        high = new_bid_amount

        
        return render(request,"auctions/listing.html",{
            "items": item,
            "commands": commands,
            "highest_bid": high,
            "watchlist": watch_list,
            "total_bids": len(total_bids),
            "new_message": new_message,
            "winner": new_bid
        })


# get listing page
def get_listing(request,listing_id):
    
    item = Listing.objects.get(pk=listing_id)
    current_user = request.user
    user_id = current_user.id
    commands = Command.objects.filter(listing=listing_id)
    highest_bid = Auction.objects.filter(listing=listing_id, highest_bid=True)
    if highest_bid[0].user.id == request.user.id:
        new_message = "Your bid is current bid"
    else:
        new_message = " "

    total_bids = Auction.objects.filter(listing=listing_id)

    if highest_bid:
        high = highest_bid[0].amount
    else:
        high = item.starting_bid

    watch_list = WatchList.objects.filter(user=user_id, listing=listing_id)
    
    
    return render(request, "auctions/listing.html",{
        "items": item,
        "commands": commands,
        "highest_bid": high,
        "watchlist": watch_list,
        "total_bids": len(total_bids),
        "new_message": new_message,
        "winner": highest_bid[0]

        
    })





# comment on listing
@login_required(login_url='/login')
def commend(request, listing_id):
    commend = request.POST["commend"]
    if commend:
        item = Listing.objects.get(pk=listing_id)
        user = User.objects.get(pk=request.user.id)
        new_commend = Command(command=commend, listing=item, user=user)
        new_commend.save()
        return HttpResponseRedirect(reverse("get_listing" ,args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("get_listing" ,args=(listing_id,)))


# add to watchlist
@login_required(login_url='/login')
def add_watchlist(request, listing_id):
    watch_list = WatchList(listing=Listing.objects.get(pk=listing_id), user=User.objects.get(pk=request.user.id))
    watch_list.save()
    return HttpResponseRedirect(reverse("get_listing", args=(listing_id,)))
    

# remove from watchlist
@login_required(login_url='/login')
def remove_watchlist(request, listing_id):
    watch_list = WatchList.objects.get(listing=listing_id, user=request.user.id)
    watch_list.delete()
    return HttpResponseRedirect(reverse("get_listing", args=(listing_id,)))


# if owner close bid
@login_required(login_url='/login')
def close_bid(request, listing_id):
    item = Listing.objects.get(pk=listing_id)
    item.active = False
    item.save()

    return HttpResponseRedirect(reverse("get_listing", args=(listing_id,)))

# watch list page
def watchlist(request):
    # get current user
    user = request.user

    # get current user's watchlist from watch list model
    watch_listed = WatchList.objects.filter(user=request.user.id)
    return render (request, "auctions/watchlist.html",{
        "watchlist": watch_listed
    })

# get categories page
def categories(request):
    categories = Listing.categories
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

# view every listing on category page
def category(request, category):
    listing_category = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html",{
        "category": listing_category,
        "auctions": Auction.objects.filter(highest_bid=True),
        "type": category

    })