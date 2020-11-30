# Generated by Django 3.1.3 on 2020-11-29 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='status',
            field=models.IntegerField(choices=[('INITIATED', 1), ('APPROVED', 2), ('DELETED', 3)], default=2),
        ),
    ]
