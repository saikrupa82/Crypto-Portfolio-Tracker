from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from viewflow.fields import CompositeKey



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Holdings(models.Model):
    # auto_increment_id = models.AutoField(primary_key=True)
    # id = CompositeKey(columns=['user', 'symbol_name'])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.FloatField()
    symbol_name = models.CharField(max_length=255)
    amount_spent = models.FloatField()
    # class Meta:
    #     db_table = 'Holdings'
    #     unique_together = (("symbol_name", "user"),)
        # managed = True

class Transaction(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=255)
    symbol_name = models.CharField(max_length=255)
    quantity = models.FloatField()
    price = models.CharField(max_length=20)
    date = models.DateField() 
    buy_sell = models.CharField(max_length=255)

class AddReminder(models.Model):
    FILTER_CHOICES = (
        ('Above', 'Above'),
        ('Below', 'Below'),
    )
    auto_increment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Price = models.FloatField()
    Above_below = models.CharField(max_length = 20,choices = FILTER_CHOICES,default='buy')
    Notes = models.CharField(max_length=100000)
    
class DailyStats(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    portfolio_value = models.FloatField()
    # portfolio_value_24 = models.FloatField()