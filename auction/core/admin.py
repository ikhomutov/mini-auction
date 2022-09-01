from django.contrib import admin

from . import models


@admin.register(models.UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')



@admin.register(models.Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'owner',)


@admin.register(models.Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ('pet', 'author', 'price', 'status')
    list_filter = ('status',)


@admin.register(models.Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('lot', 'author', 'price')