# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True)),
                ('last_edited_by', models.CharField(max_length=50, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True)),
                ('last_edited_by', models.CharField(max_length=50, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('summary', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True, null=True)),
                ('registered', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('complete_date', models.DateTimeField(blank=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('prerequisite_description', models.TextField(blank=True, null=True)),
                ('last_edited', models.DateTimeField(auto_now=True)),
                ('last_edited_by', models.CharField(max_length=50, null=True)),
                ('commentary', models.TextField(blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, to='tasks.UserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='prerequisite',
            field=models.ForeignKey(to='tasks.Task'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.ForeignKey(to='tasks.Priority'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(to='tasks.Status'),
            preserve_default=True,
        ),
    ]
