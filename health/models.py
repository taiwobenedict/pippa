from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
import uuid


# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    age = models.IntegerField(default=0, blank=False)
    sex = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    location = models.CharField(max_length=200, blank=False)

    def save(self, *args, **kwargs):
        # Automatically set the username to be the same as the email
        if not self.username:
            self.username = self.email
        
        # Hash the password before saving, if it's not already hashed
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)



class StressRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    overall_stress_level = models.IntegerField(default=0, blank=True)
    pre_frontal_cortext = models.IntegerField(default=0, blank=True)
    hypothalamus = models.IntegerField(default=0, blank=True)
    amygdala = models.IntegerField(default=0, blank=True)
    hippocampus = models.IntegerField(default=0, blank=True)
    social_connected = models.IntegerField(default=0, blank=True)
    physical_active = models.IntegerField(default=0, blank=True)
    time_in_nature = models.IntegerField(default=0, blank=True)
    health_diet = models.IntegerField(default=0, blank=True)
    sleep_quality = models.IntegerField(default=0, blank=True)
    daily_phone_use = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return  f'{self.user.get_full_name()} stress record'



class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='modules')
    name = models.CharField(max_length=150)
    info =  models.CharField(max_length=150, blank= True)
    completed = models.BooleanField(default=False)
    next = models.OneToOneField("self",on_delete=models.SET_NULL, null=True, blank=True, related_name="previous")
    order = models.PositiveIntegerField(default=0)
    
    def total_completed_programs(self):

        return self.programs.filter(completed=True).count()
        
    def total_programs(self):
        return self.programs.count()
    
    def __str__(self):
        return f'{self.name} {self.order} | {self.info}'
    
    
class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete= models.CASCADE, related_name="programs")
    title = models.CharField(max_length=200,)
    completed = models.BooleanField(default=False)
    video = models.URLField()
    next = models.OneToOneField("self",on_delete=models.SET_NULL, null=True, blank=True, related_name="previous")
    order = models.PositiveIntegerField(default=0,)
    
    def __str__(self):
        return f'{self.title} {self.order} | {self.module.name}'