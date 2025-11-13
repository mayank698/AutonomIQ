from django.db import models


# Create your models here.
class Student(models.Model):
    roll_no = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.customer_name


class Employee(models.Model):
    employee_id = models.IntegerField()
    employee_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=True)
    retirement = models.DecimalField(max_digits=10, decimal_places=True)
    other_benefits = models.DecimalField(max_digits=10, decimal_places=True)
    total_benefits = models.DecimalField(max_digits=10, decimal_places=True)
    total_compensation = models.DecimalField(max_digits=10, decimal_places=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee_name
