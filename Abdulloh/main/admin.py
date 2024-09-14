from django.contrib import admin
from .models import Product, Category, Comment, ProductImage



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'price', 'created_at')
    inlines = [ProductImageInline]
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'created_at')
    search_fields = ('product__name', 'text')
    list_filter = ('product', 'user', 'created_at')
    ordering = ('-created_at',)