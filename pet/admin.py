from django.contrib import admin

from .models import Pet, Breed, Registration, Food

# Register your models here.
admin.site.register(
    (Pet, Breed, Food)
)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    exclude = ["reg_num"]