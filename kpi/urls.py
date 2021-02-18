from django.urls import path, include, re_path
from kpi import views
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^index$', views.index),
    re_path(r'^login_ajax$', views.login_ajax),
    re_path(r'^outcomedata$', views.outcomedata),
    re_path(r'^decrypt$', views.decrypt),
    re_path(r'^scrapped$', views.scrapped),
    re_path(r'^entrust$', views.entrust),
    re_path(r'^costproject$', views.costproject),
    re_path(r'^upload$', views.upload),
    re_path(r'^nuclear_price$', views.nuclear_price_2),
]
