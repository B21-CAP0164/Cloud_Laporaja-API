# Generated by Django 3.2.3 on 2021-06-02 12:50

from django.db import migrations, models
import core.models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_id')
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='image',
            field=models.FileField(upload_to=core.models.get_file_path, default=None, blank=True, null=True),
        ),
    ]
