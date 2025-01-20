from django.contrib import admin
from .models import Movie,Watchlist,Contact,SubscriptionPlan,UserSubscription

# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','name','mov_vi_ori','genre','description','re_year','rating','starcast','director','movie_image','video']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'films']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email' ,'message']


@admin.register(SubscriptionPlan)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'duration']


@admin.register(UserSubscription)
class UserscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'plan']
