# Generated by Django 4.0 on 2023-08-04 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_announcement_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='accept',
            field=models.BooleanField(default=False),
        ),
    ]
