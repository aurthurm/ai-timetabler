# Generated by Django 3.0.2 on 2020-02-08 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_complexclass_complexschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='GAType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simple_ga', models.BooleanField(default=True)),
            ],
        ),
    ]
