# Generated by Django 4.1 on 2022-11-15 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_alter_article_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_type',
            field=models.CharField(choices=[('home-page', 'Home'), ('detail-page', 'Detail'), ('category-page', 'Category')], default='', max_length=20),
        ),
    ]
