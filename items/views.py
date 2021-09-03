import json
from django.db.models import F, Sum, FloatField, Case, When, Value, CharField, DecimalField, IntegerField, Avg, OuterRef, Subquery
from django.db.models.functions import Left
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView, DetailView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import datetime
from items.forms import SupplierForm, ImportProductForm, SettingsForm
from items.models import ProductFilter, SupplierFilter, SuppBalance, ProductCategoryFilter, ProductSubCategory,  CeleryTasks
from items.tables import ProductTable, SupplierTable,ProductCategoryTable,ProductSubCategoryListTable
from .functions import sales_plot, gauge_plot, sunburst_plot, plotly_table, objforecast_plot, dist_plot
from .models import Itemtrans, ProductDetail, Product, Supplier, SupplierDetail, Customer, CustomerDetail, \
    CustomerFilter, ItemFinData,ProductCategory, ProductSubcategoryFilter, ProductSubCategoryList, OptimizationItem, OptimizationItemAttribute, Settings, \
    SupplierCategory, FullItemStoreData
from dateutil.relativedelta import relativedelta
from items.tasks import missing_items, update_atributes, forecast, optimize
import pandas as pd


# Create your views here.

def SettingsView(request):
    template_name = "settings.html"
    context = {}
    if request.method == "GET":
        pending_task=False
        if CeleryTasks.objects.filter(status='PROGRESS'):
            pending_task=True
        queryset = Settings.objects.get(pk=1)
        context = {'pending_task': pending_task, 'QuerySet': queryset }
        return render(request, template_name, context)
    elif request.method == "POST":
        content = json.loads(request.body)
        try:
            g = Settings.objects.get(pk=1)
            g.A_percent = content["A_percent"]
            g.B_percent = content["B_percent"]
            g.C_percent = content["C_percent"]
            g.save()
            context = {'success': True}
        except:
            context = {'success': False}
        finally:
            return render(request, template_name, context)


def actionview(request):
    template_name = "action.html"
    form_class = SupplierForm
    context = {'form': form_class}
    return render(request, template_name, context)


def ImportProducts(request):
    if request.method == 'GET':
        result = missing_items.delay()
        data = {
            'task_id': result.task_id
        }
        return HttpResponse(json.dumps({"task_id": result.task_id}),content_type="application/json")
        #return render(request, 'action.html', context={'task_id': result.task_id, 'form': ImportProductForm})
    else:
        return HttpResponse("Request method is not a GET")


def UpdateAttributes(request):
    if request.method == 'GET':
        result = update_atributes.delay()
        data = {
            'task_id': result.task_id
        }
        return HttpResponse(json.dumps({"task_id": result.task_id}),content_type="application/json")
        #return render(request, 'action.html', context={'task_id': result.task_id, 'form': ImportProductForm})
    else:
        return HttpResponse("Request method is not a GET")


def UpdateForecast(request):
    if request.method == 'GET':
        result = forecast.delay()
        data = {
            'task_id': result.task_id
        }
        return HttpResponse(json.dumps({"task_id": result.task_id}),content_type="application/json")
        #return render(request, 'action.html', context={'task_id': result.task_id, 'form': ImportProductForm})
    else:
        return HttpResponse("Request method is not a GET")

def Optimize(request):
    if request.method == 'GET':
        result = optimize.delay()
        data = {
            'task_id': result.task_id
        }
        return HttpResponse(json.dumps({"task_id": result.task_id}),content_type="application/json")
        #return render(request, 'action.html', context={'task_id': result.task_id, 'form': ImportProductForm})
    else:
        return HttpResponse("Request method is not a GET")


class ProductListView(SingleTableMixin, FilterView):
    table_class = ProductTable
    queryset = Product.objects.all().order_by('-valuey0')
    template_name = "index.html"
    filterset_class = ProductFilter


