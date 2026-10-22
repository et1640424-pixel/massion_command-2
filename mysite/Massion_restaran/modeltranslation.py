from modeltranslation.translator import TranslationOptions, register
from .models import restaran, category, product, book_a_table

@register(restaran)
class RestaranTranslationOptions(TranslationOptions):
    fields = ('restaran',)
    required_fields = ('name',)

@register(category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category',)
    required_fields = ('name',)

@register(product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product',)
    required_fields = ('name',)
    
@register(book_a_table)
class BookATableTranslationOptions(TranslationOptions):
    fields = ('book_a_table',)
    required_fields = ('name',)