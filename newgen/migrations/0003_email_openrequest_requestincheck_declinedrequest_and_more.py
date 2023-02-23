# Generated by Django 4.1.4 on 2023-01-25 05:51

from django.db import migrations, models
import django.db.models.deletion
import newgen.models


class Migration(migrations.Migration):

    dependencies = [
        ('newgen', '0002_urgencystatus_alter_shedule_target_objects_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('email_id', models.IntegerField(default=newgen.models.Email.number, primary_key=True, serialize=False, verbose_name='Номер email')),
                ('email', models.CharField(max_length=40, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
            },
        ),
        migrations.CreateModel(
            name='OpenRequest',
            fields=[
                ('note_id', models.IntegerField(default=newgen.models.OpenRequest.number, primary_key=True, serialize=False, verbose_name='Номер записи')),
                ('organisation', models.CharField(max_length=50, verbose_name='Организация')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('problem_description', models.CharField(max_length=200, verbose_name='Описание проблемы')),
                ('date', models.DateField(verbose_name='Дата')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.email', verbose_name='Email')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.urgencystatus', verbose_name='Статус срочности')),
            ],
            options={
                'verbose_name': 'Открытая заявка',
                'verbose_name_plural': 'Открытые заявки',
            },
        ),
        migrations.CreateModel(
            name='RequestInCheck',
            fields=[
                ('note_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Номер записи')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('open_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.openrequest', verbose_name='Открытая заявка')),
            ],
            options={
                'verbose_name': 'Закрыта заявка в ожидании',
                'verbose_name_plural': 'Закрытые заявки в ожидании',
            },
        ),
        migrations.CreateModel(
            name='DeclinedRequest',
            fields=[
                ('note_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Номер записи')),
                ('organisation', models.CharField(max_length=50, verbose_name='Организация')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('problem_description', models.CharField(max_length=200, verbose_name='Описание проблемы')),
                ('comment', models.CharField(max_length=200, verbose_name='Комментарий')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.email', verbose_name='Email')),
                ('open_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.openrequest', verbose_name='Открытая заявка')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.urgencystatus', verbose_name='Статус срочности')),
            ],
            options={
                'verbose_name': 'Непринятая заявка',
                'verbose_name_plural': 'Непринятые заявки',
            },
        ),
        migrations.CreateModel(
            name='ClosedRequest',
            fields=[
                ('note_id', models.IntegerField(default=newgen.models.ClosedRequest.number, primary_key=True, serialize=False, verbose_name='Номер записи')),
                ('organisation', models.CharField(max_length=50, verbose_name='Организация')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('problem_description', models.CharField(max_length=200, verbose_name='Описание проблемы')),
                ('rating', models.IntegerField(verbose_name='Качество обслуживания')),
                ('comment', models.CharField(max_length=200, verbose_name='Комментарий')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.email', verbose_name='Email')),
                ('open_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.openrequest', verbose_name='Открытая заявка')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.urgencystatus', verbose_name='Статус срочности')),
            ],
            options={
                'verbose_name': 'Закрытая заявка',
                'verbose_name_plural': 'Закрытые заявки',
            },
        ),
    ]
