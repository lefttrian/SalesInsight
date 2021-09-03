# -*- coding: utf-8 -*-
import django_filters as filters
from django.db import models
from django.db.models import F, Case, When, Q, CharField, Value
from django.db.models.functions import Substr


class Supplier(models.Model):
    id = models.AutoField(db_column='MASTERID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=25, blank=True,
                            null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True,
                            null=True)  # Field name made lowercase.
    valuey0 = models.FloatField(db_column='valuey0')
    valuey1 = models.FloatField(db_column='valuey1')
    valuey2 = models.FloatField(db_column='valuey2')
    valuey3 = models.FloatField(db_column='valuey3')
    valuey4 = models.FloatField(db_column='valuey4')
    valuey5 = models.FloatField(db_column='valuey5')

    class Meta:
        managed = False
        ordering = ['name']
        db_table = 'SUPPLIERBROWSER'

    def get_absolute_url(self):
        return "%i/details" % self.id

    def __str__(self):
        return self.code+' '+self.name

class Country(models.Model):
    codeid = models.AutoField(db_column='CODEID', primary_key=True)
    descr = models.CharField(db_column='DESCR', max_length=255)

    class Meta:
        managed = False
        db_table = 'dbo].[COUNTRY'

    def __str__(self):
        return self.descr

class SupplierCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null= False)


    class Meta:
        managed = False
        db_table = 'SupplierCategory'

    def __str__(self):
        return self.name



class SupplierDetail(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=25, blank=True, null=True, verbose_name='Supplier code')  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True, null=True, verbose_name='Supplier name')  # Field name made lowercase.
    occupation = models.CharField(db_column='OCCUPATION', max_length=255, blank=True, null=True)
    city = models.CharField(db_column='CITY1', max_length=255, blank=True, null=True)
    district = models.CharField(db_column='DISTRICT1', max_length=255, blank=True, null=True)
    email = models.CharField(db_column='EMAIL', max_length=255, blank=True, null=True)
    street1 = models.CharField(db_column='STREET1', max_length=255, blank=True, null=True)
    zipcode = models.CharField(db_column='ZIPCODE1', max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='cntid')
    category = models.ManyToManyField(SupplierCategory,blank=True,through="SupplierAttribute", verbose_name='Supplier salesinsight category')

    class Meta:
        managed = False
        db_table = 'dbo].[SUPPLIER'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return ProductDetail.objects.filter(id=timezone.now())


class SupplierAttribute(models.Model):
    id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey(SupplierDetail, models.DO_NOTHING,db_column='supplier_id')
    suppliercategory_id = models.ForeignKey(SupplierCategory, models.CASCADE, db_column='suppliercategory_id')
    safetystock = models.FloatField(null=True, verbose_name='Safety stock')
    annual_consumption_value = models.FloatField(null=True, verbose_name='Annual consumption value')
    annual_units = models.FloatField(null=True, verbose_name='Annual units sold')
    percent_acv = models.FloatField(null=True, verbose_name='Percent of total annual consumption value')
    percent_au = models.FloatField(null=True, verbose_name='Percent of total annual units sold')

    class Meta:
        managed = False
        db_table = 'SupplierAttribute'

    def __str__(self):
        return self.supplier_id.name


class SuppBalance(models.Model):
    supid = models.AutoField(db_column='MASTERID', primary_key=True)
    fyeid = models.IntegerField(db_column='FYEID')
    fipid = models.IntegerField(db_column='FIPID')
    masterperiodturnover = models.FloatField('MASTERPERIODTURNOVER')

    class Meta:
        managed = False
        db_table = 'dbo].[SUPPBALANCESHEET'


class SupplierFilter(filters.FilterSet):
    code = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Supplier
        fields = ['code', 'name']


class ProductCat(models.Model):
    codeid = models.AutoField(db_column='CODEID', primary_key=True)
    descr = models.CharField(db_column='DESCR', max_length=255)

    class Meta:
        managed = False
        db_table = 'dbo].[FLDCUSTBL1'

    def __str__(self):
        return self.descr


class ProductSubCategory(models.Model):
    id = models.AutoField(db_column='CODEID', primary_key=True)
    name = models.CharField(db_column='DESCR', max_length=255)

    class Meta:
        managed = False
        db_table = 'dbo].[FLDCUSTBL3'

    def __str__(self):
        return self.name


