from django.db import models


class AttributeTable(models.Model):
    cod_number = models.CharField(verbose_name="物料代码", max_length=20, db_index=True, unique=True)
    name = models.CharField(verbose_name="物料名称", max_length=50)
    type = models.CharField(verbose_name="类型", max_length=4)
    unit = models.CharField(verbose_name="单位", max_length=3, null=True)
    pur_price = models.DecimalField(verbose_name="采购价", max_digits=10, decimal_places=2)
    pla_price = models.DecimalField(verbose_name="计划价", max_digits=10, decimal_places=2)
    mat_group = models.CharField(verbose_name="物料组", max_length=6)
    dra_number = models.CharField(verbose_name="图号", max_length=20, null=True)
    profession = models.CharField(verbose_name="专业", max_length=2, null=True)
    virtual = models.CharField(verbose_name="虚拟", max_length=4, null=True)
    description = models.CharField(verbose_name="说明", max_length=20, null=True)

    def __str__(self):
        return self.cod_number

    class Meta:
        db_table = "attributetable"


class TransferTable(models.Model):
    ord_number = models.CharField(max_length=20, null=True)
    cod_number = models.CharField(max_length=20, db_index=True, default=None)
    # cod_number = models.ForeignKey(to="AttributeTable", to_field="cod_number",
    #                                blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    out_ware = models.CharField(max_length=6)
    in_ware = models.CharField(max_length=7)

    def __str__(self):
        return str(self.cod_number)

    class Meta:
        db_table = "transfertable"


class EntruSumTable(models.Model):
    date = models.DateField()
    cod_number = models.CharField(max_length=20, db_index=True, default=None)
    # cod_number = models.ForeignKey(to="AttributeTable", to_field="cod_number",
    #                                blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    entru_number = models.CharField(max_length=15)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.cod_number)

    class Meta:
        db_table = "entrusumtable"


class AdjustTable(models.Model):
    ord_number = models.CharField(max_length=20, null=True)
    cod_number = models.CharField(max_length=20, default=None, db_index=True)
    # cod_number = models.ForeignKey(to="AttributeTable", to_field="cod_number",
    #                                blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    ware = models.CharField(max_length=6)
    reason = models.CharField(max_length=6)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.cod_number)

    class Meta:
        db_table = "adjusttable"


class IncomeTable(models.Model):
    cod_number = models.CharField(max_length=20, default=None, db_index=True)
    # cod_number = models.ForeignKey(to="AttributeTable", to_field="cod_number",
    #                                blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    date = models.DateField()
    ord_number = models.CharField(max_length=20, null=True)
    ware = models.CharField(max_length=6)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    amount = models.DecimalField(max_digits=12, decimal_places=4)

    def __str__(self):
        return str(self.cod_number)

    class Meta:
        db_table = "incometable"


class SalePriceTb(models.Model):
    cod_number = models.CharField(max_length=20, db_index=True, default=None)
    # cod_number = models.ForeignKey(to="AttributeTable", to_field="cod_number",
    #                                blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    tax_price = models.DecimalField(max_digits=10, decimal_places=2)
    not_tax_price = models.DecimalField(max_digits=10, decimal_places=2)
    bnot_tax_price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()

    def __str__(self):
        return str(self.cod_number)

    class Meta:
        db_table = "salepricetb"


class DispatchTable(models.Model):
    cod_number = models.CharField(max_length=20, default=None)
    # cod_number = models.ForeignKey(to="AttributeTable", to_field="cod_number",
    #                                blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    date = models.DateField()
    ord_number = models.CharField(max_length=20, null=True)
    sfc_ware = models.CharField(max_length=6)
    out_ware = models.CharField(max_length=6, db_index=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.cod_number)

    class Meta:
        db_table = "dispatchtable"


class ScrappedToOutputTable(models.Model):
    department = models.CharField(max_length=6)
    ware = models.CharField(max_length=6, null=True, blank=True, db_index=True)
    ware2 = models.CharField(max_length=6, default=None, null=True, blank=True)
    ware_a = models.CharField(max_length=6, default=None, null=True, blank=True)
    reason = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return str(self.department)

    class Meta:
        db_table = "scrappedtooutputtable"


class CostprojectTable(models.Model):
    department = models.CharField(max_length=6)
    pro_name = models.CharField(max_length=6, null=True, blank=True, db_index=True)
    month = models.CharField(max_length=6, default=None, null=True, blank=True)
    # cooperation = models.CharField(max_length=6, default=None, null=True, blank=True)
    # pioneer = models.CharField(max_length=6, null=True, blank=True)
    # sort = models.CharField(max_length=6, null=True, blank=True)
    # est_benefit = models.CharField(max_length=6, null=True, blank=True)
    # act_benefit = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return str(self.department)

    class Meta:
        db_table = "CostprojectTable"

class NuclearPriceTable(models.Model):
    version1 = models.CharField(max_length=20)
    version2 = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    description = models.CharField(max_length=20, default=None, null=True, blank=True)
    cod_number = models.CharField(verbose_name="物料代码", max_length=20, db_index=True, unique=True)
    name = models.CharField(verbose_name="物料名称", max_length=50)
    pac_price1 = models.DecimalField(verbose_name="套餐价1", max_digits=10, decimal_places=2)
    pac_price2 = models.DecimalField(verbose_name="套餐价2", max_digits=10, decimal_places=2)
    gua_price= models.DecimalField(verbose_name="保本价", max_digits=10, decimal_places=2)
    point1= models.CharField(verbose_name="点位1", max_length=10)
    point2= models.CharField(verbose_name="点位2", max_length=10)

    def __str__(self):
        return str(self.cod_number)

    class Meta:
        db_table = "NuclearPriceTable"

