# Generated by Django 5.1.1 on 2024-09-14 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_comment_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='top_selling',
        ),
        migrations.DeleteModel(
            name='Product_like',
        ),
    ]