class ProductSubCategoryList(models.Model):
    fltid3 = models.AutoField(db_column='FLTID3', primary_key=True)  # Field name made lowercase.
    valuey0 = models.FloatField(db_column='valuey0')
    valuey1 = models.FloatField(db_column='valuey1')
    valuey2 = models.FloatField(db_column='valuey2')
    valuey3 = models.FloatField(db_column='valuey3')
    valuey4 = models.FloatField(db_column='valuey4')
    valuey5 = models.FloatField(db_column='valuey5')
    qy0 = models.FloatField(db_column='qy0')
    qy1 = models.FloatField(db_column='qy1')
    qy2 = models.FloatField(db_column='qy2')
    qy3 = models.FloatField(db_column='qy3')
    qy4 = models.FloatField(db_column='qy4')
    qy5 = models.FloatField(db_column='qy5')

    class Meta:
        managed = False
        db_table = 'ITEMSUBCATEGORYBROWSER'

    def get_absolute_url(self):
        return "%i/details" % self.fltid3


class ProductSubcategoryFilter(filters.FilterSet):
    fltid3 = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ProductSubCategoryList
        fields = ['fltid3']

class Mesunit(models.Model):
    codeid = models.AutoField(db_column='CODEID', primary_key=True)
    descr = models.CharField(db_column='DESCR', max_length=255)

    class Meta:
        managed = False
        db_table = 'dbo].[MESUNIT'

    def __str__(self):
        return self.descr

class ItemFinData(models.Model):
    masterid=models.IntegerField(db_column='MASTERID',primary_key=True)
    costvalue=models.FloatField(db_column='COSTVALUE')

    class Meta:
        managed = False
        db_table = 'dbo].[ITEMFINDATA'

    def __str__(self):
        return self.costvalue.__str__()

class Product(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='SUBCODE1', max_length=25, blank=True,
                                null=True)  # Field name made lowercase.
    name = models.CharField(db_column='DESCRIPTION', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    descr2 = models.CharField(db_column='descr2', max_length=9999, blank=True, null=True)
    valuey0 = models.FloatField(db_column='valuey0')
    valuey1 = models.FloatField(db_column='valuey1')
    valuey2 = models.FloatField(db_column='valuey2')
    valuey3 = models.FloatField(db_column='valuey3')
    valuey4 = models.FloatField(db_column='valuey4')
    valuey5 = models.FloatField(db_column='valuey5')

    class Meta:
        managed = False
        db_table = 'ITEMSBROWSER'

    def get_absolute_url(self):
        return "%i/details" % self.id


class ProductCategory(models.Model):
    category = models.AutoField(db_column='category',primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=255, blank=True,
                            null=True, verbose_name='Περιγραφή')
    valuey0 = models.FloatField(db_column='valuey0')
    valuey1 = models.FloatField(db_column='valuey1')
    valuey2 = models.FloatField(db_column='valuey2')
    valuey3 = models.FloatField(db_column='valuey3')
    valuey4 = models.FloatField(db_column='valuey4')
    valuey5 = models.FloatField(db_column='valuey5')

    class Meta:
        managed = False
        db_table = 'ITEMCATEGORYBROWSER'

    def get_absolute_url(self):
        return "%i/details" % self.category


class ProductDetail(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='SUBCODE1', max_length=25, blank=True, null=True,unique=True, verbose_name='Κωδικός')  # Field name made lowercase.
    name = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True,
                            null=True, verbose_name='Περιγραφή')  # Field name made lowercase.
    category = models.ForeignKey(ProductCat, models.DO_NOTHING,db_column='fltid1', verbose_name='Κατηγορία')
    composition = models.CharField(db_column='COMPOSITION', max_length=255, blank=True, null=True, verbose_name='Αγγλική Περ.')
    mu1 = models.ForeignKey(Mesunit, models.DO_NOTHING, db_column='mu1', verbose_name='Μον. Μέτρ.')
    descr2 = models.CharField(db_column='descr2', max_length=9999, blank=True, null=True, verbose_name='Πεδίο Αναζ.')
    cost = models.ForeignKey(ItemFinData, models.DO_NOTHING, db_column='id', verbose_name='Κόστος',  help_text='Κόστος μαζί με απόθεμα')
    subcategory = models.ForeignKey(ProductSubCategory, models.DO_NOTHING, db_column='fltid3', verbose_name='Υποκατηγορία SalesInsight')
    lastbuyprice = models.FloatField(db_column='lastbuyprice', verbose_name='Τελ. τιμή αγοράς',  help_text='Τελευταία τιμή αγοράς με κόστη φακέλου επιμερισμένα')
    suppliers = models.ManyToManyField(SupplierDetail,blank=True,through='ItemSup')


    class Meta:
        managed = False
        db_table = 'dbo].[MATERIAL'


