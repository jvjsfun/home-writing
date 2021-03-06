# Generated by Django 2.1.4 on 2018-12-29 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importexport', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='snippet',
            options={'ordering': ['date']},
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='data',
        ),
        migrations.AddField(
            model_name='snippet',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='snippet',
            name='profile',
            field=models.IntegerField(blank=True, choices=[(1, 'lorenzo.writing'), (2, 'benni.wolf09')], null=True),
        ),
        migrations.AddField(
            model_name='snippet',
            name='title',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='status',
            field=models.IntegerField(choices=[(0, 'queued'), (1, 'ready'), (3, 'error'), (2, 'accepted')], default=0),
        ),
    ]
