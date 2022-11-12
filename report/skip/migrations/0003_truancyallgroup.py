# Generated by Django 4.1.2 on 2022-10-18 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skip', '0002_rename_group_truancy_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='TruancyAllGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('absenteeism', models.IntegerField(verbose_name='Общее Количество отсутствующих')),
                ('percent', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Общий Процент от общего числа')),
                ('num_hours', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Общее Количество Часов')),
            ],
        ),
    ]
