# Generated by Django 2.1.3 on 2019-03-06 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importexport', '0004_auto_20190215_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='username',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]