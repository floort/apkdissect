# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-28 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APK',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apk', models.FileField(upload_to=b'apks/')),
                ('sha256', models.CharField(db_index=True, max_length=64)),
                ('md5', models.CharField(db_index=True, max_length=32)),
                ('name', models.CharField(max_length=256, null=True)),
                ('permissions_loaded', models.BooleanField(default=False)),
                ('decompiled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=256)),
                ('apk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apk.APK')),
            ],
        ),
        migrations.CreateModel(
            name='BugTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DalvikClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('javasource', models.TextField()),
                ('apk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apk.APK')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=256)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sha256', models.CharField(db_index=True, max_length=64)),
                ('apk', models.FileField(upload_to=b'apks/')),
            ],
        ),
        migrations.CreateModel(
            name='ImportBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apk.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='app',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apk.ImportBatch'),
        ),
        migrations.AddField(
            model_name='apk',
            name='bug_tags',
            field=models.ManyToManyField(to='apk.BugTag'),
        ),
        migrations.AddField(
            model_name='apk',
            name='permissions',
            field=models.ManyToManyField(to='apk.Permission'),
        ),
    ]