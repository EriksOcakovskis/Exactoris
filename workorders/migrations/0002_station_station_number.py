# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='station_number',
            field=models.CharField(default=1234, max_length=4),
            preserve_default=False,
        ),
    ]
