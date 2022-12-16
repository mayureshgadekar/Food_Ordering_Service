from django.db import models

# Create your models here.

class signin_userdata(models.Model):
    emailid=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class signin_resdata(models.Model):
    emailid=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class insert_userdata(models.Model):
    emailid=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    phone_number=models.IntegerField()
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    
class insert_resdata(models.Model):
    r_emailid=models.CharField(max_length=100)
    r_password=models.CharField(max_length=100)
    r_name=models.CharField(max_length=100)
    r_phone_number=models.IntegerField()
    r_address=models.CharField(max_length=100)
    r_city=models.CharField(max_length=100)
    r_country=models.CharField(max_length=100)

class insert_resmenu(models.Model):
    r_emailid=models.CharField(max_length=100)
    Item=models.CharField(max_length=100)
    Price=models.IntegerField()
    
class insert_cart(models.Model):
    emailid=models.CharField(max_length=100)
    r_name=models.CharField(max_length=100)
    Item=models.CharField(max_length=100)
    Price=models.IntegerField()
    
class search_res(models.Model):
    r_name=models.CharField(max_length=100)
    Item=models.CharField(max_length=100)
        
class user_page_display(models.Model):
    r_emailid = models.CharField(max_length=100)
    Item = models.CharField(max_length=100)
    Price = models.IntegerField()

class res_menu_page_display(models.Model):
    r_emailid = models.CharField(max_length=100)

    
    