class ProductFilter(filters.FilterSet):
    descr2 = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['descr2']


class ProductCategoryFilter(filters.FilterSet):

    class Meta:
        model = ProductCategory
        fields = []


class CustomerSet(models.QuerySet):
    def custom_set(self, id_list):
        return self.filter(id__in=id_list)

    def domestic_sales(self):
        self.custom_set()

    def get_first_digit_of_code(self):
        return self.annotate(
            firstdigit=Substr('code', 1, 1)
        )

class Customer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    valuey0 = models.FloatField(db_column='valuey0')
    valuey1 = models.FloatField(db_column='valuey1')
    valuey2 = models.FloatField(db_column='valuey2')
    valuey3 = models.FloatField(db_column='valuey3')
    valuey4 = models.FloatField(db_column='valuey4')
    valuey5 = models.FloatField(db_column='valuey5')
    objects = CustomerSet.as_manager()

    class Meta:
        managed = False
        db_table = 'CUSTOMERBROWSER'

    def get_absolute_url(self):
        return "%i/details" % self.id

class CustomerDetail(models.Model):
    id = models.AutoField(db_column='ID',  primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', verbose_name='Κωδικός', max_length=25, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', verbose_name='Επωνυμία',  max_length=255, blank=True, null=True)  # Field name made lowercase.
    occupation = models.CharField(db_column='OCCUPATION', verbose_name='Απασχόληση',  max_length=255, blank=True, null=True)
    city = models.CharField(db_column='CITY1', verbose_name='Πόλη',  max_length=255, blank=True, null=True)
    district = models.CharField(db_column='DISTRICT1', max_length=255, blank=True, null=True)
    email = models.CharField(db_column='EMAIL', max_length=255, blank=True, null=True)
    street1 = models.CharField(db_column='STREET1', max_length=255, blank=True, null=True)
    zipcode = models.CharField(db_column='ZIPCODE1', max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, verbose_name='Χώρα',  db_column='cntid')

    class Meta:
        managed = False
        db_table = 'dbo].[CUSTOMER'


class CustomerFilter(filters.FilterSet):
    code = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['code', 'name']


