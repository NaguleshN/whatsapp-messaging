# Generated by Django 4.2.8 on 2024-03-08 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging_app', '0002_rename_ended_at_log_ended_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='ended_at',
            field=models.DateTimeField(null=True),
        ),
    ]
