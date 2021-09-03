from __future__ import print_function
import datetime

from celery.exceptions import Ignore
from ortools.linear_solver import pywraplp
import numpy as np
import os
import string
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db.models import F, Sum, FloatField, Case, When, Value, CharField, \
    DecimalField, \
    IntegerField, Avg
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task, task
from celery import app
from items.models import OptimizationItem, ProductDetail, ItemSup, Itemtrans, \
    OptimizationItemAttribute, \
    SupplierDetail, SupplierAttribute, Settings, ProductSubCategory, \
    OptimizationItemForecast, \
    FullItemStoreData, \
    OptimizationItemResults, Supplier
from items.functions import arima_run
from celery import shared_task
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True)
def missing_items(self):
    progress_recorder = ProgressRecorder(self)
    counter = 0
    dd = ProductDetail.objects.exclude(
        subcategory__in=OptimizationItem.objects.values_list('codeid', flat=True)).filter(
        subcategory__gte=20000000,
        subcategory__lte=30000000).values(
        'subcategory', 'subcategory__name').distinct()
    number_elements = dd.__len__()
    if dd:
        for i in dd:
            OptimizationItem(
                codeid=ProductSubCategory.objects.get(id=i.get('subcategory')),
                code=i.get('subcategory__name')).save()
            if counter == 0 or divmod(counter, 100)[1] == 0 or counter == number_elements:
                progress_recorder.set_progress(counter, number_elements)
            counter += 1
    else:
        counter = 0
    return counter


