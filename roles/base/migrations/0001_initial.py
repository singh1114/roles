# Generated by Django 3.1.3 on 2020-11-29 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_type', models.IntegerField(choices=[('ACCESS', 3), ('AUDIT', 2), ('ACTION', 1)], default=1)),
                ('action', models.IntegerField(choices=[('TWEET', 1), ('LOGIN', 2), ('DELETE', 3), ('REQUESTED_CHANGE', 4), ('APPROVED', 5)], default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]