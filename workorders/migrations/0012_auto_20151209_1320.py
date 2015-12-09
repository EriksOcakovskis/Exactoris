# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0011_workorder_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorCause',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('code', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=80)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ErrorSymptom',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('code', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=80)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PerformedActions',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('code', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=80)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='workorder',
            name='call_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 9, 11, 20, 21, 424421, tzinfo=utc), verbose_name='Complaint date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workorder',
            name='err_cause_id',
            field=models.ForeignKey(to='workorders.ErrorCause', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workorder',
            name='err_symp_id',
            field=models.ForeignKey(to='workorders.ErrorSymptom', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workorder',
            name='field_eng_used',
            field=models.BooleanField(default=False, verbose_name='Rederected to field engineers?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workorder',
            name='perf_act_id',
            field=models.ForeignKey(to='workorders.PerformedActions', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workorder',
            name='rnd_used',
            field=models.BooleanField(default=False, verbose_name='Was RND used?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workorder',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workorder',
            name='work_assigned_to',
            field=models.ForeignKey(to='workorders.UserProfile', blank=True, null=True),
            preserve_default=True,
        ),
    ]
