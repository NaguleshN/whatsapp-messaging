# Generated by Django 4.2.8 on 2024-03-09 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging_app', '0012_alter_log_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='duration',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
