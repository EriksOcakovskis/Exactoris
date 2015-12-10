# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import workorders.models


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0013_auto_20151210_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='workorder_expires',
            field=models.DateTimeField(default=workorders.models.WorkOrder.one_day_hence),
            preserve_default=True,
        ),
    ]
