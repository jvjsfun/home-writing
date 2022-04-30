# Generated by Django 2.1.4 on 2018-12-30 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importexport', '0002_auto_20181229_2201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='snippet',
            options={'ordering': ['date', 'status']},
        ),
        migrations.AlterField(
            model_name='snippet',
            name='status',
            field=models.IntegerField(choices=[(0, 'queued'), (1, 'processing'), (2, 'error'), (3, 'accepted')], default=0),
        ),
    ]