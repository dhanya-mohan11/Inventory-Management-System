from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(Vendor)
admin.site.register(Unit)
# admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseBill)
admin.site.register(Sale)
admin.site.register(SaleBill)
# admin.site.register(Stock)
admin.site.register(UserProfile)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass

@admin.register(Stock)
class StockAdmin(ImportExportModelAdmin):
    pass