# Generated by Django 4.1 on 2022-11-09 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_district_page_rename_tag_articletag_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='cover_image',
        ),
        migrations.AlterField(
            model_name='leadnews',
            name='position',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], unique=True),
        ),
    ]
