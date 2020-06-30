from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    pic = models.ImageField(default='media/default.jpg', upload_to='account', blank=True)
    bio = models.TextField(blank=True)

    REQUIRED_FIELDS = ('email',)
    def __str__(self):
        return self.username
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.pic.path)
        except:
            img = Image.open('media/default.jpg')
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pic.path)