@shared_task(bind=True)
def update_atributes(self):
    warning = ""
    progress_recorder = ProgressRecorder(self)
    td = datetime.datetime.now() - relativedelta(years=+1)
    # d=ItemSup.objects.filter(product_id__subcategory__in=OptimizationItem.objects.values_list('codeid',flat=True))
    dd = pd.DataFrame(Itemtrans.objects.exclude(iteid__suppliers__isnull=True).filter(
        iteid__subcategory__in=OptimizationItem.objects.values_list('codeid', flat=True),
        iteid__suppliers__id__in=SupplierAttribute.objects.values_list('supplier_id',
                                                                       flat=True),
        source=5, fyeid=td.year).values('iteid__suppliers__id', 'iteid__subcategory',
                                        'iteid__cost__costvalue',
                                        'iteid__suppliers__category')
        .annotate(
        units_sold=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField()),
        value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField())))
    totals = pd.DataFrame(
        Itemtrans.objects.exclude(iteid__suppliers__isnull=True).filter(
            iteid__subcategory__gt=20000000,
            iteid__subcategory__lt=30000000,
            source=5, fyeid=td.year).values(
            'fyeid').annotate(
            units_sold=Sum(F('primaryqty') * F('outputquantmode'),
                           output_field=FloatField()),
            value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField())))
    monthly_q = pd.DataFrame(
        Itemtrans.objects.exclude(iteid__suppliers__isnull=True).filter(
            iteid__subcategory__in=OptimizationItem.objects.values_list('codeid',
                                                                        flat=True),
            iteid__suppliers__id__in=SupplierAttribute.objects.values_list('supplier_id',
                                                                           flat=True),
            source=5,
            fyeid=td.year)
            .values('iteid__suppliers__id', 'iteid__subcategory', 'fipid').annotate(
            units_sold=Sum(F('primaryqty') * F('outputquantmode'),
                           output_field=FloatField())))
    counter = 0
    Z = 1.28  # 90% coverage see: https://abcsupplychain.com/en/safety-stock-formula-calculation/
    lead_time = 2  # in months
    if dd.__len__() > 0:
        dd['unique_code'] = dd['iteid__subcategory'].astype(str) + '-' + dd[
            'iteid__suppliers__id'].astype(str)
        d_count = dd['unique_code'].value_counts()
        d_drop = dd[dd['unique_code'].isin(d_count[d_count.values > 1].index.values)]
        d_drop.to_csv(os.path.join(os.path.expanduser("~/Desktop"),
                                   'Duplicate_Suppliers' + datetime.datetime.now().strftime(
                                       '%Y-%m-%d_%H-%M-%S.csv')),
                      index=None, header=True)
        dd = dd.drop(d_drop.index)
        if d_drop.__len__() > 0:
            warning = "Duplicate supplier records where found for " + d_drop.__len__().__str__() + " occurences. The report was saved on your desktop. Attribute calculation was skipped for these items."
        d = list(dd.iteid__subcategory.unique())  # Subcategories distinct
        dd['annual_consumption_value'] = dd['iteid__cost__costvalue'] * dd['units_sold']
        dd['percent_acv'] = (dd[
                                 'annual_consumption_value'] / dd.annual_consumption_value.sum()) * 100
        dd['percent_au'] = (dd['units_sold'] / dd.units_sold.sum()) * 100
        dd_unique = pd.DataFrame(dd.iteid__subcategory.unique())
        dd_unique['percent_acv'] = 0
        dd_unique['percent_acv'] = dd_unique['percent_acv'].astype(float)
        for p in dd_unique.itertuples():
            dd_unique.at[p.Index, 'percent_acv'] = dd[dd['iteid__subcategory'] == p._1][
                'percent_acv'].sum()
        dd_unique = dd_unique.sort_values('percent_acv', ascending=False)
        dd_unique['percent_acv_cumsum'] = dd_unique['percent_acv'].cumsum()
        dd_unique['ABC'] = 0
        app_settings = Settings.objects.filter(id=1)
        dd_unique.at[
            dd_unique.percent_acv_cumsum <= app_settings[0].A_percent, 'ABC'] = 'A'
        dd_unique.at[
            (dd_unique.percent_acv_cumsum <= app_settings[0].A_percent + app_settings[
                0].B_percent) & (
                    dd_unique.percent_acv_cumsum > app_settings[
                0].A_percent), 'ABC'] = 'B'
        dd_unique.at[
            (dd_unique.percent_acv_cumsum > 100 - app_settings[0].C_percent), 'ABC'] = 'C'
        category_lastyear_sales = pd.DataFrame(
            Itemtrans.objects.filter(fyeid=td.year).values('iteid__subcategory', 'fyeid',
                                                           'fipid').annotate(
                value=Sum(F('trnvalue') * F('outputvalmode'), output_field=FloatField())))
        number_elements = d.__len__()
        for i in d:
            for row in dd[dd['iteid__subcategory'] == i].itertuples():
                OptimizationItemAttribute.objects.update_or_create(
                    optimizationitem_id=OptimizationItem.objects.get(codeid=i),
                    supplier_id=SupplierDetail.objects.get(id=row.iteid__suppliers__id),
                    defaults={'annual_consumption_value': row.annual_consumption_value,
                              'annual_units': row.units_sold,
                              'percent_acv': row.percent_acv,
                              'percent_au': row.percent_au,
                              'safetystock': Z * np.sqrt(lead_time) * np.std(
                                  monthly_q[(monthly_q[
                                                 'iteid__subcategory'] == i) & (
                                                    monthly_q[
                                                        'iteid__suppliers__id'] == row.iteid__suppliers__id)][
                                      'units_sold']),
                              'reorder_point': (Z * np.sqrt(lead_time) * np.std(
                                  monthly_q[(monthly_q[
                                                 'iteid__subcategory'] == i) & (
                                                    monthly_q[
                                                        'iteid__suppliers__id'] == row.iteid__suppliers__id)][
                                      'units_sold'])) + monthly_q[
                                                   (monthly_q[
                                                        'iteid__subcategory'] == i) & (
                                                           monthly_q[
                                                               'iteid__suppliers__id'] == row.iteid__suppliers__id)][
                                                   'units_sold'].mean() * lead_time})
            counter += 1
            cv = None
            mean_sales = \
            category_lastyear_sales[category_lastyear_sales.iteid__subcategory == i][
                'value'].mean()
            std_sales = np.std(
                category_lastyear_sales[category_lastyear_sales.iteid__subcategory == i][
                    'value'])
            if mean_sales != 0:
                cv = std_sales / mean_sales
            OptimizationItem.objects.filter(codeid=i).update(
                annual_units=dd[dd['iteid__subcategory'] == i]['units_sold'].sum(),
                annual_consumption_value=dd[dd['iteid__subcategory'] == i][
                    'annual_consumption_value'].sum(),
                percent_acv=dd_unique[dd_unique[0] == i]['percent_acv'],
                percent_au=dd[dd['iteid__subcategory'] == i]['percent_au'].sum(),
                ABC=dd_unique[dd_unique[0] == i]['ABC'].values[0],
                coeffv=cv,
                safetystock=Z * np.sqrt(lead_time) * np.std(
                    monthly_q[(monthly_q['iteid__subcategory'] == i)]['units_sold']),
                reorder_point=(Z * np.sqrt(lead_time) * np.std(
                    monthly_q[(monthly_q['iteid__subcategory'] == i)]['units_sold'])) +
                              monthly_q[(monthly_q['iteid__subcategory'] == i)][
                                  'units_sold'].mean() * lead_time)
            if counter == 0 or divmod(counter, 100)[1] == 0 or counter == number_elements:
                progress_recorder.set_progress(counter, number_elements)
    else:
        counter = 0
    return counter, warning


