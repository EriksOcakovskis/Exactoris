# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0014_workorder_workorder_expires'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workorder',
            name='workorder_expires',
        ),
    ]
