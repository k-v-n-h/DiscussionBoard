from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

class Post(models.Model):
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE) #on_delete here means that if a user is deleted all the posts the user created will be deleted too
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null = True)
    
    def publish(self): # this function is to save a post to be able to publish later.
        self.published_date = timezone.now
        self.save()
        
    def __str__(self):
        return self.title + ' || posted by: ' + str(self.author)

class Comment(models.Model): # each comment related to a post each comment and post to an author 
    post = models.ForeignKey('discussboard.Post', on_delete = models.CASCADE, related_name='comments') # on_delete means when main post is deleted all comments will be deleted also
    author = models.CharField(max_length = 200)
    created_date = models.DateTimeField(default = timezone.now)
    text = models.TextField()
    liked = models.ManyToManyField('auth.user', default=None, blank=True, related_name='liked')

    class Meta:
        # sort comments in chronological order by default
        ordering = ('created_date',)
        


    def __str__(self):
        return str(self.text)
    
    @property
    def NumberOfLikes(self):
        return self.liked.all().count

likeChoices  = {
    ('like', 'like'),
    ('unlike', 'unlike'),
 }

class LikedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.CharField(choices=likeChoices, default='like', max_length=10)

    def __str__(self):
        return str(self.comment)