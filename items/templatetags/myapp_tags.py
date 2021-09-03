from django import template
from items.models import FullItemStoreData, ItemSup
from django.db.models import Sum

register = template.Library()

@register.filter(name='get_obj_attr')
def get_obj_attr(obj, attr):
    if type(obj)==dict:
        if attr.lower()=='itemstock' and not 'optimizationitem__supplier_id' in obj.items() :
            return FullItemStoreData.objects.filter(subcat=obj['id']).values('subcat').annotate(total=Sum('itemstock')).values('total')[0].get('total')
        elif attr.lower()=='itemstock' and 'optimizationitem__supplier_id' in obj.items():
            return FullItemStoreData.objects.filter(subcat=obj['id'],supplier_id=obj['optimizationitem__supplier_id']).values('subcat').annotate(total=Sum('itemstock')).values('total')[0].get('total')
        else:
            g = [value for key, value in obj.items() if attr.lower() in key.lower()]
            if g.__len__() > 0:

                return g[0]
            else:
                return None
    else:
        return obj.__getattribute__(attr)

@register.simple_tag
def get_verbose_field_name(obj, field):
    """
    Returns verbose_name for a field.
    """
    try:
        return obj._meta.get_field(field).verbose_name
    except:
        return field

@register.simple_tag
def get_help_text(obj, field):
    """
    Returns help_text for a field.
    """
    try:
        return obj._meta.get_field(field).help_text
    except:
        return field


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag(name='get_supstock')
def get_supstock(supplier, subcat):
    try:
        d = FullItemStoreData.objects.filter(supplier_id__code=supplier,subcat=subcat).values('itemstock')[0].get('itemstock')
    except:
        d = 0
    return d


@register.simple_tag(name='get_supprice')
def get_supstock(supplier, subcat):
    try:
        d = ItemSup.objects.filter(supplier_id__code=supplier,product_id__subcategory=subcat).values('lastbuysupprice')[0].get('lastbuysupprice')
    except:
        d = 0
    return d


@register.simple_tag(name='get_supcatstock')
def get_supcatstock(supcat, subcat):
    try:
        d = FullItemStoreData.objects.filter(supplier_id__category__name=supcat,subcat=subcat).values('subcat').annotate(total=Sum('itemstock')).values('total')[0].get('total')
    except:
        d = 0
    return d
