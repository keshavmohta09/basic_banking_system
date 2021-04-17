from django.db import models
from django.utils import translation

# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class User(Base):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    balance = models.DecimalField(max_digits=50,decimal_places=2)
    account_no = models.CharField(max_length=15,unique=True)
    mobile_no = models.CharField(max_length=10,unique=True)
    address = models.TextField()
    ifsc_code = models.CharField(max_length=20)
    aadhar_number = models.CharField(max_length=12,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Customer"

class Transaction(Base):
    sender = models.ForeignKey(User,related_name='sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='receiver',on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=50,decimal_places=2)

    def __str__(self):
        return f"{self.id}"