# Generated by Django 4.2 on 2023-04-19 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(editable=False, max_length=50, unique=True),
        ),
    ]