class ProductCategoryListView(SingleTableMixin, FilterView):
    template_name = "index.html"
    table_class = ProductCategoryTable
    filterset_class = ProductCategoryFilter
    #filterset_class = ProductCategoryFilter

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data(**kwargs)
        queryset = ProductCategory.objects.all().order_by('-valuey0')
        context['table'] = ProductCategoryTable(queryset)
        return context


class ProductSubCategoryListView(SingleTableMixin, FilterView):
    template_name = "index.html"
    queryset = ProductSubCategoryList.objects.all().order_by('-valuey0')
    table_class = ProductSubCategoryListTable
    filterset_class = ProductSubcategoryFilter
    #filterset_class = ProductCategoryFilter


class SupplierListView(SingleTableMixin, FilterView):
    table_class = SupplierTable
    queryset = Supplier.objects.all().order_by('-valuey0')
    template_name = "index.html"
    filterset_class = SupplierFilter


class CustomerListView(SingleTableMixin, FilterView):
    table_class = SupplierTable
    queryset = Customer.objects.all().order_by('-valuey0')
    template_name = "index.html"
    filterset_class = CustomerFilter


class ProductDetailView(DetailView):
    model = ProductDetail
    fields = [field.name for field in ProductDetail._meta.concrete_fields]
    template_name = "details.html"

    def get_queryset(self):
        return ProductDetail.objects.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        td = datetime.datetime(2020,12,31) - relativedelta(months=+1) #datetime.datetime(2020,12,31).month
        value_gauge_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], source=5, fipid__lt=td.month).values('iteid','fyeid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField())).order_by('-fyeid')
        div = gauge_plot(value_gauge_data,"Sales Value Jan-"+td.strftime("%b")+" ("+str(datetime.datetime(2020,12,31).year-1)+"-"+str(datetime.datetime(2020,12,31).year)+")")
        value_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], source=5, fipid__lt=td.month).values('iteid', 'fyeid').annotate(
            value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField())).order_by('-fyeid')
        div2 = gauge_plot(value_gauge2_data, "Sales Units Jan-"+td.strftime("%b")+" ("+str(datetime.datetime(2020,12,31).year-1)+"-"+str(datetime.datetime(2020,12,31).year)+")")
        #value1_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
       # value2_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year-1, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
        #div2 = gauge_plot(value1_gauge2_data,"  ")
        context['graph'] = div
        context['graph2'] = div2
        v=value_gauge_data[0].get('value')/value_gauge2_data[0].get('value')
        context['field1'] = v
        c=ItemFinData.objects.filter(masterid=self.kwargs['pk']).values('costvalue')[0].get('costvalue') #datetime.datetime(2020,12,31).year
        d1 = list(Itemtrans.objects.select_related().filter(iteid=self.kwargs['pk'], source=5, fyeid=td.year).values(
            'perid__code', 'fyeid', 'perid__name'). \
            annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()),
                     domorex=Case(When(perid__code__startswith='8', then=Value('export'))
                                  , default=Value('domestic'), output_field=CharField())).order_by('-fyeid'))
        div3=sunburst_plot(d1, 'test')                           #datetime.datetime(2020,12,31).month
        d = list(Itemtrans.objects.all().filter(iteid=self.kwargs['pk'], source=5, fipid__lt=td.month).values('fyeid').annotate(
            value=Sum(F('trnvalue') * F('outputvalmode'), output_field=IntegerField())).order_by('fyeid'))

        for i in d:
            if d.index(i) == 0:
                i['yoy'] = str("-%")
                i['color']=('rgb(255,255,255)')
                continue
            else:
                i['yoy'] = ((i['value'] / d[d.index(i) - 1]['value']) - 1)*100
                if i['yoy']>0:
                    i['color']='rgb(152,251,152)'
                else:
                    i['color']='rgb(255,99,71)'
                i['yoy']=str(int(round(i['yoy'])))+"%"
        div4=plotly_table(d)
        context['graph4'] = div4
        context['graph3'] = div3
        context['field2'] = v-c
        context['field22'] = (1-(c/v))*100
        # context['panel'] = acp[0] + acp[1]
        return context


