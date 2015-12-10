# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0012_auto_20151209_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='device',
            field=models.ForeignKey(null=True, to='workorders.Device', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workorder',
            name='field_eng_used',
            field=models.BooleanField(verbose_name='Redirected to field engineers?', default=False),
            preserve_default=True,
        ),
    ]
