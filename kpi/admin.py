from django.contrib import admin
from kpi.models import AttributeTable,TransferTable,EntruSumTable,AdjustTable,IncomeTable,SalePriceTb,DispatchTable,\
    ScrappedToOutputTable,NuclearPriceTable
# Register your models here.


class IncomeAdmin(admin.ModelAdmin):
    """生产收货模型管理类"""
    list_per_page = 14  # 知道每页数量
    list_display = ["cod_number", "date", "ord_number", "ware", "quantity", "amount"]
    list_filter = ["ware"]
    search_fields = ["ord_number"]


class ScrappedAdmin(admin.ModelAdmin):
    """万元产值报废关系模型管理类"""
    list_per_page = 14  # 知道每页数量
    list_display = ["department", "ware", "ware2", "reason"]
    list_filter = ["ware"]
    search_fields = ["department"]


class AdjustTableAdmin(admin.ModelAdmin):
    """调整模型管理类"""
    list_per_page = 14  # 知道每页数量
    list_display = ["ord_number", "cod_number", "ware", "reason", "date", "quantity", "amount"]
    # list_filter = ["ware"]
    search_fields = ["cod_number"]


class SalePriceTbAdmin(admin.ModelAdmin):
    """销售价模型管理类"""
    list_per_page = 14  # 知道每页数量
    list_display = ["cod_number", "tax_price", "not_tax_price", "bnot_tax_price", "year"]
    # list_filter = ["ware"]
    search_fields = ["cod_number"]

class TransferTableAdmin(admin.ModelAdmin):
    """销售价模型管理类"""
    list_per_page = 14  # 知道每页数量
    list_display = ["cod_number", "ord_number", "quantity", "date", "out_ware", "in_ware"]
    search_fields = ["ord_number"]

class NuclearPriceTableAdmin(admin.ModelAdmin):
    """套餐价模型管理类"""
    list_per_page = 14  # 知道每页数量
    list_display = ["cod_number", "description", "name", "pac_price1","point1", "pac_price2","point2", "gua_price"]
    search_fields = ["cod_number"]

admin.site.register(IncomeTable, IncomeAdmin)
admin.site.register(ScrappedToOutputTable, ScrappedAdmin)
admin.site.register(SalePriceTb, SalePriceTbAdmin)
admin.site.register(AdjustTable, AdjustTableAdmin)
admin.site.register(TransferTable, TransferTableAdmin)
admin.site.register(NuclearPriceTable, NuclearPriceTableAdmin)