class ProductSubCategoryDetailView(DetailView):
    model = ProductSubCategory
    fields = [field.name for field in ProductSubCategory._meta.concrete_fields]
    fields.extend([field.name for field in OptimizationItem._meta.concrete_fields])
    fields.extend([field.name for field in FullItemStoreData._meta.concrete_fields])
    template_name = "details.html"

    def get_queryset(self):
        return ProductSubCategory.objects.filter(id=self.kwargs['pk']).values('id','name','optimizationitem__annual_consumption_value',
                                                                         'optimizationitem__annual_units','optimizationitem__percent_acv',
                                                                              'optimizationitem__percent_au','optimizationitem__safetystock',
                                                                              'optimizationitem__ABC', 'optimizationitem__coeffv','optimizationitem__reorder_point').\
            annotate(itemstock=Sum(1, output_field=FloatField()))

    def get_context_data(self, **kwargs):
        context = super(ProductSubCategoryDetailView, self).get_context_data(**kwargs)
        context['fields'] = self.fields                                                                 #datetime.datetime(2020,12,31).month
        td = datetime.datetime(2020,12,31) - relativedelta(months=+1)
        value_gauge_data = Itemtrans.objects.filter(iteid__subcategory=self.kwargs['pk'], source=5, fipid__lt=td.month).values('iteid__subcategory','fyeid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField())).order_by('-fyeid')
        div = gauge_plot(value_gauge_data,"Sales Value Jan-"+td.strftime("%b")+" ("+str(datetime.datetime(2020,12,31).year-1)+"-"+str(datetime.datetime(2020,12,31).year)+")")
        value_gauge2_data = Itemtrans.objects.filter(iteid__subcategory=self.kwargs['pk'], source=5, fipid__lt=td.month).values('iteid__subcategory', 'fyeid').annotate(
            value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField())).order_by('-fyeid')
        div2 = gauge_plot(value_gauge2_data, "Sales Units Jan-"+td.strftime("%b")+" ("+str(datetime.datetime(2020,12,31).year-1)+"-"+str(datetime.datetime(2020,12,31).year)+")")
        #value1_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
        #value2_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year-1, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
        #div2 = gauge_plot(value1_gauge2_data,"  ")
        context['graph'] = div
        context['graph2'] = div2
        v=value_gauge_data[0].get('value')/value_gauge2_data[0].get('value')
        context['field1'] = v
        c=ProductDetail.objects.filter(subcategory=self.kwargs['pk'], cost__costvalue__gt=0).values('subcategory').annotate(value=Avg(F('cost__costvalue')))[0].get('value')
        d1 = list(Itemtrans.objects.select_related().filter(iteid__subcategory=self.kwargs['pk'], source=5, fyeid=td.year).values(
            'perid__code', 'fyeid', 'perid__name'). \
            annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()),
                     domorex=Case(When(perid__code__startswith='8', then=Value('export'))
                                  , default=Value('domestic'), output_field=CharField())).order_by('-fyeid'))
        div3=sunburst_plot(d1,'test')                           #datetime.datetime(2020,12,31).month
        div5=dist_plot(pd.DataFrame(Itemtrans.objects.values('iteid__subcategory', 'fyeid', 'fipid').filter(source=5,iteid__subcategory=self.kwargs['pk']).annotate(
            Quantity=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField()))),"")
        d = list(Itemtrans.objects.all().filter(iteid__subcategory=self.kwargs['pk'], source=5, fipid__lt=td.month).values('fyeid').annotate(
            value=Sum(F('trnvalue') * F('outputvalmode'), output_field=IntegerField())).order_by('fyeid'))
        for i in d:
            if d.index(i) == 0:
                i['yoy'] = str("-%")
                i['color']=('rgb(255,255,255)')
                continue
            else:
                i['yoy'] = ((i['value'] / d[d.index(i) - 1]['value']) - 1)*100
                if i['yoy']>0:
                    i['color']='rgb(152,251,152)'
                else:
                    i['color']='rgb(255,99,71)'
                i['yoy']=str(int(round(i['yoy'])))+"%"
        div4=plotly_table(d)
        context['graph4'] = div4
        context['graph3'] = div3
        context['graph5'] = div5
        context['field2'] = v-c
        context['field22'] = (1-(c/v))*100
        #a = FullItemStoreData.objects.filter(subcat=OuterRef('optimizationitem_id__codeid'),subcat__supplier__id=OuterRef('optimizationitem_id__supplier_id')).values('subcat').annotate(stock=Sum('itemstock', output_field=FloatField())).values('stock')
        oi_attributes = OptimizationItemAttribute.objects.filter(optimizationitem_id__codeid=self.kwargs['pk'],
                                                                 optimizationitem_id__supplier__in=OptimizationItem.objects.filter(codeid=self.kwargs['pk']).values('supplier__id')).\
            values('supplier_id__code', 'supplier_id__name','supplier_id__category__name','annual_consumption_value',
                   'annual_units', 'safetystock','percent_acv','percent_au','reorder_point').annotate(
                     itemstock=Sum(1, output_field=FloatField()),itemprice=Sum(1, output_field=FloatField()))
        oi_suppliers_distinct = OptimizationItemAttribute.objects.filter(optimizationitem_id__codeid=self.kwargs['pk']).\
            values('supplier_id__name','supplier_id__category__name').distinct()
        oi_supplier_categories = OptimizationItemAttribute.objects.filter(
            optimizationitem_id__codeid=self.kwargs['pk']).values('supplier_id__category__name').distinct()
        oi_supplier_cat_attributes = SupplierCategory.objects.filter(supplierdetail__optimizationitem__codeid=self.kwargs['pk']).values('name').\
            annotate(annual_consumption_value=Sum('supplierdetail__optimizationitemattribute__annual_consumption_value'),
                     annual_units=Sum('supplierdetail__optimizationitemattribute__annual_units'),
                     safetystock=Sum('supplierdetail__optimizationitemattribute__safetystock'),
                     percent_acv=Sum('supplierdetail__optimizationitemattribute__percent_acv'),
                     percent_au=Sum('supplierdetail__optimizationitemattribute__percent_au'),
                     reorder_point=Sum('supplierdetail__optimizationitemattribute__reorder_point'),
                     itemstock=Sum(1, output_field=FloatField()))
        oi_attributes_fields={'supplier_id__code':'Supplier code','supplier_id__name':'Supplier Name',
                              'supplier_id__category':'Supplier salesinsight category','annual_consumption_value':'Annual consumption value','annual_units':'Annual units sold',
                              'safetystock':'Safety stock','percent_acv':'Percent from total annual consumption value',
                              'percent_au':'Percent from total annual units sold',
                              'reorder_point':'Reorder point', 'itemstock':'Available stock', 'itemprice':'Last price'}
        context['oi_attributes'] = oi_attributes
        context['oi_suppliers_distinct'] = oi_suppliers_distinct
        context['oi_supplier_categories'] = oi_supplier_categories
        context['oi_supplier_cat_attributes'] = oi_supplier_cat_attributes
        context['oi_attributes_fields'] = oi_attributes_fields
        # context['panel'] = acp[0] + acp[1]
        return context



