# Generated by Django 4.2.3 on 2023-08-01 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alert_cache', '0002_capfeedalertdistrict_capfeeddistrict_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='capfeedalert',
            options={'managed': False},
        ),
        migrations.AlterModelTable(
            name='capfeedalertdistrict',
            table='cap_feed_alertdistrict',
        ),
    ]
