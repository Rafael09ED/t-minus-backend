# Generated by Django 2.1.4 on 2019-08-10 05:26

import api.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('time', models.DateTimeField()),
                ('key', models.CharField(default=api.models.generateKey, max_length=64)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='CountdownEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('text', models.CharField(max_length=256)),
                ('time_delta', models.DurationField()),
                ('countdown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Countdown')),
            ],
        ),
    ]