class ProductCategoryDetailView(DetailView):
    model = ProductCategory
    fields = [f.name for f in ProductCategory._meta.concrete_fields if not f.name.__contains__('value')]
    template_name = "details.html"

    def get_queryset(self):
        return ProductCategory.objects.filter(category=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryDetailView, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        td = datetime.datetime(2020,12,31) - relativedelta(months=+1)
        value_gauge_data = Itemtrans.objects.filter(iteid__category__codeid__exact=self.kwargs['pk'], source=5, fipid__lt=datetime.datetime(2020,12,31).month).values('fyeid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField())).order_by('-fyeid')

        div = gauge_plot(value_gauge_data,"Sales Value Jan-"+td.strftime("%b")+" ("+str(datetime.datetime(2020,12,31).year-1)+"-"+str(datetime.datetime(2020,12,31).year)+")")
        value_gauge2_data = Itemtrans.objects.filter(iteid__category__codeid__exact=self.kwargs['pk'], source=5, fipid__lt=datetime.datetime(2020,12,31).month).values( 'fyeid').annotate(
            value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField())).order_by('-fyeid')
        div2 = gauge_plot(value_gauge2_data, "Sales Units Jan-"+td.strftime("%b")+" ("+str(datetime.datetime(2020,12,31).year-1)+"-"+str(datetime.datetime(2020,12,31).year)+")")
        #value1_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
       # value2_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year-1, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
        #div2 = gauge_plot(value1_gauge2_data,"  ")
        context['graph'] = div
        context['graph2'] = div2
        v = value_gauge_data[0].get('value')/value_gauge2_data[0].get('value')
        context['field1'] = v
        c = ProductDetail.objects.filter(category=102).values('category').annotate(s=Avg('cost__costvalue'))[0]['s']
        d1 = list(Itemtrans.objects.select_related().filter(iteid__category__codeid__exact=self.kwargs['pk'], source=5,
                                                            fyeid=datetime.datetime(2020,12,31).year).values(
            'perid__code', 'fyeid', 'perid__name').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()),
                     domorex= Case(When(perid__code__startswith='8', then=Value('export'))
                                  , default= Value('domestic'), output_field=CharField())).order_by('-fyeid'))
        div3 = sunburst_plot(d1,'test')
        d = list(Itemtrans.objects.all().filter(iteid__category__codeid__exact=self.kwargs['pk'], source=5, fipid__lt=datetime.datetime(2020,12,31).month).values('fyeid').annotate(
            value=Sum(F('trnvalue') * F('outputvalmode'), output_field=IntegerField())))
        for i in d:
            if d.index(i) == 0:
                i['yoy'] = str("-%")
                i['color'] = ('rgb(255,255,255)')
                continue
            else:
                i['yoy'] = ((i['value'] / d[d.index(i) - 1]['value']) - 1)*100
                if i['yoy'] > 0:
                    i['color'] = 'rgb(152,251,152)'
                else:
                    i['color'] = 'rgb(255,99,71)'
                i['yoy'] = str(int(round(i['yoy'])))+"%"
        div4=plotly_table(d)
        context['graph4'] = div4
        context['graph3'] = div3
        context['field2'] = v-c
        context['field22'] = (1-(c/v))*100
        # context['panel'] = acp[0] + acp[1]
        return context


