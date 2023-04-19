from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class User(AbstractUser):
    pass

# Listing model all listing data
class Listing(models.Model):
    unspecified = "Unspecified"

    categories = [
        (unspecified, "Unspecified"),
        ("Kids", "Kids"),
        ("Cars", "Cars"),
        ("Clothing", "Clothing"),
        ("Electronics", "Electronics"),
        ("Games","Games"),
        ("Toys","Toys"),
        ("Sporting Goods","Sporting Goods"),
        ("Jwellary & Watches","Jwellary & Watches")
    ]

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    starting_bid = models.IntegerField()
    image_url = models.TextField(blank=True, default="https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg")
    active = models.BooleanField(default = True)
    category = models.CharField(max_length=64, choices=categories, default=unspecified)

    def __str__(self):
        return f"{self.id} : {self.title}"



# watchlist model
class WatchList(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watcher")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_list")

    def __str__(self):
        return f"{self.listing} : {self.user}"


# commend on listing
class Command(models.Model):
    command = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commands")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commander")

    def __str__(self):
        return f"{self.command}"


# all the bids on listing
class Auction(models.Model):
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    highest_bid = models.BooleanField(default=True)
    amount = models.IntegerField()

    def __str__(self):
        return f"bid amount = {self.amount} | title : {self.listing.title} | by : {self.user.username} {self.highest_bid}"