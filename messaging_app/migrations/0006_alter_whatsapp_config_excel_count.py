# Generated by Django 4.2.8 on 2024-03-08 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging_app', '0005_whatsapp_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsapp_config',
            name='excel_count',
            field=models.PositiveIntegerField(),
        ),
    ]