class SupplierDetailView(UpdateView):
    model = SupplierDetail
    fields = [field.name for field in SupplierDetail._meta.concrete_fields]
    template_name = "details.html"

    def get_queryset(self):
        return SupplierDetail.objects.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(SupplierDetailView, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        try:
            value_gauge_data = SuppBalance.objects.filter(supid=self.kwargs['pk'], fipid__lt=datetime.datetime(2020,12,31).month).values('fyeid').annotate(value=Sum('masterperiodturnover')).order_by('-fyeid')
            td = datetime.datetime(2020,12,31) - relativedelta(months=+1)
            div = gauge_plot(value_gauge_data,"Sales Value Jan-"+td.strftime("%b")+" ("+str(datetime.datetime(2020,12,31).year-1)+"-"+str(datetime.datetime(2020,12,31).year)+")")
            # value_gauge2_data = Itemtrans.objects.filter(perid=self.kwargs['pk'], source=5, fipid__lt=datetime.datetime(2020,12,31).month).values('iteid', 'fyeid').annotate(
            #     value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField())).order_by('-fyeid')
            # div2 = gauge_plot(value_gauge2_data, "Sales Units Jan-"+td.strftime("%b")+" ("+str(datetime.datetime(2020,12,31).year-1)+"-"+str(datetime.datetime(2020,12,31).year)+")")
            #value1_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
           # value2_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year-1, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
            #div2 = gauge_plot(value1_gauge2_data,"  ")
            context['graph'] = div
            # context['graph2'] = div2
            # v=value_gauge_data[0].get('value')/value_gauge2_data[0].get('value')
            # context['field1'] = v
            # c=ItemFinData.objects.filter(masterid=self.kwargs['pk']).values('costvalue')[0].get('costvalue')
            # d1 = list(Itemtrans.objects.select_related().filter(perid=self.kwargs['pk'], source=5, fyeid=datetime.datetime(2020,12,31).year).values(
            #     'perid__code', 'fyeid', 'perid__name'). \
            #     annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()),
            #              domorex=Case(When(perid__code__startswith='8', then=Value('export'))
            #                           , default=Value('domestic'), output_field=CharField())).order_by('-fyeid'))
            # div3=sunburst_plot(d1,'test')
            d = list(value_gauge_data)

            for i in d:
                if d.index(i) == 0:
                    i['yoy'] = str("-%")
                    i['color']=('rgb(255,255,255)')
                    continue
                else:
                    i['yoy'] = ((i['value'] / d[d.index(i) - 1]['value']) - 1)*100
                    if i['yoy']>0:
                        i['color']='rgb(152,251,152)'
                    else:
                        i['color']='rgb(255,99,71)'
                    i['yoy']=str(int(round(i['yoy'])))+"%"
            div4=plotly_table(d)
            context['graph4'] = div4
            #context['graph3'] = div3
            # context['panel'] = acp[0] + acp[1]
        finally:
            return context


class CustomerDetailView(UpdateView):
    model = CustomerDetail
    fields = [field.name for field in CustomerDetail._meta.concrete_fields]
    template_name = "details.html"

    def get_queryset(self):
        return CustomerDetail.objects.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        try:
            value_gauge_data = Itemtrans.objects.filter(perid=self.kwargs['pk'], source=5,
                                                        fipid__lt=datetime.datetime(2020,12,31).month).values('perid',
                                                                                                        'fyeid').annotate(
                value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField())).order_by('-fyeid')
            td = datetime.datetime(2020,12,31) - relativedelta(months=+1)
            div = gauge_plot(value_gauge_data, "Sales Value Jan-" + td.strftime("%b") + " (" + str(
                datetime.datetime(2020,12,31).year - 1) + "-" + str(datetime.datetime(2020,12,31).year) + ")")
            value_gauge2_data = Itemtrans.objects.filter(perid=self.kwargs['pk'], source=5,
                                                         fipid__lt=datetime.datetime(2020,12,31).month).values('perid',
                                                                                                         'fyeid').annotate(
                value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField())).order_by('-fyeid')
            div2 = gauge_plot(value_gauge2_data, "Sales Units Jan-" + td.strftime("%b") + " (" + str(
                datetime.datetime(2020,12,31).year - 1) + "-" + str(datetime.datetime(2020,12,31).year) + ")")
            # value1_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
            # value2_gauge2_data = Itemtrans.objects.filter(iteid=self.kwargs['pk'], fyeid=datetime.datetime(2020,12,31).year-1, fipid__lte=datetime.datetime(2020,12,31).month).values('iteid').annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
            # div2 = gauge_plot(value1_gauge2_data,"  ")
            context['graph'] = div
            context['graph2'] = div2
            # v = value_gauge_data[0].get('value') / value_gauge2_data[0].get('value')
            # context['field1'] = v
            # c = ItemFinData.objects.filter(masterid=self.kwargs['pk']).values('costvalue')[0].get('costvalue')
            d1 = list(Itemtrans.objects.select_related().filter(perid=self.kwargs['pk'], source=5,
                                                                fyeid=datetime.datetime(2020,12,31).year).values(
                'iteid__code', 'fyeid', 'iteid__name', 'iteid__category__descr'). \
                      annotate(value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField())).order_by('-fyeid'))
            div3 = sunburst_plot(d1, 'test', type=2)
            d = list(Itemtrans.objects.all().filter(perid=self.kwargs['pk'], source=5,
                                                    fipid__lt=datetime.datetime(2020,12,31).month).values('fyeid').annotate(
                value=Sum(F('trnvalue') * F('outputvalmode'), output_field=IntegerField())).order_by('fyeid'))

            for i in d:
                if d.index(i) == 0:
                    i['yoy'] = str("-%")
                    i['color'] = ('rgb(255,255,255)')
                    continue
                else:
                    if d[d.index(i) - 1]['value'] != 0:
                        i['yoy'] = ((i['value'] / d[d.index(i) - 1]['value']) - 1) * 100
                    else:
                        i['yoy'] = 100
                    if i['yoy'] > 0:
                        i['color'] = 'rgb(152,251,152)'
                    else:
                        i['color'] = 'rgb(255,99,71)'
                    i['yoy'] = str(int(round(i['yoy']))) + "%"
            div4 = plotly_table(d)
            context['graph4'] = div4
            context['graph3'] = div3
            #context['field2'] = v - c
            #context['field22'] = (1 - (c / v)) * 100
            # context['panel'] = acp[0] + acp[1]
        finally:
            return context



