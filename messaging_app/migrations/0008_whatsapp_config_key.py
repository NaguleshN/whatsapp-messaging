# Generated by Django 4.2.8 on 2024-03-08 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging_app', '0007_log_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatsapp_config',
            name='key',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
