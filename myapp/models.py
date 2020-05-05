from django.db import models

# Create your models here.
class Company_Info(models.Model):
    company = models.CharField(max_length=100, null=False)
    units = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.company
    

class Credit_Info(models.Model):
    bank = models.CharField(max_length=100, null=False)
    credit = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    used = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    company = models.ForeignKey(Company_Info, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.bank
    