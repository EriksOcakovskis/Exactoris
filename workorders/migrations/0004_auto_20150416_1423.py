# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0003_workorder_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='station',
            field=smart_selects.db_fields.ChainedForeignKey(to='workorders.Station'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workorder',
            name='terminal',
            field=smart_selects.db_fields.ChainedForeignKey(to='workorders.Terminal'),
            preserve_default=True,
        ),
    ]
