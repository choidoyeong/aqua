# Generated by Django 2.2 on 2019-04-15 06:25

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mains', '0004_auto_20190412_1719'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('weight',)},
        ),
        migrations.AlterModelOptions(
            name='scrap',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='water',
            options={'ordering': ['date']},
        ),
        migrations.AddField(
            model_name='scrap',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='water',
            unique_together={('user', 'date')},
        ),
    ]
