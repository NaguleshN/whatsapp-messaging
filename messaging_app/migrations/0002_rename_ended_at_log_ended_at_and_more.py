# Generated by Django 4.2.8 on 2024-03-06 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='Ended_at',
            new_name='ended_at',
        ),
        migrations.RenameField(
            model_name='log',
            old_name='Excel_sheet',
            new_name='excel_sheet',
        ),
        migrations.RenameField(
            model_name='log',
            old_name='Started_at',
            new_name='started_at',
        ),
        migrations.RenameField(
            model_name='log',
            old_name='Successful',
            new_name='successfull',
        ),
    ]