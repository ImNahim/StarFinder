# Generated by Django 3.1.5 on 2021-02-08 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starapp', '0006_auto_20210122_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='save',
            name='star_name',
            field=models.TextField(default='Nobody'),
        ),
    ]