# Generated by Django 2.2.9 on 2020-01-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Traduction', '0015_auto_20200126_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='assertmente',
            field=models.FileField(blank=True, null=True, upload_to='files/assermente/'),
        ),
    ]