# Generated by Django 4.2.8 on 2024-03-05 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


from django.contrib.auth.models import User

def create_superuser(apps, schema_editor):
    User.objects.create_superuser(username='iqube', email='iqubekct@gmail.com', password='iqube')
    User.objects.create_user(username='iqube1', email='iqubekct@gmail.com', password='iqube1')



class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_name', models.CharField(max_length=50)),
                ('instance_key', models.CharField(max_length=25)),
                ('instance_token', models.CharField(max_length=100)),
                ('qrscanned', models.BooleanField(default=False)),
                ('instance_created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12)),
                ('message_text', models.CharField(max_length=200)),
                ('message_time', models.DateTimeField(verbose_name='time sent')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging_app.instance')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Excel_sheet', models.CharField(max_length=100)),
                ('Started_at', models.DateTimeField()),
                ('Ended_at', models.DateTimeField()),
                ('Successful', models.BooleanField()),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging_app.instance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_superuser),
    ]
