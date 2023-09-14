from django.contrib.auth.models import Permission, User
from django.db import models


class Seller(models.Model):
    user = models.ForeignKey(User, default=1)
    Key = models.CharField(max_length=10)
    BookSet_Photo = models.FileField()
    Subjects = models.CharField(max_length=500)
    Description = models.CharField(max_length=500)
    Total_Price = models.CharField(max_length=10)
    wishlist = models.BooleanField(default=False)

    def __str__(self):
        return self.key + ' - ' + self.total_price


class Chat(models.Model):
    created = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User)
    message = models.TextField()

    def __unicode__(self):
        return self.message
