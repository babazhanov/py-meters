# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-20 08:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0005_auto_20181217_1532'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pe_profile',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='pe_profile',
            name='cell',
        ),
        migrations.AlterUniqueTogether(
            name='pi_profile',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='pi_profile',
            name='cell',
        ),
        migrations.AlterUniqueTogether(
            name='qe_profile',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='qe_profile',
            name='cell',
        ),
        migrations.AlterUniqueTogether(
            name='qi_profile',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='qi_profile',
            name='cell',
        ),
        migrations.DeleteModel(
            name='PE_Profile',
        ),
        migrations.DeleteModel(
            name='PI_Profile',
        ),
        migrations.DeleteModel(
            name='QE_Profile',
        ),
        migrations.DeleteModel(
            name='QI_Profile',
        ),
    ]
