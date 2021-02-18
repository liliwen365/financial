import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "financial.settings")
django.setup()
import xlrd
from django.http import HttpResponse, JsonResponse
from django.db import models
import transaction
from django.shortcuts import render, redirect
from kpi.models import CostprojectTable
import xlwings as xw


""":param request::return: 上传文件excel表格 ,并进行解析"""
# file_name = input("请输入要导入的excel文件名称:")
# wb = xlrd.open_workbook(filename="D:/env/myenv1/project/financial/static/kpi/files/项目测试.xlsx")  # 关键点在于这里
# table = wb.sheets()[0]


app = xw.App(visible=False, add_book=False)
app.display_alerts = False
app.screen_updating = False
file_path = r"D:/env/myenv1/project/financial/static/kpi/files/项目测试.xlsx"
wb = app.books.open(file_path)
sht = wb.sheets["Sheet1"]
a = sht.range("A2").expand().value
print(a)
CostprojectTable.objects.create(department=a[0][0], pro_name=a[0][1]
                                      , month=a[0][2])


wb.close()
app.quit()


# nrows = table.nrows  # 行数
# for i in range(1, nrows):
#     rowValues = table.row_values(i)  # 一行的数据
#     print(rowValues)
#     CostprojectTable.objects.create(department=rowValues[0], pro_name=rowValues[1]
#                                     , month=rowValues[2])
