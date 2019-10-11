from django.contrib import admin

# Register your models here.

from . models import Category, Product, Subcategories, feedback

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['Scategory', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category','subcategory', 'price', 'stock', 'available', 'created', 'update']
    list_filter = ['available', 'created', 'update' ,'category']
    list_editable = ['price', 'stock', 'available', ]
    prepopulated_fields = {'slug': ('name',)}

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name','email','msg']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategories, SubCategoryAdmin)
admin.site.register(feedback, FeedbackAdmin)

