# Generated by Django 4.2.1 on 2023-09-16 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout_app', '0003_alter_search_city_alter_search_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='zip_code',
            field=models.IntegerField(),
        ),
    ]