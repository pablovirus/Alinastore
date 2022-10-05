from .models import Category
from .misc_scripts import parser


def categories_dropdown(request):
    categories = Category.objects.all().order_by('name')
    categories_rows = parser(categories, 4)
    return { 'categories_rows' : categories_rows }
