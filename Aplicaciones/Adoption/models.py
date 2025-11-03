from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo_path = models.ImageField(upload_to='users', blank=True, null=True)
    role = models.CharField(max_length=20, default='adopter')
    num_publications=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, blank=True, null=True)
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='available')  
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class PetPhoto(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='pets')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Photo of {self.pet.name}"


class Adoption(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopter = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    contract_path = models.FileField(upload_to='adoptions', blank=True, null=True)

    def __str__(self):
        return f"{self.adopter.username} -> {self.pet.name}"
