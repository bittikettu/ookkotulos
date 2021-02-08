# Generated by Django 3.1.5 on 2021-02-07 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsCancelled',
            fields=[
                ('eventsjoined_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.eventsjoined')),
            ],
            bases=('app.eventsjoined',),
        ),
        migrations.RenameField(
            model_name='eventsjoined',
            old_name='date_joined',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='eventsjoined',
            name='Peruutus',
        ),
        migrations.RemoveField(
            model_name='eventsjoined',
            name='date_cancel',
        ),
        migrations.AddField(
            model_name='event',
            name='memberscancelled',
            field=models.ManyToManyField(blank=True, default=None, related_name='cancels', through='app.EventsCancelled', to=settings.AUTH_USER_MODEL),
        ),
    ]
