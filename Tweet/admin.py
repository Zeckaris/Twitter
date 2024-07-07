from django.contrib import admin
from .models import Profile, Reply, Post,Mention,HashTag,Follow,Retweet,Like,DM
# Register your models here.
admin.site.register(Profile)
admin.site.register(Reply)
admin.site.register(Post)
admin.site.register(Mention)
admin.site.register(HashTag)
admin.site.register(Follow)
admin.site.register(Retweet)
admin.site.register(Like)
admin.site.register(DM)
