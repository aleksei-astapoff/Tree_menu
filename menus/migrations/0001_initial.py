# Generated by Django 5.0.7 on 2024-07-24 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('url', models.CharField(blank=True, max_length=200, verbose_name='URL')),
                ('named_url', models.CharField(blank=True, max_length=200, verbose_name='Наименование URL')),
                ('menu_name', models.CharField(max_length=100, verbose_name='Название меню')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menus.menuitem', verbose_name='Предыдущий элемент меню')),
            ],
            options={
                'verbose_name': 'Элемент меню',
                'verbose_name_plural': 'Элементы меню',
            },
        ),
    ]
