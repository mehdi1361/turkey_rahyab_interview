# Generated by Django 4.0 on 2023-08-02 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_remove_useraccount_is_student_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.useraccount')),
            ],
            options={
                'db_table': 'announcement',
            },
        ),
    ]