from django.db import models
from django.contrib.auth.models import User
import re

# Create your models here.

class Profile(models.Model):
    user=                   models.OneToOneField(User,on_delete=models.CASCADE , blank=False, null=False, related_name='user_profile')
    bio=                    models.CharField(verbose_name='Biography', blank=True , null= True, max_length=100)

    
    profile_image =         models.ImageField(upload_to='profile_images/',blank=True, null= True )    
    
    def __str__(self):
        return self.user.username 
    
class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='following_set', on_delete=models.CASCADE)
    followed = models.ForeignKey(Profile, related_name='follower_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
    
   
class HashTag(models.Model):
    title=                  models.CharField(max_length=30, unique=True)
    
class Post(models.Model):
    body=                   models.TextField(max_length=500, blank=False, null=False)
    created=                models.DateTimeField(auto_now=True)
    author=                 models.ForeignKey(Profile,related_name='posts', on_delete=models.CASCADE, blank=False, null=False)
    hashtags=               models.ManyToManyField(HashTag,related_name='posts' ,blank=True)
    def __str__(self):
        return f'{self.author.user.username}  \n {self.body[:50]}'   
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Extract hashtags from the body text
        hashtags_list = re.findall(r'#\w+', self.body)

        # Associate each hashtag with the post
        for tag in hashtags_list:
            tag_filtered = tag[1:]  # Remove the leading '#'
            hashtag, created = HashTag.objects.get_or_create(title=tag_filtered)
            self.hashtags.add(hashtag)

     
class Reply(models.Model):
    parentPost=             models.ForeignKey(Post,related_name='child_post', on_delete=models.CASCADE , blank=False, null=False)
    parentReply=            models.ForeignKey('self',related_name='reply_to_reply', on_delete=models.CASCADE,blank=True, null=True)
    author =                models.ForeignKey(Profile, on_delete=models.CASCADE)
    content =               models.TextField(max_length=200)
    created_at =            models.DateTimeField(auto_now_add=True)
    hashtags=               models.ManyToManyField(HashTag,related_name='replies' ,blank=True)
    
    def __str__(self):
        return f'Replied to:{self.parentPost.author.user.username} \n {self.content[:50]}'
    
    
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        hashtags_list= re.findall(r'#\w', self.content)
        for tag in hashtags_list:
            tag_filtered=tag[1:]
            hashtag, created= Reply.objects.get_or_create(tag_filtered)
            self.hashtags.add(hashtag)
            
            

    
class Mention(models.Model):
    post=                   models.ForeignKey(Post, related_name='mentioned_users', on_delete=models.CASCADE, blank=False, null=False)
    mentionedUser=          models.ForeignKey(Profile, related_name='mentions', on_delete=models.CASCADE, blank=False, null=False)

class Like(models.Model):
    post=                   models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    profile=                models.ForeignKey(Profile, related_name='liked_post', on_delete=models.CASCADE)
    
class Retweet(models.Model):
    post=                   models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_retweets')
    profile=                models.ForeignKey(Profile, related_name='retweeted_post', on_delete=models.CASCADE)
    
class DM(models.Model):
    sender=                 models.ForeignKey(Profile,related_name='dms_sent', on_delete=models.CASCADE)
    receiver=               models.ForeignKey(Profile,related_name='dms_received', on_delete=models.CASCADE)
    body=                   models.TextField(max_length=1000)
    created=                models.DateTimeField(auto_now=True)
    
