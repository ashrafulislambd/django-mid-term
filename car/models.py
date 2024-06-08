from django.db import models
from brand.models import Brand
from django.contrib.auth.models import User

class Car(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="car/media/uploads/")
    price = models.IntegerField()
    quantity = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    name = models.CharField(max_length=100)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:50]
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.time)