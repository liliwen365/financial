# Generated by Django 3.0.4 on 2020-12-21 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi', '0002_nuclearpricetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nuclearpricetable',
            name='point1',
            field=models.CharField(max_length=10, verbose_name='点位1'),
        ),
        migrations.AlterField(
            model_name='nuclearpricetable',
            name='point2',
            field=models.CharField(max_length=10, verbose_name='点位2'),
        ),
    ]