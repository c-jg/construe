from django.db import models

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email

class Plan(models.Model):
    first_name = models.CharField(max_length=50)
    email = models.EmailField()
    comments = models.IntegerField(verbose_name= 'Estimated number of comments needed to be analyzed')
    full_channel = models.BooleanField(verbose_name= 'Check this box if you need all comments from a channel analyzed')
    multiple_channels = models.BooleanField(verbose_name= 'Check this box if you need all comments from multiple channels analyzed')
    advertisement = models.BooleanField(verbose_name= 'Check this box if you need advertisement comment analysis')
    other_platforms = models.BooleanField(verbose_name= 'Check this box if you need comment analysis for other platforms (Facebook, Instagram, Twitter, etc.)')
    message = models.TextField(verbose_name= 'Additional details', null=True)