# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20160105_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurrenceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('complete_date', models.DateTimeField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('assigned_to', models.ForeignKey(to='tasks.UserProfile', blank=True, null=True)),
                ('task', models.ForeignKey(to='tasks.Task', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='dateof_recurrence',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='recurring',
            field=models.BooleanField(default=False, verbose_name='Is the task recurring?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='typeof_recurrence',
            field=models.ForeignKey(to='tasks.RecurrenceType', blank=True, null=True),
            preserve_default=True,
        ),
    ]
