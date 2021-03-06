"""
# Copyright (C) 2019-2020 Woods Hole Oceanographic Institution
#
# This file is part of the Roundabout Database project ("RDB" or 
# "ooicgsn-roundabout").
#
# ooicgsn-roundabout is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# ooicgsn-roundabout is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ooicgsn-roundabout in the COPYING.md file at the project root.
# If not, see <http://www.gnu.org/licenses/>.
"""

# Generated by Django 2.2.4 on 2019-10-14 14:48

from decimal import Decimal
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('doc_type', models.CharField(choices=[('Test', 'Test Documentation'), ('Design', 'Design Documentation')], max_length=20)),
                ('doc_link', models.CharField(max_length=1000)),
            ],
            options={
                'ordering': ['doc_type', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('friendly_name', models.CharField(blank=True, max_length=255)),
                ('revision', models.CharField(blank=True, max_length=100)),
                ('part_number', models.CharField(db_index=True, max_length=100)),
                ('unit_cost', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('refurbishment_cost', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('note', models.TextField(blank=True)),
                ('custom_fields', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision_code', models.CharField(db_index=True, default='A', max_length=255)),
                ('unit_cost', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('refurbishment_cost', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisions', to='parts.Part')),
            ],
            options={
                'ordering': ['-created_at', '-revision_code'],
            },
        ),
        migrations.CreateModel(
            name='PartType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='parts.PartType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='part',
            name='part_type',
            field=mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parts', to='parts.PartType'),
        ),
    ]
