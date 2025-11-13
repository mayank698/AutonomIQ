from django.contrib import admin
from .models import Student, Customer, Employee


class StudentsAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ["name", "roll_no", "created_at"]
    # ordering = ["created_at"]
    list_filter = ["created_at", "updated_at"]
    date_hierarchy = "created_at"


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("customer_name",)
    list_display = ["customer_name", "created_at"]
    list_filter = ["created_at", "updated_at"]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["employee_name", "designation", "created_at"]
    search_fields = ("employee_name",)
    list_filter = ("created_at", "designation")


# Register your models here.
admin.site.register(Student, StudentsAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
