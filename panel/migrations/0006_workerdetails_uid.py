# Generated by Django 2.0 on 2018-11-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0005_workerdetails_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerdetails',
            name='uid',
            field=models.CharField(default='default', max_length=100000, null=True),
        ),
    ]
