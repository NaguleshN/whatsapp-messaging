# Generated by Django 4.2.8 on 2024-03-08 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging_app', '0006_alter_whatsapp_config_excel_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='duration',
            field=models.DurationField(null=True),
        ),
    ]
