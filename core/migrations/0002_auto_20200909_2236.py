# Generated by Django 3.1.1 on 2020-09-09 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ManyToManyField(to='core.Category'),
        ),
    ]
