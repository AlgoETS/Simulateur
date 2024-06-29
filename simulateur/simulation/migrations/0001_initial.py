# Generated by Django 5.0.6 on 2024-06-29 04:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('backstory', models.TextField(default='')),
                ('sector', models.CharField(default='', max_length=100)),
                ('country', models.CharField(default='', max_length=100)),
                ('industry', models.CharField(default='', max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='')),
                ('type', models.CharField(default='', max_length=100)),
                ('date', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(default=0.0)),
            ],
            options={
                'verbose_name_plural': 'Portfolios',
            },
        ),
        migrations.CreateModel(
            name='SimulationSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_users', models.IntegerField(default=100)),
                ('max_companies', models.IntegerField(default=50)),
                ('timer_step', models.IntegerField(default=10)),
                ('timer_step_unit', models.CharField(choices=[('second', 'Second'), ('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('month', 'Month'), ('year', 'Year')], default='minute', max_length=6)),
                ('interval', models.IntegerField(default=20)),
                ('interval_unit', models.CharField(choices=[('second', 'Second'), ('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('month', 'Month'), ('year', 'Year')], default='minute', max_length=6)),
                ('max_interval', models.IntegerField(default=3000)),
                ('fluctuation_rate', models.FloatField(default=0.1)),
                ('close_stock_market_at_night', models.BooleanField(default=True)),
                ('noise_function', models.CharField(choices=[('brownian', 'Brownian Motion'), ('monte_carlo', 'Monte Carlo'), ('perlin', 'Perlin Noise'), ('random_walk', 'Random Walk'), ('fbm', 'Fractional Brownian Motion'), ('other', 'Other')], default='brownian', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Simulation Settings',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Teams',
            },
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='')),
                ('backstory', models.TextField(default='')),
                ('duration', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('companies', models.ManyToManyField(related_name='scenarios', to='simulation.company')),
                ('events', models.ManyToManyField(related_name='scenarios', to='simulation.event')),
                ('simulation_settings', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='simulation.simulationsettings')),
            ],
            options={
                'verbose_name_plural': 'Scenarios',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('content', models.TextField(default='')),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_items', to='simulation.event')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_items', to='simulation.scenario')),
            ],
            options={
                'verbose_name_plural': 'Market News',
            },
        ),
        migrations.CreateModel(
            name='SimulationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('price_changes', models.JSONField(default=list)),
                ('transactions', models.JSONField(default=list)),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.scenario')),
            ],
            options={
                'verbose_name_plural': 'Simulation Data',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(default='', max_length=10)),
                ('price', models.FloatField(default=0.0)),
                ('open_price', models.FloatField(default=0.0)),
                ('high_price', models.FloatField(default=0.0)),
                ('low_price', models.FloatField(default=0.0)),
                ('close_price', models.FloatField(default=0.0)),
                ('partial_share', models.FloatField(default=0.0)),
                ('complete_share', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.company')),
            ],
            options={
                'verbose_name_plural': 'Stocks',
                'ordering': ['timestamp'],
            },
        ),
        migrations.AddField(
            model_name='scenario',
            name='stocks',
            field=models.ManyToManyField(related_name='scenarios', to='simulation.stock'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0.0)),
                ('transaction_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], default='BUY', max_length=100)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.scenario')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.stock')),
            ],
            options={
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='StockPortfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.portfolio')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.stock')),
            ],
            options={
                'unique_together': {('stock', 'portfolio')},
            },
        ),
        migrations.AddField(
            model_name='portfolio',
            name='stocks',
            field=models.ManyToManyField(through='simulation.StockPortfolio', to='simulation.stock'),
        ),
        migrations.CreateModel(
            name='StockPriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='simulation.stock')),
            ],
            options={
                'verbose_name_plural': 'Stock Price Histories',
                'ordering': ['timestamp'],
            },
        ),
        migrations.AddField(
            model_name='stock',
            name='stock_price_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocks_history', to='simulation.stockpricehistory'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='teams',
            field=models.ManyToManyField(related_name='scenarios', to='simulation.team'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='team',
            field=models.ManyToManyField(blank=True, related_name='portfolios', to='simulation.team'),
        ),
        migrations.CreateModel(
            name='JoinLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=32, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_links', to='simulation.team')),
            ],
            options={
                'verbose_name_plural': 'Join Links',
            },
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.ManyToManyField(related_name='transactions', to='simulation.order')),
            ],
            options={
                'verbose_name_plural': 'Transaction Histories',
            },
        ),
        migrations.AddField(
            model_name='portfolio',
            name='transactions',
            field=models.ManyToManyField(blank=True, related_name='portfolios', to='simulation.transactionhistory'),
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(default='')),
                ('type', models.CharField(default='', max_length=100)),
                ('value', models.FloatField(default=0.0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('events', models.ManyToManyField(blank=True, to='simulation.event')),
            ],
            options={
                'verbose_name_plural': 'Triggers',
            },
        ),
        migrations.AddField(
            model_name='scenario',
            name='triggers',
            field=models.ManyToManyField(related_name='scenarios', to='simulation.trigger'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profiles', to='simulation.team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='teams', to='simulation.userprofile'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='users',
            field=models.ManyToManyField(related_name='scenarios', to='simulation.userprofile'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to='simulation.userprofile'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.userprofile'),
        ),
    ]
