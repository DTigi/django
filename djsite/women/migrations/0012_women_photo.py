# Generated by Django 4.2.6 on 2024-01-14 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0011_uploadfile_alter_women_managers_alter_women_cat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
