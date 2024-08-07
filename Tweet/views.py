from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from .forms import CustomUserCreationForm
from django.urls import reverse
from .models import Profile, Reply, Post,Mention,HashTag,Follow,Retweet,Like,DM
from django.contrib.auth.models import User
from django.contrib.auth import logout, login,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm, ReplyForm,SearchQueryForm
from django.db.models import Count, Q
import re


from django.shortcuts import render, redirect
from django.db.models import Q, Count
from .forms import PostForm, SearchQueryForm
from .models import Post, Profile,Follow

def home(request):
    tweets = None
    trends = HashTag.objects.annotate(tweet_count=Count('posts')).order_by('-tweet_count')[:10]
    search_form = SearchQueryForm(request.GET)
    
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user = None
    else:
        user = None

   

    hashtag = request.GET.get('hashtag')
    if hashtag:
        tweets = Post.objects.filter(
            hashtags__title=hashtag
        ).distinct().annotate(
            num_retweets=Count('post_retweets', distinct=True),
            num_likes=Count('post_likes', distinct=True)
        ).order_by('-created')
    else:
        if user:
            tweets = Post.objects.annotate(
                num_retweets=Count('post_retweets', distinct=True),
                num_likes=Count('post_likes', distinct=True)
            ).order_by('-created')

    context = {'tweets': tweets,'user': user,'trends': trends,'search_form': search_form,'selected_hashtag': hashtag}
    return render(request, 'Tweet/home.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = Profile.objects.get(user=request.user)
            post.save()
            return redirect('home')
    return redirect('home')



def signup(request):
    page = 'signup'
    if request.method == 'GET':
        form = CustomUserCreationForm()
        context = {'form': form, 'page': page}
        return render(request, 'Tweet/signup.html', context)
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username'].lower()
            user.save()
            login(request, user)

            Profile.objects.create(
                user=user,
                bio=form.cleaned_data.get('bio', ''),
                profile_image=form.cleaned_data.get('profile_image', None),
                coverPicture=form.cleaned_data.get('cover_picture', None)
            )
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
            context = {'form': form, 'page': page}
            return render(request, 'Tweet/signup.html', context)
        
        
        
        
@login_required
def logout_page(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')
    
def login_page(request):
    page='login'
    if request.method == 'GET':
        context={'page':page}
        return render(request, 'Tweet/signup.html', context)
    
    if request.method == 'POST':
        context={'page':page}
        username=request.POST.get('username')
        password= request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist")
            return redirect('login')
            
        user= authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password invalid')
        return render(request, 'Tweet/signup.html', context)
    
@login_required
def post_tweet(request):
    if request.method == 'GET':
        form= PostForm(request.GET)
        if form.is_valid():
            profile=request.user.user_profile
            post=Post.objects.create(
                body = form.cleaned_data['body'],
                author=profile
            )
            post.save()
            return redirect('home')
        
    
    
    
    
    
@login_required
def like_tweet(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=id)
        profile = request.user.user_profile
        liked_previously = Like.objects.filter(post=post, profile=profile).first()

        if liked_previously:
            liked_previously.delete()
        else:
            Like.objects.create(
                post=post,
                profile=profile
            )
        return redirect('home') 
    else:
        return JsonResponse({'error': 'Invalid method'})

@login_required
def retweet_post(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=id)
        profile = request.user.user_profile
        retweeted_previously = Retweet.objects.filter(post=post, profile=profile).first()

        if retweeted_previously:
            retweeted_previously.delete()
        else:
            Retweet.objects.create(
                post=post,
                profile=profile
            )
        return redirect('home')  
    else:
        return JsonResponse({'error': 'Invalid method'})


@login_required
def delete_post(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=id)
        if request.user.user_profile == post.author:
            post.delete()
        return redirect('home') 
    else:
        return JsonResponse({'error': 'Invalid method'})



    
    
    
@login_required   
def reply_to_post(request,id):
    if request.method == 'POST':
        replyform= ReplyForm(request.POST)
        if replyform.is_valid():
            profile= request.user.user_profile
            post= Post.objects.get(pk=id)
            reply=Reply.objects.create(
                parentPost=post,
                author=profile,
                content=replyform.cleaned_data['content']
            )
            return redirect('viewPost',id=id)

@login_required        
def reply_to_reply(request,id,pid):
    if request.method == 'POST':
        replyform=ReplyForm(request.POST)
        if replyform.is_valid():
            parentreply= Reply.objects.get(pk=id)
            profile=request.user.user_profile
            parentpost= Post.objects.get(id=pid)
            Reply.objects.create(
                parentPost=parentpost,
                parentReply=parentreply,
                author=profile,
                content=replyform.cleaned_data['content']
            )
            return redirect('viewPost',id=pid)
            
@login_required            
def view_post(request,id):
    if request.method == 'GET':
        replyform=ReplyForm()
        post= Post.objects.filter(pk=id).annotate(num_likes=Count('post_likes', distinct=True), num_retweets=Count('post_retweets', distinct=True)).first()
        replies=Reply.objects.filter(parentPost=post)
        context={'post':post, 'replies':replies,'replyform':replyform}
        return render(request, 'TWeet/post.html', context)
            
@login_required             
def send_DM(request):
    
    if request.method== 'GET':
        qry=request.GET.get('query')
        if qry is not None:
            query=User.objects.filter(Q(user=qry)).order_by('-created')[:3]
            context= {'query':query}
            return render(request, 'Tweet/dm.html', context)
        sender=Profile.objects.get(user=request.user)
        messages=DM.objects.filter(Q(sender= sender))
        context={'messages':messages}
        return render (request,'Tweet/dm.html',context )
    
    if request.method == 'POST':
        sender=Profile.objects.get(user=request.user)
        username=request.POST.get('username')
        try:
            user=User.objects.get(username=username)
            profile=Profile.objects.get(user=user)
        except:
            raise ValidationError('Username not found')
        if sender is not profile:
            content= request.POST.get('message')
            DM.objects.create(
                sender=sender,
                receiver=profile,
                body=content
            )
        else:
            raise ValidationError('You can not dm your self')
        return redirect('sendDm')
  
        
def follow(request):
    if request.method == 'GET':
        query = request.GET.get('username', '')
        usernameList = Profile.objects.filter(Q(user__username__icontains=query))
        return render(request, 'Tweet/home.html', {'profileList': usernameList})

    elif request.method == 'POST':
        followerProfile = Profile.objects.get(user=request.user)
        personality = request.POST.get('personality')
        try:
            profile = Profile.objects.get(user__username=personality)
        except Profile.DoesNotExist:
            raise ValidationError('The provided user does not exist')

        Follow.objects.create(
            follower=followerProfile, 
            followed=profile
        )
        return redirect('profile', username=personality)
    
    
    
    
def viewProfile(request,username):
    if request.method == 'GET':
        userProfile = get_object_or_404(Profile, user__username=username)
        tweets = Post.objects.filter(author=userProfile)
        likedTweets = Post.objects.filter(post_likes__profile=userProfile)
        retweetedPosts = Post.objects.filter(post_retweets__profile=userProfile)
        context = {'userProfile': userProfile,'tweets': tweets,'likedTweets': likedTweets,'retweetedPosts': retweetedPosts,}

        return render(request, 'Tweet/profile.html', context)

    

def searchBar(request):
    search_form = SearchQueryForm(request.GET)
    tweets = Post.objects.none()

    if request.method == 'GET' and search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query', '')
        print(f"Search query: {search_query}")  
        
        if search_query:
            tweets = Post.objects.filter(
                Q(author__user__username__icontains=search_query) |
                Q(hashtags__title__icontains=search_query) |
                Q(body__icontains=search_query)
            ).distinct().annotate(
                num_retweets=Count('post_retweets', distinct=True),
                num_likes=Count('post_likes', distinct=True)
            ).order_by('-created')
            print(f"SQL Query: {str(tweets.query)}")  

    return render(request, 'Tweet/home.html', {'tweets': tweets})





   
        