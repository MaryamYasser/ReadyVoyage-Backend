from distutils.command.upload import upload
from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator







class MyAccountManager(BaseUserManager):
    def create_user(self,email,username, password=None,**extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
             **extra_fields
            
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,username,password = None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(unique=True)
    #password = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to = 'images/',null = True, blank = True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff =  models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()


    def __str__(self):
        return self.username

    def has_perm(self,perm,obj = None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True





class Preferences(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    budget = models.IntegerField()
    max_duration = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(30)])
    starting_city = models.CharField(max_length=50)
    preferences = models.JSONField()

    ##KEY VALUE PAIRS?

class Place(models.Model):
    Budget_Choices = (
        ('0','Free'),
        ('1','Inexpensive'),
        ('2','Moderate'),
        ('3','Expensive'),
        ('4','Very Expensive')
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    budget_range = models.CharField(choices=Budget_Choices,default='Moderate',max_length=20)
    photo = models.ImageField(upload_to = "places_images")

    # orders places by name 
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Trip(models.Model):
    user = models.ForeignKey(Preferences, on_delete=models.SET_NULL,null=True)
    plan = models.ManyToManyField(Place,related_name=('Plan'))

    
    ## array of array of places id



class UserTrips(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL,null=True)
    rating = models.IntegerField()






# Create your models here.
