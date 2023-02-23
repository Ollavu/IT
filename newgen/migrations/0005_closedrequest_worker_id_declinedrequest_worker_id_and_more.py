# Generated by Django 4.1.4 on 2023-01-30 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newgen', '0004_requeststatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedrequest',
            name='worker_id',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='newgen.worker', verbose_name='Ответственный'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='declinedrequest',
            name='worker_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='newgen.worker', verbose_name='Ответственный'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='openrequest',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='newgen.requeststatus', verbose_name='Статус заявки'),
            preserve_default=False,
        ),
    ]