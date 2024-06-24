# Generated by Django 4.2.13 on 2024-06-24 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('salary', models.IntegerField()),
                ('expedition_date', models.DateField()),
            ],
        ),
    ]