# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0003_auto_20150325_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='crip',
            field=models.BooleanField(verbose_name='Is this a CRIP?'),
            preserve_default=True,
        ),
    ]
