# Generated by Django 4.0.6 on 2022-09-30 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='banner',
            field=models.ImageField(upload_to='banners/', verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_fav',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
