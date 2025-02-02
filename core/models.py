from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Movie(models.Model):


    CATEGORY_CHOICES = [
        ('CAROUSEL','Carousel'),
        ('TRENDING','Trending'),
        ('ANIME', 'Anime'),
        ('INDIAN', 'Indian'),
        ('WEBSERIES','Webseries'),
        ('HOLLYWOOD','Hollywood')
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    mov_vi_ori = models.CharField(max_length=100, default= 'Movie Vista Original')
    genre = models.CharField(max_length=100)
    description=models.TextField()
    re_year = models.IntegerField()
    imdb = models.CharField(max_length=20, default='IMDB')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    starcast = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    movie_image =models.ImageField(upload_to='movie_images')  
    video = models.FileField(upload_to='movie_videos')

    def __str__(self):
        return str(self.name)
    

##########################################################  watchlist   #######################################################################


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    films = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    

#########################################################  Contact(help) #################################################################

class Contact(models.Model):
    name = models.CharField(max_length=100, default='')
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    

####################################################### Subscription #################################################################

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    detail1 = models.CharField(max_length=200,default='')
    detail2 = models.CharField(max_length=200,default='')
    detail3 = models.CharField(max_length=200,default='')

    def _str_(self):
        return self.name

class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey('SubscriptionPlan', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'plan', 'is_active')