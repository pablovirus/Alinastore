from ast import Or
from atexit import register
from django.contrib import admin
from .models import Product, Order, OrderProduct, ProductImages, Category, Customer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
    class Meta:
        model = Category

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Customer)

class ProductImagesAdmin(admin.StackedInline):
    model = ProductImages
    extra = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = Product        

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    pass