@shared_task(bind=True)
def optimize(self):
    if self.request.delivery_info['redelivered']:
        raise Ignore()
    progress_recorder = ProgressRecorder(self)
    OptimizationItemResults.objects.all().delete()
    months = 3
    oitems = OptimizationItem.objects.values().exclude(
        optimizationitemattribute__supplier_id__isnull=True)
    items_total = oitems.__len__()
    counter = 0
    t = list()
    for count, value in enumerate(oitems):  # είδη
        quantities = []
        constraints = []
        solver = pywraplp.Solver('SalesInsight', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        objective = solver.Objective()
        itemsupdata = OptimizationItemAttribute.objects.filter(
            optimizationitem_id__codeid=value['codeid_id'],
            supplier_id__itemsup__product_id__subcategory=value[
                'codeid_id']) \
            .values('id', 'optimizationitem_id_id', 'supplier_id_id', 'safetystock',
                    'annual_consumption_value',
                    'annual_units',
                    'percent_acv', 'percent_au', 'reorder_point',
                    'supplier_id__itemsup__lastbuysupprice')
        try:
            stock = FullItemStoreData.objects.filter(subcat=value['codeid_id']).values(
                'itemstock')[
                0].get('itemstock')
        except:
            stock = 0
        try:
            demand = OptimizationItemForecast.objects.filter(
                optimizationitem_id=value['id'],
                forecast_period__lte=months).aggregate(
                Sum(
                    'value')).get('value__sum')
        except:
            demand = 0

        if demand is None or demand == 0:
            continue

        # περιορισμός στοκ .1
        constraints.append(
            solver.Constraint(value['safetystock'] + demand - stock, solver.infinity()))
        for count2, value2 in enumerate(itemsupdata):  # προμηθευτές κάθε είδους
            quantities.append(
                solver.NumVar(0, solver.infinity(),
                              value['codeid_id'].__str__() + '-' + value2[
                                  'supplier_id_id'].__str__()))
            constraints[-1].SetCoefficient(quantities[-1], 1)
            objective.SetCoefficient(quantities[-1],
                                     9999 if value2[
                                                 'supplier_id__itemsup__lastbuysupprice'] is
                                             None else value2[
                                         'supplier_id__itemsup__lastbuysupprice'])
            counter += 1
        objective.SetMinimization()
        solver.Solve()
        a = OptimizationItemResults(
            optimizationitem_id=OptimizationItem.objects.get(id=value['id']),
            supplier_id=SupplierDetail.objects.get(id=value2[
                'supplier_id_id']),
            value=quantities[-1].solution_value())
        t.append(a)
        for o in quantities:
            print(
                o.name() + ' Proposed quantity: ' + o.solution_value().__str__() + ' Supplier Price: ' + objective.GetCoefficient(
                    o).__str__())
        print('Solved item ' + count.__str__() + ' of ' + items_total.__str__() + ': ' +
              value[
                  'codeid_id'].__str__() + ' Stock Constraint: ' + (
                      value['safetystock'] + demand - stock).__str__()
              + ' Stock ' + stock.__str__() + ' Demand ' + demand.__str__() + ' Safety Stock ' +
              value[
                  'safetystock'].__str__()
              )
        if count == 0 or divmod(count, 100)[1] == 0 or count == items_total:
            if t.__len__() > 0:
                OptimizationItemResults.objects.bulk_create(t)
                t.clear()
            progress_recorder.set_progress(count, items_total)
    return counter


@shared_task(bind=True)
def forecast(self):
    if self.request.delivery_info['redelivered']:
        raise Ignore()
    counter = 0
    progress_recorder = ProgressRecorder(self)
    OptimizationItemForecast.objects.all().delete()
    td = datetime.datetime.now() - relativedelta(years=+2)
    data1 = pd.DataFrame(Itemtrans.objects.filter(
        iteid__subcategory__in=OptimizationItem.objects.exclude(
            optimizationitemattribute__isnull=True).
            values('codeid')).values('iteid__subcategory', 'fyeid', 'fipid').annotate(
        value=Sum(F('primaryqty') * F('outputquantmode'), output_field=FloatField())))
    cats = data1.iteid__subcategory.unique()
    # cats = cats[0:102]
    number_elements = len(cats)
    t = list()
    for i in cats:
        try:
            counter += 1
            d = data1[data1.iteid__subcategory == i]
            d1, fc_series, lower_series, upper_series, series2 = arima_run(d,
                                                                           output=False)

            for j in range(1, fc_series.__len__()):
                a = OptimizationItemForecast(
                    optimizationitem_id=OptimizationItem.objects.get(codeid=i),
                    forecast_period=j,
                    value=fc_series[j], model=d1.order, seasonal_model=d1.seasonal_order)
                t.append(a)
                # OptimizationItemForecast.objects.create(optimizationitem_id=OptimizationItem.objects.get(codeid=i),forecast_period=j,
                # value=fc_series[j], model=d1.order, seasonal_model = d1.seasonal_order)
            if counter == 0 or divmod(counter, 100)[1] == 0 or counter == number_elements:
                if t.__len__() > 0:
                    OptimizationItemForecast.objects.bulk_create(t)
                    t.clear()
                progress_recorder.set_progress(counter, number_elements)
            print('Completed forecast for item ' + counter.__str__() + ' of ' + len(
                cats).__str__())
        except KeyboardInterrupt:
            break
        except Exception as e:
            continue
    sett = Settings.objects.get(id=1)
    sett.lastforecast = datetime.datetime.now()
    sett.save()
    return counter
