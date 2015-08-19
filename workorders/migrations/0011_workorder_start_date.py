# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0010_workorder_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='start_date',
            field=models.DateTimeField(default='2015-08-01 12:30'),
            preserve_default=False,
        ),
    ]
