# Generated by Django 3.1.5 on 2021-02-07 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210207_1929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'permissions': [('can_eat_pizzas', 'Can eat pizzas')]},
        ),
    ]
