from django.db import models
from datetime import datetime

# Create your models here.
class Product(models.Model):
    name =models.CharField(max_length=150)
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    photo=models.ImageField(upload_to='photo/%Y/%m/%d/')
    is_active=models.BooleanField(default=True)
    publish_date=models.DateTimeField(default=datetime.now)


    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering =['name']