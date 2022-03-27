from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'carmake', 'dealer_id', 'type']

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']

admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)