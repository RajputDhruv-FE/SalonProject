from django.db import models


class CityMst(models.Model):
    CityName = models.CharField(max_length=30)
    
    def __str__(self):
        return self.CityName
    class Meta:
        ordering=['CityName']

class AreaMst(models.Model):
    AreaName = models.CharField(max_length=40)
    CityName = models.ForeignKey(CityMst, on_delete=models.CASCADE)
    def __str__(self):
        return self.AreaName


class ServiceMst(models.Model):
    ServiceName = models.CharField(max_length=30)
    def __str__(self):
        return self.ServiceName
class UserMst(models.Model):
    Name= models.CharField(max_length=20)
    UserName = models.CharField(max_length=20)
    Email = models.EmailField(max_length=50)
    PhoneNumber = models.CharField(max_length=10)
    Password = models.CharField(max_length=20)
    Usertype= models.CharField(max_length=10)
    Status= models.CharField(max_length=10)
    Img=models.ImageField(default='default.jpg') 
    
class SalonMst(models.Model):
    Name = models.CharField(max_length=20)
    Location = models.CharField(max_length=20)
    Owner = models.ForeignKey(UserMst, on_delete=models.CASCADE)
    Img = models.ImageField(default='default.jpg')
    Status = models.CharField(max_length=10)
    Service = models.ForeignKey(ServiceMst, on_delete=models.CASCADE)
    Area = models.ForeignKey(AreaMst, on_delete=models.CASCADE)
    City = models.ForeignKey(CityMst, on_delete=models.CASCADE)
    OpenTime = models.TimeField()
    CloseTime = models.TimeField()
    Type = models.CharField(max_length=10)

