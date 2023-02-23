# Generated by Django 4.1.4 on 2023-01-30 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newgen', '0005_closedrequest_worker_id_declinedrequest_worker_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('note_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Номер записи')),
                ('activation_code', models.CharField(max_length=20, verbose_name='Код активации')),
                ('expiry_date', models.DateField(verbose_name='Окончательный срок действия кода')),
                ('open_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newgen.openrequest', verbose_name='Открытая заявка')),
            ],
            options={
                'verbose_name': 'Подтверждение Email',
                'verbose_name_plural': 'Подтверждения Email',
            },
        ),
    ]