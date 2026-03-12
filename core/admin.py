from django.contrib import admin
from .models import Donor,BloodRequest

admin.site.register(Donor)

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'status')
    list_filter = ('status',)