# Generated by Django 3.2.23 on 2023-12-02 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to='blog.Profile'),
        ),
    ]
