from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    role = ((
        ('chef', 'Chef'),
        ('user', 'User')
    ))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_Name = models.CharField(max_length=200)
    last_Name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=role)
    otp = models.CharField(max_length=6, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.full_name} - {self.role}" 
    
class recipes(models.Model):
    category = ((
        ('chef', 'Chef'),
        ('user', 'User')
    ))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=200)
    caterogy = models.CharField(max_length=20, choices=category)
    description = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.user}" 

class ingredient(models.Model):
    recipie_id  = models.ForeignKey(recipes, on_delete=models.CASCADE, related_name="ingredient")
    ingredient_name = models.CharField(max_length=200)
    ammount = models.CharField(max_length=20)
    vitamin_contain = models.TextField()

    def __str__(self):
        return f"{self.recipie_id}" 


class instruction(models.Model):
    recipie_id  = models.ForeignKey(recipes, on_delete=models.CASCADE, related_name="instruction")
    note = models.TextField()

    def __str__(self):
        return f"{self.recipie_id}" 


class chefNote(models.Model):
    recipie_id  = models.ForeignKey(recipes, on_delete=models.CASCADE, related_name="chefNote")
    note = models.TextField()

    def __str__(self):
        return f"{self.recipie_id}" 

class ChefPostCreation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chefPostCreation")
    title = models.CharField(max_length=200)
    description = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user}" 

class Comment(models.Model):
    post = models.ForeignKey(ChefPostCreation, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    parent = models.ForeignKey("self",on_delete=models.CASCADE, null=True, blank = True)
    comment_text = models.TextField(null=True, blank = True)




