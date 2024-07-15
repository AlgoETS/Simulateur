# Generated by Django 5.0.6 on 2024-07-15 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0002_stock_liquidity_stock_volatility_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulationsettings',
            name='interval_unit',
            field=models.CharField(choices=[('millisecond', 'Millisecond'), ('centisecond', 'Centisecond'), ('decisecond', 'Decisecond'), ('second', 'Second'), ('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('month', 'Month'), ('year', 'Year')], default='second', max_length=20),
        ),
        migrations.AlterField(
            model_name='simulationsettings',
            name='timer_step_unit',
            field=models.CharField(choices=[('millisecond', 'Millisecond'), ('centisecond', 'Centisecond'), ('decisecond', 'Decisecond'), ('second', 'Second'), ('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('month', 'Month'), ('year', 'Year')], default='second', max_length=20),
        ),
    ]