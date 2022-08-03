from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    name=models.CharField(max_length=60)
    description=models.TextField(blank=True,null=True,max_length=500)
    image_product=models.ImageField(upload_to='product_images', default='https://betarill.com/media/images/products/default_product.png')
    stores=models.CharField(max_length=50)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    picture = models.ImageField(upload_to="profile_images", blank=True)

    def __str__(self):
        return self.user.username