# Generated by Django 2.2.4 on 2021-03-30 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landr_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='password', max_length=50),
            preserve_default=False,
        ),
    ]
