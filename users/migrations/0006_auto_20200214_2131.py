# Generated by Django 3.0.3 on 2020-02-14 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200214_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_secret',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]