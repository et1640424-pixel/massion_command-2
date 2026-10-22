from django.contrib import admin
from .models import UserProfile, Restaran, Category, Product, book_a_table, Cart, CartItem, Favorite
from modeltranslation.admin import TranslationAdmin


@admin.register(Restaran, Category, Product, book_a_table)
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