class Itemtrans(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    iteid = models.ForeignKey(ProductDetail, models.DO_NOTHING, db_column='iteid')
    outputvalmode = models.SmallIntegerField(db_column='OUTPUTVALMODE', null=True)
    outputquantmode = models.SmallIntegerField(db_column='OUTPUTQUANTMODE', null=True)
    primaryqty = models.FloatField(db_column='PRIMARYQTY', null=True)
    trnvalue = models.FloatField(db_column='TRNVALUE', null=True)
    trndate = models.DateTimeField(db_column='TRNDATE', null=True)
    fyeid = models.IntegerField(db_column='FYEID', null=False)
    fipid = models.IntegerField(db_column='FIPID', null=False)
    perid = models.ForeignKey(CustomerDetail, models.DO_NOTHING,db_column='perid')
    source = models.IntegerField(db_column='SOURCE', null=False)

    class Meta:
        managed = False
        db_table = 'dbo].[ITEMTRANS'

    def get_year(self):
        return self.trndate.year


class ItemSup(models.Model):
    product_id = models.ForeignKey(ProductDetail, models.DO_NOTHING, db_column='iteid' )
    supplier_id = models.ForeignKey(SupplierDetail,models.DO_NOTHING, db_column='supid'  )
    lastbuysupprice=models.FloatField(db_column='LASTBUYSUPPRICE', null=True)
    lastbuysuppriceupdate=models.DateTimeField(db_column='LASTBUYSUPPRICEUPDATE', null=True)

    class Meta:
        managed = False
        unique_together = ['product_id', 'supplier_id']
        db_table = 'dbo].[ITEMSUP'


class CeleryTasks(models.Model):
    id=models.AutoField(primary_key=True)
    task_id=models.CharField(max_length=155, null=True)
    status=models.CharField(max_length=50, null=True)

    class Meta:
        managed=False
        db_table = 'celery_taskmeta'


class OptimizationItem(models.Model):
    id=models.AutoField(primary_key=True)
    codeid=models.OneToOneField(ProductSubCategory,models.DO_NOTHING,db_column='codeid')
    code=models.CharField(max_length=255, null=False)
    supplier = models.ManyToManyField(SupplierDetail, blank=True,
                                   through='OptimizationItemAttribute')
    safetystock=models.FloatField(null=True, verbose_name='Safety stock')
    annual_consumption_value=models.FloatField(null=True, verbose_name='Annual consumption value')
    annual_units=models.FloatField(null=True, verbose_name='Annual units sold')
    percent_acv=models.FloatField(null=True, verbose_name='Percent of total annual consumption value')
    percent_au=models.FloatField(null=True, verbose_name='Percent of total annual units sold')
    ABC = models.CharField(max_length=10, null=True, verbose_name='ABC analysis category')
    coeffv = models.FloatField(null=True,db_column='cv', verbose_name='Coefficient of variation (volatility)')
    reorder_point = models.FloatField(null=True,db_column='reorder_point', verbose_name='Reorder point')


    class Meta:
        managed=False
        db_table = 'OptimizationItem'


class OptimizationItemAttribute(models.Model):
    id=models.AutoField(primary_key=True, name='id')
    optimizationitem_id=models.ForeignKey(OptimizationItem, models.CASCADE,db_column='optimizationitem_id')
    supplier_id=models.ForeignKey(SupplierDetail,models.DO_NOTHING,db_column='supplier_id')
    safetystock=models.FloatField(null=True, verbose_name='Safety stock')
    annual_consumption_value=models.FloatField(null=True, verbose_name='Annual consumption value')
    annual_units=models.FloatField(null=True, verbose_name='Annual units sold')
    percent_acv=models.FloatField(null=True, verbose_name='Percent of total annual consumption value')
    percent_au=models.FloatField(null=True, verbose_name='Percent of total annual units sold')
    reorder_point = models.FloatField(null=True,db_column='reorder_point', verbose_name='Reorder point')

    class Meta:
        managed=False
        db_table = 'OptimizationItemAttribute'
        unique_together=['optimizationitem_id','supplier_id']


class Tasks(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    status=models.SmallIntegerField(null=False, default=0)

    def __str__(self):
        return f'{self.id} {self.name}'


class Settings(models.Model):
    id=models.AutoField(primary_key=True)
    A_percent=models.IntegerField(null=False)
    B_percent=models.IntegerField(null=False)
    C_percent = models.IntegerField(null=False)
    lastforecast = models.DateTimeField(null=True)

    class Meta:
        managed=False
        db_table = 'Settings'


class FullItemStoreData(models.Model):
    cat = models.ForeignKey(ProductCat, models.DO_NOTHING, db_column='cat', verbose_name='Κατηγορία')
    subcat = models.ForeignKey(ProductSubCategory, models.DO_NOTHING, db_column='subcat',
                                    verbose_name='Υποκατηγορία SalesInsight', primary_key=True)
    supplier_id = models.ForeignKey(SupplierDetail, models.DO_NOTHING, db_column='supplier_id',verbose_name='Προμηθευτής')
    itemstock = models.FloatField(null=False, verbose_name='Available stock')

    class Meta:
        managed=False
        db_table = 'itemstock'


class OptimizationItemForecast(models.Model):
    id = models.AutoField(primary_key=True)
    optimizationitem_id = models.ForeignKey(OptimizationItem, models.DO_NOTHING,db_column='optimizationitem_id')
    forecast_period = models.IntegerField(null=False)
    value = models.FloatField(null=False)
    model = models.CharField(max_length=50)
    seasonal_model = models.CharField(max_length=50)

    class Meta:
        managed=False
        db_table = 'OptimizationItemForecast'


class OptimizationItemResults(models.Model):
    id = models.AutoField(primary_key=True)
    optimizationitem_id = models.ForeignKey(OptimizationItem, models.DO_NOTHING,db_column='optimizationitem_id')
    supplier_id = models.ForeignKey(SupplierDetail, models.DO_NOTHING, db_column='supplier_id',verbose_name='Προμηθευτής')
    value = models.FloatField(null=False)

    class Meta:
        managed=True
        db_table = 'OptimizationItemResults'