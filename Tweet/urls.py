from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('create_post/', views.create_post, name='create_post'),
    path('signup/',views.signup, name='signup'),
    path('logoutPage/',views.logout_page, name='logout'),
    path('loginPage/', views.login_page, name='login'),
    path('postTweet/', views.post_tweet, name='post'),
    path('likePost/<int:id>/', views.like_tweet, name='like'),
    path('retweetPost/<int:id>/', views.retweet_post, name='retweet'),
    path('deletePost/<int:id>/', views.delete_post, name='deletePost'),
    path('viewPost/<int:id>', views.view_post, name='viewPost'),
    path('replyPost/<int:id>', views.reply_to_post, name='reply'),
    path('replycursive/<int:id>/<int:pid>', views.reply_to_reply, name='rr'),
    path('sendDM/', views.send_DM , name='sendDm'),
    path('follow/', views.follow , name='follow'),
    path('viewProfile/<str:username>/', views.viewProfile, name='viewProfile'),
    path('query/', views.searchBar, name='query'),
    
]
