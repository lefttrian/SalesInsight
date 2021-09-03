from django.contrib import admin
from .models import SupplierAttribute, SupplierCategory,  ItemSup, ProductSubCategory
# Register your models here.


class SupplierAttributeAdmin(admin.ModelAdmin):
    model = SupplierAttribute
    list_display  = ['get_supplier_id__name', 'get_suppliercategory_id__name']
    list_filter = ['suppliercategory_id']

    def get_supplier_id__name(self, obj):
        return obj.supplier_id.name
    get_supplier_id__name.admin_order_field = 'supplier_id__name'
    get_supplier_id__name.short_description = 'Supplier'

    def get_suppliercategory_id__name(self, obj):
        return obj.suppliercategory_id.name
    get_suppliercategory_id__name.admin_order_field = 'suppliercategory_id__name'
    get_suppliercategory_id__name.short_description = 'Category'


# class ItemSupInline(admin.TabularInline):
#     model = ItemSup
#     extra = 1
#
#
# class ProductSubcategoryAdmin(admin.ModelAdmin):
#     model = ProductSubcategory
#     search_fields = ['descr']
#
#
# class ProductAttributeAdmin(admin.ModelAdmin):
#     model = ProductAttribute
#     autocomplete_fields  = ["productsubcategory_id"]
#     list_display = ['get_productsubcategory_id__name']
#     inlines = [ItemSupInline]
#
#     def get_productsubcategory_id__name(self, obj):
#         return obj.productsubcategory_id.descr
#     get_productsubcategory_id__name.order_field='productsubcategory_id__descr'
#     get_productsubcategory_id__name.short_description = 'Product'

admin.site.register(SupplierAttribute, SupplierAttributeAdmin)
admin.site.register(SupplierCategory)

admin.site.site_header = 'SalesInsight Administration'