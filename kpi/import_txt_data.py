import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "financial.settings")
django.setup()
from kpi.models import AttributeTable, TransferTable, EntruSumTable, AdjustTable, IncomeTable, SalePriceTb, \
    DispatchTable, ScrappedToOutputTable as SOT, NuclearPriceTable

add_attr_list = []
file_name = input("请输入要导入的txt文件名称:")
with open('../static/kpi/files/%s.txt' % file_name) as f:
    next(f)  # 从文件的第二行开始读起
    if file_name == "transfertable":
        for line in f:
            lt = line.split("	")
            # 转移订单表导入
            # cod_number = AttributeTable.objects.get(cod_number=lt[1])
            obj = TransferTable(
                ord_number=lt[0], cod_number=lt[1], quantity=lt[2], amount=lt[3], date=lt[4], out_ware=lt[5],
                in_ware=lt[6])
            add_attr_list.append(obj)
        TransferTable.objects.bulk_create(add_attr_list)

    elif file_name == "attributetable":
        for line in f:
            lt = line.split("	")
            # 属性表导入
            obj = AttributeTable(
                cod_number=lt[0], name=lt[1], type=lt[2], unit=lt[3], pur_price=lt[4], pla_price=lt[5],
                mat_group=lt[6], dra_number=lt[7], profession=lt[8], virtual=lt[9], description=lt[10])
            add_attr_list.append(obj)
        AttributeTable.objects.bulk_create(add_attr_list)

    elif file_name == "entrusumtable":
        for line in f:
            lt = line.split("	")
            # 委托加工表导入
            """如果使用了外键，使用ORM插入数据时，插入的外键必须是外键关联表Attributetable中的instance(实例)
            ORM:object Relational Mapping 想像操作对象一样操作数据库"""
            # cod_number = AttributeTable.objects.get(cod_number=lt[1])
            obj = EntruSumTable(
                date=lt[0], cod_number=lt[1], entru_number=lt[2], quantity=lt[3])
            add_attr_list.append(obj)
        EntruSumTable.objects.bulk_create(add_attr_list)

    elif file_name == "adjusttable":
        for line in f:
            lt = line.split("	")
            # 调整订单表导入
            # cod_number = AttributeTable.objects.get(cod_number=lt[1])
            obj = AdjustTable(
                ord_number=lt[0], cod_number=lt[1], ware=lt[2], reason=lt[3], date=lt[4], quantity=lt[5], amount=lt[6])
            add_attr_list.append(obj)
        AdjustTable.objects.bulk_create(add_attr_list)

    elif file_name == "incometable":
        for line in f:
            lt = line.split("	")
            # 生产收货表导入
            # cod_number = AttributeTable.objects.get(cod_number=lt[0])
            obj = IncomeTable(
                cod_number=lt[0], date=lt[1], ord_number=lt[2], ware=lt[3], quantity=lt[4], amount=lt[5])
            add_attr_list.append(obj)
        IncomeTable.objects.bulk_create(add_attr_list)

    elif file_name == "salepricetb":
        for line in f:
            lt = line.split("	")
            # 销售价表导入
            obj = SalePriceTb(
                cod_number=lt[0], tax_price=lt[1], not_tax_price=lt[2], bnot_tax_price=lt[3], year=lt[4])
            add_attr_list.append(obj)
        SalePriceTb.objects.bulk_create(add_attr_list)

    elif file_name == "dispatchtable":
        for line in f:
            lt = line.split("	")
            # 生产发料表导入
            obj = DispatchTable(
                cod_number=lt[0], date=lt[1], ord_number=lt[2], sfc_ware=lt[3], out_ware=lt[4], quantity=lt[5],
                amount=lt[6])
            add_attr_list.append(obj)
        DispatchTable.objects.bulk_create(add_attr_list)

    elif file_name == "scrappedtooutputtable":
        for line in f:
            lt = line.split("	")
            # 万元产值报废关系表导入
            obj = SOT(
                department=lt[0], ware=lt[1], reason=lt[2], ware_w=lt[3], ware_a=lt[4])
            add_attr_list.append(obj)
        SOT.objects.bulk_create(add_attr_list)

    elif file_name == "NuclearPriceTable":
        for line in f:
            lt = line.split("	")
            # 万元产值报废关系表导入
            obj = NuclearPriceTable(
                version1=lt[0], version2 =lt[1], description=lt[2], cod_number=lt[3], name=lt[4],pac_price1=lt[5],
                pac_price2=lt[6],gua_price=lt[7],point1=lt[8],point2=lt[9])
            add_attr_list.append(obj)
        NuclearPriceTable.objects.bulk_create(add_attr_list)


    else:
        print("输入表名有误")
