# Generated by Django 5.2.1 on 2025-05-22 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0002_advertisement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={'verbose_name': 'Advertisement', 'verbose_name_plural': 'Advertisements'},
        ),
        migrations.AlterModelOptions(
            name='lead',
            options={'verbose_name': 'Lead', 'verbose_name_plural': 'Leads'},
        ),
    ]
