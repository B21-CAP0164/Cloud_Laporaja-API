# Generated by Django 3.2.3 on 2021-06-01 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_user_fk_report_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=-6.2, max_digits=9),
        ),
        migrations.AddField(
            model_name='report',
            name='long',
            field=models.DecimalField(decimal_places=6, default=106.816666, max_digits=9),
        ),
    ]