def objectsalesview(request, pk):
    template_name = "sales.html"
    if request.path.__contains__("suppliers"):
        plot_data1 = SuppBalance.objects.filter(supid=pk).values('fyeid', 'fipid').annotate(
            value=Sum(F('masterperiodturnover'), output_field=FloatField()))
        obj = Supplier.objects.filter(id=pk)
    elif request.path.__contains__("customers"):
        plot_data1 = Itemtrans.objects.filter(perid=pk).values('fyeid', 'fipid').annotate(
            value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
        obj = Customer.objects.filter(id=pk)
    elif request.path.__contains__("itemsubcategories"):
        plot_data1 = Itemtrans.objects.filter(iteid__subcategory=pk).values('fyeid', 'fipid').annotate(
            value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
        obj = ProductSubCategory.objects.filter(id=pk)
    else:
        plot_data1 = Itemtrans.objects.filter(iteid=pk).values('fyeid', 'fipid').annotate(
            value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField()))
        obj = Product.objects.filter(id=pk)
    div, div2 = sales_plot(plot_data1)
    context = {'graph': div2, 'graph2': div, 'object': obj[0]}
    return render(request, template_name, context)

def objectforecastview(request, pk):
    template_name = "objforecast.html"
    if request.path.__contains__("suppliers"):
        plot_data1 = SuppBalance.objects.filter(supid=pk, fyeid__lte=2020).values('fyeid', 'fipid').annotate(
            value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField()))
        obj = Supplier.objects.filter(id=pk)
    elif request.path.__contains__("customers"):
        plot_data1 = Itemtrans.objects.filter(perid=pk, fyeid__lte=2020).values('fyeid', 'fipid').annotate(
            value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField()))
        obj = Customer.objects.filter(id=pk)
    #elif request.path.__contains__("itemsubcategories"):
    elif request.path.__contains__("itemsubcategories"):
        plot_data1 = Itemtrans.objects.filter(iteid__subcategory=pk, fyeid__lte=2020).values('fyeid', 'fipid').annotate(
            value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField()))
        obj = ProductSubCategory.objects.filter(id=pk)
    else:
        plot_data1 = Itemtrans.objects.filter(iteid=pk, fyeid__lte=2020).values('fyeid', 'fipid').annotate(
            value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField()))
        obj = Product.objects.filter(id=pk)
    div, div2, arimamodel, fc_series = objforecast_plot(plot_data1)
    context = {'graph': div,'graph2': div2,'object': obj[0], 'arimamodel': arimamodel, 'graph3':plotly_table(fc_series, 2)}
    return render(request, template_name, context)
