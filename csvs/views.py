import csv
from decimal import Decimal

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template.defaultfilters import slugify

from .forms import CsvModelForm
from .models import Csv
from store.models import Product,Category



# Create your views here.

@login_required
@permission_required('csvs.can_upload_csv', raise_exception=True)
def upload_file_view(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated = False)
        with open(obj.file_name.path, 'r', encoding="utf8") as f:
            reader = csv.reader(f)
            next(reader) #go past header
            for row in reader:
                category, _ = Category.objects.get_or_create(slug=slugify(row[5]))
                if row[3]:
                    discount_decimal = Decimal(row[3].strip(', "\''))
                else:
                    discount_decimal = Decimal('0.0')
                product, _ = Product.objects.get_or_create(name=row[0],
                    slug=row[1],
                    price=Decimal(row[2].strip(', "\'')),
                    discount_price=discount_decimal,
                    description=row[4],
                    category=category,
                    color_or_version=row[6],
                    tags=row[7],
                    )
                product.save()
            print('CSV file added to database')
            obj.activated = True
            obj.save()

    return render(request, 'csvs/upload.html', {'form': form})