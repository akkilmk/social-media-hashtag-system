import os
import datetime
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('', filename)



class PostManager(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=100)
    image = models.ImageField(upload_to=filepath)