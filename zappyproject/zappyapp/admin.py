from django.contrib import admin
from zappyapp.models import Product,Customer,Order,Cart



class ProductAdmin(admin.ModelAdmin):
    list_display=['cat_choice','price','pname']
    list_filter=['cat_choice']
    list_editable=['price','pname']

admin.site.register(Product,ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display=['customer','cust_address','mobile']
    list_filter=['customer']
    list_editable=['mobile']

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Order)
admin.site.register(Cart)
