from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

#more models
class Category(models.Model):
    name=models.CharField(max_length =64)
    url = models.URLField(max_length = 200 , default="http://placehold.it/460x250/e67e22/ffffff&text=HTML5") 
    
    def __str__(self):
        return f"{self.name}"

class Auctionlist(models.Model):
    
    title = models.CharField(max_length =64 )
    description = models.TextField()
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    url = models.URLField(max_length = 200)
    date = models.DateField()
    active = models.BooleanField()
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    category = models.ForeignKey(Category ,on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.id} {self.user.username} {self.title} {self.bid}"

class Bids(models.Model):

    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    auctionlist = models.ForeignKey(Auctionlist ,on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} {self.auctionlist.title} {self.bid} {self.winner}"

class Comments(models.Model):

    comment = models.CharField(max_length = 200 )
    date = models.DateField()
    auctionlist = models.ForeignKey(Auctionlist ,on_delete=models.CASCADE)
    user = models.ForeignKey(User ,on_delete=models.CASCADE)

class Watchlist(models.Model):
    user = models.CharField(max_length = 200 )
    auctionlist = models.ForeignKey(Auctionlist ,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.auctionlist}"
