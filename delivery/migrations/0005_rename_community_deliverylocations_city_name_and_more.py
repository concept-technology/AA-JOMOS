# Generated by Django 5.0.6 on 2024-09-05 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_alter_deliverylocations_village'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliverylocations',
            old_name='community',
            new_name='city_name',
        ),
        migrations.RenameField(
            model_name='deliverylocations',
            old_name='village',
            new_name='town_name',
        ),
    ]
