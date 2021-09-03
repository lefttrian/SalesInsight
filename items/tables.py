from django.db import models
import django_tables2 as tables
from items.models import Product, Supplier, ProductCategory,ProductSubCategoryList
from djmoney.models.fields import MoneyField
from datetime import datetime

class NumberColumn(tables.Column):
    def render(self, value):
        return '{:0.2f}'.format(value)

class ProductTable(tables.Table):
    id = tables.Column(visible=False)
    code = tables.Column(linkify=True,attrs={"th": {"width": "200px"}, "td": {"width": "200px"}})
    description=tables.Column()
    descr2 = tables.Column(visible=False)
    valuey0 = NumberColumn(verbose_name=datetime.now().year)
    valuey1 = NumberColumn(verbose_name=datetime.now().year-1)
    valuey2 = NumberColumn(verbose_name=datetime.now().year-2)
    valuey3 = NumberColumn(verbose_name=datetime.now().year-3)
    valuey4 = NumberColumn(verbose_name=datetime.now().year-4)
    valuey5 = NumberColumn(verbose_name=datetime.now().year-5)

    class Meta:
        model = Product
        attrs = {"class": "table table-sm table-striped table-hover"}


class ProductCategoryTable(tables.Table):
    category = tables.Column(linkify=True)
    valuey0 = NumberColumn(verbose_name=datetime.now().year)
    valuey1 = NumberColumn(verbose_name=datetime.now().year-1)
    valuey2 = NumberColumn(verbose_name=datetime.now().year-2)
    valuey3 = NumberColumn(verbose_name=datetime.now().year-3)
    valuey4 = NumberColumn(verbose_name=datetime.now().year-4)
    valuey5 = NumberColumn(verbose_name=datetime.now().year-5)


    class Meta:
        model = ProductCategory
        attrs = {"class": "table table-sm table-striped table-hover"}


class ProductSubCategoryListTable(tables.Table):
    fltid3 = tables.Column(linkify=True, verbose_name='Category')
    valuey0 = NumberColumn(verbose_name=datetime.now().year)
    valuey1 = NumberColumn(verbose_name=datetime.now().year-1)
    valuey2 = NumberColumn(verbose_name=datetime.now().year-2)
    valuey3 = NumberColumn(verbose_name=datetime.now().year-3)
    valuey4 = NumberColumn(verbose_name=datetime.now().year-4)
    valuey5 = NumberColumn(verbose_name=datetime.now().year-5)
    qy0 = NumberColumn(visible=False)
    qy1 = NumberColumn(visible=False)
    qy2 = NumberColumn(visible=False)
    qy3 = NumberColumn(visible=False)
    qy4 = NumberColumn(visible=False)
    qy5 = NumberColumn(visible=False)

    class Meta:
        model = ProductSubCategoryList
        attrs = {"class": "table table-sm table-striped table-hover"}


class SupplierTable(tables.Table):
    id = tables.Column(linkify=True)
    code = tables.Column()
    name =tables.Column()
    valuey0 = NumberColumn(verbose_name=datetime.now().year)
    valuey1 = NumberColumn(verbose_name=datetime.now().year-1)
    valuey2 = NumberColumn(verbose_name=datetime.now().year-2)
    valuey3 = NumberColumn(verbose_name=datetime.now().year-3)
    valuey4 = NumberColumn(verbose_name=datetime.now().year-4)
    valuey5 = NumberColumn(verbose_name=datetime.now().year-5)

    class Meta:
        model = Supplier
        attrs = {"class": "table table-sm table-striped table-hover"}
