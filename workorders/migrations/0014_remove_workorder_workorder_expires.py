# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0013_auto_20151210_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workorder',
            name='workorder_expires',
        ),
    ]
