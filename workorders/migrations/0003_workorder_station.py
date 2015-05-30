# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0002_remove_workorder_station'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='station',
            field=models.ForeignKey(to='workorders.Station', default='1'),
            preserve_default=False,
        ),
    ]
