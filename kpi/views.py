from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection
import kpi.models as models
from kpi.models import TransferTable, IncomeTable, AdjustTable, SalePriceTb, AttributeTable, EntruSumTable, CostprojectTable,NuclearPriceTable
from django.core import serializers
import xlrd
from django.db import models
# import transaction
import xlwings as xw
import os
import time
import json
import itertools

def login_power(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.has_key("islogin"):
            # 用户已经登录，跳转首页
            return view_func(request, *args, **kwargs)
        else:
            return redirect("/login_ajax")

    return wrapper


def login_ajax(request):
    """登录"""
    if request.method == "GET":

        return render(request, "kpi/login_ajax.html")
    else:
        # 获取ajax post方式提交的数据
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "9313." and password == "qwe!23":
            response = JsonResponse({"res": 1})
            response.set_cookie("username", username, max_age=14 * 24 * 3600)
            request.session["islogin"] = True
            return response
        else:
            return JsonResponse({"res": 0})


def decrypt(request):
    """解密文件"""
    if request.method == "GET":
        return render(request, "kpi/decrypt.html")
    else:
        # 获取文件
        pic = request.FILES["pic"]

        # 创建一个文件
        # save_path = "%s/booktest/%s" % (settings.MEDIA_ROOT, pic.name)
        save_path = "E:/不常用工作/已解密文件/%s" % pic.name
        with open(save_path, "wb") as f:
            # 获取上传文件的内容并写入打开的文件
            for content in pic.chunks():
                f.write(content)
        # 复制一份文件放入桌面
        # save_path_desktop = "C:/Users/931304/Desktop/已解密文件/%s" % pic.name
        # with open(save_path_desktop, "wb") as f:
        #     for content in pic.chunks():
        #         f.write(content)
        # 返回
        return redirect("/decrypt")


@login_power
def index(request):
    """产入产量数据"""
    if request.method == "GET":
        date1 = "20200101"
        date2 = "20200101"
        context = {"date1": date1, "date2": date2}
        return render(request, "kpi/index.html", context)
    else:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        sql = """select c.id,c.ware,format(sum(c.quantity),0)quantity,format(sum(c.amount),2)amount from incometable as c 
                 where c.date between %s and %s group by c.ware order by sum(quantity);
                          """
        queryset = IncomeTable.objects.raw(sql, (date1, date2))
        context = {"content": queryset, "date1": date1, "date2": date2}
        return render(request, "kpi/index.html", context)


@login_power
def outcomedata(request):
    """产出产量数据"""
    if request.method == "GET":
        date1 = "20200101"
        date2 = "20200101"
        context = {"date1": date1, "date2": date2}
        return render(request, "kpi/outcomedata.html", context)
    else:
        date2 = request.POST.get("date2")
        date1 = request.POST.get("date1")
        year = str(date1)[0:4]
        sql = """select * from 
                        (select ifnull(a.cod_number,'总计') as cod_number,
                        ifnull(a.out_ware,'仓库汇总') as out_ware,id,
                        sum(quantity) as quantity_b ,format(sum(quantity),0)quantity,format(sum(amount),2)amount,format(sum(new_amount),2)new_amount,format(sum(not_tax_price),2)not_tax_amount,format(sum(bnot_tax_price),2)bnot_tax_amount from
                        (select c.id,c.out_ware as out_ware,c.cod_number as cod_number,sum(c.quantity) as quantity,sum(c.amount) as amount,sum(c.quantity*w.pla_price) as new_amount,
                        sum(c.quantity*x.not_tax_price) as not_tax_price,
                        (sum(c.quantity*x.not_tax_price)-ifnull(t.quantity*x.not_tax_price-t.quantity*x.bnot_tax_price,0)) as bnot_tax_price
                        from transfertable as c 
                        left join 
                        (select cod_number,sum(quantity) as quantity from entrusumtable where date between %s and %s group by cod_number) t 
                        on c.cod_number=t.cod_number
                        left join salepricetb as x on c.cod_number=x.cod_number and year=%s
                        left join  attributetable as w on w.cod_number=c.cod_number
                        where c.date between %s and %s
                        and c.out_ware in ('F10','F30','F40')
                        and c.ord_number not like "XF%%"
                        group by c.cod_number) as a
                        group by a.out_ware,a.cod_number with rollup) as b
                        order by b.out_ware,b.quantity_b;
                                  """
        queryset = TransferTable.objects.raw(sql, (date1, date2, year, date1, date2))
        context = {"content": queryset, "date1": date1, "date2": date2}
        return render(request, "kpi/outcomedata.html", context)


@login_power
def scrapped(request):
    """万元产值报废"""
    if request.method == "GET":
        date1 = "20200101"
        date2 = "20200101"
        context = {"date1": date1, "date2": date2}
        return render(request, "kpi/scrapped.html", context)
    else:
        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        # 只在最外一层使用format函数，不然会错误，format后加了千分符合已经不是数值了。
        sql = """select id,ii.dt, format((ii.amount-ifnull(ss.amount,0)),2) as amount, format(ifnull(aa.amount,0),2) as scrapped,
                    round(ifnull(aa.amount,0)*10000/(ii.amount-ifnull(ss.amount,0)),2) as scrapped_amount
                    from
                    (select id,s.department dt, sum(i.amount) as amount
                        from incometable as i
                        left join (select distinct ware,department from scrappedtooutputtable) as s
                        on i.ware=s.ware
                        where i.date between %s and %s
                        group by s.department
                        having dt is not null) ii
                    left join
                    (select s.department dt, sum(d.amount) as amount
                        from dispatchtable as d
                        left join (select distinct ware,ware2,department from scrappedtooutputtable) as s
                        on d.sfc_ware=s.ware
                        where d.date between %s and %s
                        and d.out_ware=s.ware2
                        group by s.department
                        having dt is not null) ss
                        on ii.dt=ss.dt
                    left join
                    (select s.department dt, -sum(a.amount) as amount
                        from adjusttable as a
                        left join (select distinct department,reason from scrappedtooutputtable) as s
                        on a.reason=s.reason
                        where a.date between %s and %s
                        group by s.department
                        having dt is not null) aa
                        on aa.dt=ii.dt
                    order by ii.dt desc,scrapped_amount;
                  """
        queryset = IncomeTable.objects.raw(sql, (date1, date2, date1, date2, date1, date2))
        context = {"content": queryset, "date1": date1, "date2": date2}
        return render(request, "kpi/scrapped.html", context)


@login_power
def entrust(request):
    """委托加工数据"""
    if request.method == "GET":
        date1 = "20200101"
        date2 = "20200101"
        context = {"date1": date1, "date2": date2}
        return render(request, "kpi/entrust.html", context)
    else:
        date2 = request.POST.get("date2")
        date1 = request.POST.get("date1")
        # 只在最外一层使用format函数，不然会错误，format后加了千分符合已经不是数值了。
        # 为什么需在加一次子查询，因为第一次查出的entruquantity是不能汇总，没有汇总值，如果需汇总值，就必须在汇总一次
        # 也可以考虑union加一列合并，而不使用子查询。
        sql = """select ifnull(tt.cod_number,"总计") cod_number,id,profession,name,description,
                    format(sum(tt.quantity),0) as quantity,format(sum(tt.entruquantity),0) as entruquantity
                    from 
                    (select z.cod_number as cod_number,
                        z.id,w.profession,w.name,w.description,sum(z.quantity) quantity,
                        ifnull(t.quantity,0) entruquantity
                        from transfertable as z left join attributetable as w on z.cod_number=w.cod_number 
                        left join 
                        (select cod_number,sum(quantity) as quantity 
                            from entrusumtable 
                            where date between %s and %s
                            group by cod_number) t 
                        on z.cod_number=t.cod_number
                        where z.date between %s and %s 
                        and z.out_ware in ("f10","f40","f30")
                        and z.ord_number not like "XF%%"
                        group by z.cod_number) as tt
                    group  by tt.cod_number with rollup
                    ;
              """
        queryset = IncomeTable.objects.raw(sql, (date1, date2, date1, date2))
        context = {"content": queryset, "date1": date1, "date2": date2}
        return render(request, "kpi/entrust.html", context)


@login_power
def costproject(request):
    """降成本项目数据"""
    if request.method == "GET":
        date1 = "20200101"
        date2 = "20200101"
        context = {"date1": date1, "date2": date2}
        return render(request, "kpi/costproject.html", context)
    else:
        date2 = request.POST.get("date2")
        date1 = request.POST.get("date1")

        sql = """
              
              """
        queryset = IncomeTable.objects.raw(sql, (date1, date2, date1, date2))
        context = {"content": queryset, "date1": date1, "date2": date2}
        return render(request, "kpi/costproject.html", context)


def upload(request):
    """:param request::return: 上传文件excel表格 ,并进行解析"""
    add_attr_list = []
    if request.method == "GET":
        return render(request, "kpi/upload.html")
    else:
        # 获取文件
        pic = request.FILES["pic"]
        save_path = "E:/不常用工作/已解密文件/%s" % pic.name
        with open(save_path, "wb") as f:
            # 获取上传文件的内容并写入打开的文件
            for content in pic.chunks():
                f.write(content)
        wb = xlrd.open_workbook(filename="E:/不常用工作/已解密文件/%s" % pic.name)  # 关键点在于这里
        table = wb.sheets()[0]
        nrows = table.nrows  # 行数
        # ncole = table.ncols  # 列数
        try:
            if pic.name == "costproject.xlsx":
                for i in range(1, nrows):
                    rs = table.row_values(i)  # 一行的数据
                    obj = CostprojectTable(department=rs[0], pro_name=rs[1], month=rs[2])
                    add_attr_list.append(obj)
                CostprojectTable.objects.bulk_create(add_attr_list)
                os.remove("E:/不常用工作/已解密文件/%s" % pic.name)
            else:
                os.remove("E:/不常用工作/已解密文件/%s" % pic.name)
                return JsonResponse({'msg': 'name_error'})
        except Exception as e:
            return JsonResponse({'msg': 'error'})
        return JsonResponse({'msg': 'ok'})

@login_power
def nuclear_price(request):
    if request.method == "GET":
        return render(request, "kpi/index.html")
    else:
        # 获取文件
        now =time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        pic = request.FILES["pic"]
        save_path = "E:/不常用工作/已解密文件/%s-%s" % (now,pic.name)
        with open(save_path, "wb") as f:
            # 获取上传文件的内容并写入打开的文件
            for content in pic.chunks():
                f.write(content)
    # 读取excel文件，写入列表
    data=xlrd.open_workbook(save_path)
    table=data.sheets()[0]
    rows=table.nrows            # 获取当前sheet页总行数，并把每一行数据作为list
    list1 =[]
    for i in range(rows):
        col = table.row_values(i)
        list1.append(col)

    # 读取mysql数据库写入列表
    sql = """select * from NuclearPriceTable;"""
    c_set=NuclearPriceTable.objects.all().values()
    response=list(c_set)
    list2=[]
    for i in range(len(response)):
        list_n=list(response[i].values())
        list2.append(list_n)

    # 列表与列表取数并计算结果
    sum_max = 0
    sum_gra = 0
    number = 0
    for i in range(1,len(list1)):
        for y in range(len(list2)):
            if list1[i][0] == list2[y][4]:
                list1[i].append(list2[y][3])  # 系列
                list1[i].append(list2[y][5])  # 名称
                list1[i].append(list2[y][6])  # 套餐价1
                list1[i].append(list2[y][8])  # 保本价
                list1[i].append(list2[y][9])  # 点位1
                list1[i].append(list2[y][7])  # 套餐价2
                list1[i].append(list2[y][10])  # 点位2
                # 再添加计算列，销售收入、销售收入(点位)、保本价、
                if list1[0][0].split("-")[1]=="版本1":
                    list1[i].append(round((float(list1[i][4]) * list1[i][1]), 2))
                    p_float =list1[i][6].split("%")[0]
                    p_float=float(p_float)/100
                    list1[i].append(round((float(list1[i][4]) * list1[i][1] * p_float), 2))
                    list1[i].append(round((float(list1[i][5]) * list1[i][1]), 2))
                    break
                elif list1[0][0].split("-")[1]=="版本2":
                    list1[i].append(round((float(list1[i][7]) * list1[i][1]), 2))
                    p_float = list1[i][8].split("%")[0]
                    p_float = float(p_float) / 100
                    list1[i].append(round((float(list1[i][7]) * list1[i][1] * p_float), 2))
                    list1[i].append(round((float(list1[i][5]) * list1[i][1]), 2))
                    break
                else:
                    return HttpResponse(json.dumps({'结果': '版本号错误'}, ensure_ascii=False),
                                        content_type="application/json")
            else:
                # 判断是不是list2循环最后一个，如果是，这list1中加入空值
                if y == len(list2) - 1:
                    for x in range(8):
                        list1[i].append(0)
                    return HttpResponse(json.dumps({'结果': '数据库中物料编码:%s没有' %list1[i][0] }, ensure_ascii=False), content_type="application/json")
        # 计算净利润，转换匹配结果，销售收入(点位)、保本价求和
        number += 1
        sum_max += list1[i][10]
        sum_gra += list1[i][11]
    # print(list1)
    # print(list2)
    profit=(sum_max-sum_gra)/1.13*0.85
    profit_lv=profit/sum_max*1.13

    print("销售收入:%f" % sum_max)
    print("保本价:%f" % sum_gra)
    print("利润率为:%f"% profit_lv)
    value_p=profit_lv-0.2
    if  value_p>=0:
        if 0<=value_p<=0.05:
            response1="达标（匹配度：高）"
        elif 0.05<value_p<=0.1:
            response1 = "达标（匹配度：中）"
        elif 0.1 < value_p:
            response1 = "达标（匹配度：低）"
    elif value_p<0:
        if -0.05<=value_p<0:
            response1="不达标（匹配度：高）"
        elif -0.1<=value_p<0.05:
            response1 = "不达标（匹配度：中）"
        elif -0.1 < value_p:
            response1 = "不达标（匹配度：低）"

    # return result
    # return render(request, "kpi/index.html",)
    response1={'结果': response1}
    return HttpResponse(json.dumps(response1,ensure_ascii=False),content_type="application/json")
    # return JsonResponse({'msg': response1},charset="utf-8")

@login_power
def nuclear_price_2(request):
    if request.method == "GET":
        return render(request, "kpi/index.html")
    else:
        # 获取文件
        now =time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        pic = request.FILES["pic"]
        save_path = "E:/不常用工作/已解密文件/%s-%s" % (now,pic.name)
        with open(save_path, "wb") as f:
            # 获取上传文件的内容并写入打开的文件
            for content in pic.chunks():
                f.write(content)
    # 读取excel文件，写入列表
    data=xlrd.open_workbook(save_path)
    table=data.sheets()[0]
    rows=table.nrows            # 获取当前sheet页总行数，并把每一行数据作为list
    list1 =[]
    for i in range(rows):
        col = table.row_values(i)
        list1.append(col)

    # 读取mysql数据库写入列表
    sql = """select * from NuclearPriceTable;"""
    c_set=NuclearPriceTable.objects.all().values()
    response=list(c_set)
    list2=[]
    for i in range(len(response)):
        list_n=list(response[i].values())
        list2.append(list_n)

    # 列表与列表取数并计算结果
    sum_max = 0
    sum_gra = 0
    number = 0
    sum_max_print =0
    sum_quantity=0
    for i in range(1,len(list1)):
        for y in range(len(list2)):
            if list1[i][0] == list2[y][4]:
                list1[i].append(list2[y][3])  # 系列
                list1[i].append(list2[y][5])  # 名称
                if list1[0][0].split("-")[1]=="版本1":
                    list1[i].append(list2[y][6])  # 套餐价1
                    list1[i].append(list2[y][9])  # 点位1
                elif list1[0][0].split("-")[1]=="版本2":
                    list1[i].append(list2[y][7])  # 套餐价2
                    list1[i].append(list2[y][10])  # 点位2
                else:
                    return HttpResponse(json.dumps({'结果': '版本号错误'}, ensure_ascii=False),
                                        content_type="application/json")
                list1[i].append(list2[y][8])  # 保本价
                # 再添加计算列，销售收入、销售收入(点位)、保本价、
                list1[i].append(round((float(list1[i][4]) * list1[i][1]), 2))
                p_float = float(list1[i][5].split("%")[0]) / 100
                list1[i].append(round((float(list1[i][4]) * list1[i][1] * p_float), 2))
                list1[i].append(round((float(list1[i][6]) * list1[i][1]), 2))
                break
            else:
                # 判断是不是list2循环最后一个，如果是，这list1中加入空值
                if y == len(list2) - 1:
                    for x in range(7):
                        list1[i].append(0)
                    return HttpResponse(json.dumps({'结果': '数据库中物料编码:%s没有' %list1[i][0] }, ensure_ascii=False), content_type="application/json")
        # 计算净利润，转换匹配结果，销售收入(点位)、保本价求和
        number += 1
        if i != 0:
            sum_quantity += list1[i][1]
        sum_max_print += list1[i][7]
        sum_max += list1[i][8]
        sum_gra += list1[i][9]

    # print(list1)
    # print(list2)
    profit=(sum_max-sum_gra)/1.13*0.85
    profit_lv=profit/sum_max*1.13
    # print("销售收入:%f" % sum_max)
    # print("保本价:%f" % sum_gra)
    # print("利润率为:%f"% profit_lv)

    if list1[0][0].split("-")[1] == "版本1":
        value_p=profit_lv-0.2
    else:
        value_p = profit_lv - 0.3
    print(value_p)
    if  value_p>=0:
        if 0<=value_p<=0.05:
            response1="达标（匹配度：高）"
        elif 0.05<value_p<=0.1:
            response1 = "达标（匹配度：中）"
        elif value_p > 0.1:
            response1 = "达标（匹配度：低）"
    elif value_p<0:
        if -0.05<=value_p<0:
            response1="不达标（匹配度：高）"
        elif -0.1<=value_p<0.05:
            response1 = "不达标（匹配度：中）"
        elif value_p < -0.1:
            response1 = "不达标（匹配度：低）"
    else:
        response1 = "无匹配"

    list1.append(["汇总", sum_quantity, "", "%s%s%%" %(response1,round(profit_lv,4)*100), "", "", "", "", "", sum_max_print, ""])
    list1=list1[1:]
    context = {"content": list1}
    return render(request, "kpi/index.html",context)
    # response1={'结果': response1}
    # return HttpResponse(json.dumps(response1,ensure_ascii=False),content_type="application/json")
    # return JsonResponse({'msg': response1},c harset="utf-8")


