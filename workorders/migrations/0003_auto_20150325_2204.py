# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0002_station_station_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='station',
            old_name='station_number',
            new_name='number',
        ),
    ]
