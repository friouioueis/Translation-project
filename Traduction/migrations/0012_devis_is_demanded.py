# Generated by Django 2.2.9 on 2020-01-26 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Traduction', '0011_devis_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='devis',
            name='is_demanded',
            field=models.BooleanField(default=False),
        ),
    ]