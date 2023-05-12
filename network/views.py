from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def index(request):
    if request.method == "POST":

        # Get content 
        content = request.POST["content"]
        post = Post(user=request.user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:

        # get all posts from database and order them reverse chronological
        post = Post.objects.all().order_by('-date_time')
        posts = Paginator(post,10)
        page = posts.page(1)
        return render(request, "network/index.html",{
            "posts": page,
            "num_pages": range(1,posts.num_pages),
            "previous_page": -1,
            "next_page": 1,
            "total_pages": posts.num_pages

        })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        # create follow object when user register
        follow = Follow(user=user)
        follow.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request):
    if request.method == "POST":
        pass

    else:
        # Get user
        user = User.objects.get(username=request.user.username)
        # Get user's posts
        post = Post.objects.filter(user=user).order_by('-date_time')
        # Get user's follow information
        follow = Follow.objects.get(user=user)

        #pagination
        posts = Paginator(post,10)

        page = posts.page(1)
        return render(request, "network/profile.html",{
            "useris": user,
            "posts": page,
            "follow": follow,
            "num_pages": range(1,posts.num_pages),
            "previous_page": -1,
            "next_page": 1,
            "total_pages": posts.num_pages

        })


def following(request):
    # Get user
    user = User.objects.get(username=request.user.username)
    # Get user's following
    follow = Follow.objects.get(user=user)
    post = Post.objects.filter(user__in=follow.following.all()).order_by('-date_time')

    posts = Paginator(post,10)

    # current page info
    page = posts.page(1)
    return render(request, "network/follow.html",{
        "posts": page,
        "num_pages": range(1,posts.num_pages),
        "previous_page": -1,
        "next_page": 1,
        "total_pages": posts.num_pages
    })


def page(request, page_id, page_name):
    if page_name == "index":
        # get all posts from database and order them reverse chronological
        post = Post.objects.all().order_by('-date_time')

        # every page only show 10 posts
        posts = Paginator(post,10)

        
        page = posts.page(int(page_id) + 1)
        return render(request, "network/index.html",{
            "posts": page,
            "num_pages": range(1,posts.num_pages),
            "previous_page": int(page_id)-1,
            "next_page": int(page_id)+1,
            "total_pages": posts.num_pages
        })

    elif page_name == "profile":
        # Get user
        user = User.objects.get(username=request.user.username)
        # Get user's posts
        post = Post.objects.filter(user=user)
        # Get user's follow information
        follow = Follow.objects.get(user=user)

        #pagination
        posts = Paginator(post,10)

        page = posts.page(int(page_id) + 1)

        return render(request, "network/profile.html",{
            "user": user,
            "posts": page,
            "follow": follow,
            "num_pages": range(1,posts.num_pages),
            "previous_page": int(page_id)-1,
            "next_page": int(page_id)+1,
            "total_pages": posts.num_pages
        })

    else:
        # Get user
        user = User.objects.get(username=request.user.username)
        # Get user's following
        follow = Follow.objects.get(user=user)
        post = Post.objects.filter(user__in=follow.following.all())

        posts = Paginator(post,10)

        # current page info
        page = posts.page(1)
        return render(request, "network/follow.html",{
            "posts": page,
            "num_pages": range(1,posts.num_pages),
            "previous_page": -1,
            "next_page": 1,
            "total_pages": posts.num_pages
        })


def user(request, user_name):

    if request.method == "POST":
        action = request.POST["follow"]

        # current user
        current_user = Follow.objects.get(user=request.user)
        # the user want to follow or unfollow
        user = Follow.objects.get(user=User.objects.get(username=user_name))
        
        # do respect to action
        if action == "follow":
            current_user.following.add(User.objects.get(username=user_name))
            user.followers.add(request.user)
        elif action == "unfollow":
            current_user.following.remove(User.objects.get(username=user_name))
            user.followers.remove(request.user)
            
        # save changes
        current_user.save()
        user.save()
        return HttpResponseRedirect(reverse('user', args=(user_name,)))
        
        
    else:
        # Get user
        user = User.objects.get(username=user_name)
        # Get user's posts
        post = Post.objects.filter(user=user).order_by('-date_time')
        # Get user's follow information
        follow = Follow.objects.get(user=user)
        

        #pagination
        posts = Paginator(post,10)

        page = posts.page(1)
        return render(request, "network/profile.html",{
            "useris": user,
            "posts": page,
            "follow": follow,
            "num_pages": range(1,posts.num_pages),
            "previous_page": -1,
            "next_page": 1,
            "total_pages": posts.num_pages
            
        })

@csrf_exempt
def edit_post(request):
    if request.method == "PUT":

        # Get data
        data = json.loads(request.body)
        post_id = data.get("post_id")
        content = data.get("content")

        # check for invalid id
        try:
            post = Post.objects.get(pk=int(post_id))
        except Post.DoesNotExist: 
            return JsonResponse({"status": "unsuccess"}, status=200)

        # for valid request
        if post.user == request.user:
            post.content = content
            post.save()
            return JsonResponse({"status": "success"}, status=200)

        # for invalid request
        else:
            return JsonResponse({"status": "unsuccess"}, status=200)


@csrf_exempt
def like(request):
    if request.method == 'PUT':

        data = json.loads(request.body)
        action = data.get("action")
        post_id = int(data.get("post_id"))

        # check for invalid id
        try:
            post = Post.objects.get(pk=int(post_id))
        except Post.DoesNotExist: 
            return JsonResponse({"status": "unsuccess"}, status=200)

        if action == "unlike":
            post.like.remove(request.user)
        elif action == "like":
            post.like.add(request.user)

        return JsonResponse({"status": "success"}, status=200)