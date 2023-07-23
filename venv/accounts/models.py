from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils.text import slugify
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_favorites =models.ManyToManyField(Product)

    slug=models.SlugField(max_length=50,blank=True,null=True)
    address = models.CharField(max_length=60)
    address2 = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    zip_number = models.CharField(max_length=5)

    def __str__(self):
        return self.user.username
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.user.username)
        super(UserProfile,self).save(*args,**kwargs)