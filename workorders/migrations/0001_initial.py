# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('official_name', models.CharField(max_length=80)),
                ('address', models.CharField(max_length=80)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True)),
                ('last_edited_by', models.CharField(null=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('official_name', models.CharField(max_length=80)),
                ('address', models.CharField(max_length=80)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True)),
                ('last_edited_by', models.CharField(null=True, max_length=50)),
                ('customer', models.ForeignKey(to='workorders.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=2)),
                ('crip', models.CharField(max_length=3)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True)),
                ('last_edited_by', models.CharField(null=True, max_length=50)),
                ('station', models.ForeignKey(to='workorders.Station')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=50)),
                ('station', models.CharField(max_length=50)),
                ('station_number', models.CharField(max_length=4)),
                ('terminal', models.CharField(max_length=2)),
                ('device', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True)),
                ('time_elapsed', models.CharField(max_length=20)),
                ('finish_date', models.DateTimeField(verbose_name='Job complete date')),
                ('work_assigned_to', models.CharField(null=True, max_length=50)),
                ('last_edited_by', models.CharField(null=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
