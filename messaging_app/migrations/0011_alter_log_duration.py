# Generated by Django 4.2.8 on 2024-03-09 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging_app', '0010_alter_log_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='duration',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
