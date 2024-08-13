# Generated by Django 4.2.13 on 2024-08-13 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('content', models.TextField(default='')),
                ('published_date', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_items', to='simulation.event')),
            ],
            options={
                'verbose_name_plural': 'Market News',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0.0)),
                ('transaction_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], default='BUY', max_length=100)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Orders',
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
                ('published_date', models.DateTimeField(auto_now=True)),
                ('events', models.ManyToManyField(related_name='scenarios_events', to='simulation.event')),
                ('news', models.ManyToManyField(related_name='scenarios_news', to='simulation.news')),
            ],
            options={
                'verbose_name_plural': 'Scenarios',
            },
        ),
        migrations.CreateModel(
            name='SimulationSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_users', models.IntegerField(default=100)),
                ('max_companies', models.IntegerField(default=50)),
                ('timer_step', models.IntegerField(default=10)),
                ('timer_step_unit', models.CharField(choices=[('millisecond', 'Millisecond'), ('centisecond', 'Centisecond'), ('decisecond', 'Decisecond'), ('second', 'Second'), ('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('month', 'Month'), ('year', 'Year')], default='second', max_length=20)),
                ('interval', models.IntegerField(default=20)),
                ('interval_unit', models.CharField(choices=[('millisecond', 'Millisecond'), ('centisecond', 'Centisecond'), ('decisecond', 'Decisecond'), ('second', 'Second'), ('minute', 'Minute'), ('hour', 'Hour'), ('day', 'Day'), ('month', 'Month'), ('year', 'Year')], default='second', max_length=20)),
                ('max_interval', models.IntegerField(default=3000)),
                ('fluctuation_rate', models.FloatField(default=0.1)),
                ('close_stock_market_at_night', models.BooleanField(default=True)),
                ('noise_function', models.CharField(choices=[('brownian', 'Brownian Motion'), ('monte_carlo', 'Monte Carlo'), ('perlin', 'Perlin Noise'), ('random_walk', 'Random Walk'), ('fbm', 'Fractional Brownian Motion'), ('other', 'Other')], default='brownian', max_length=20)),
                ('stock_trading_logic', models.CharField(choices=[('dynamic', 'Dynamic'), ('static', 'Static')], default='static', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Simulation Settings',
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
                ('volatility', models.FloatField(default=0.0)),
                ('liquidity', models.FloatField(default=0.0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='simulation.company')),
            ],
            options={
                'verbose_name_plural': 'Stocks',
                'ordering': ['timestamp'],
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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('role', models.CharField(choices=[('member', 'Member'), ('team_leader', 'Team Leader'), ('admin', 'Admin'), ('super_admin', 'Super Admin'), ('moderator', 'Moderator')], default='member', max_length=20)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profiles', to='simulation.team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Profiles',
            },
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
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.ManyToManyField(related_name='transactions', to='simulation.order')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.scenario')),
            ],
            options={
                'verbose_name_plural': 'Transaction Histories',
            },
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='teams', to='simulation.userprofile'),
        ),
        migrations.CreateModel(
            name='StockPriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_price', models.FloatField(default=0.0)),
                ('high_price', models.FloatField(default=0.0)),
                ('low_price', models.FloatField(default=0.0)),
                ('close_price', models.FloatField(default=0.0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('volatility', models.FloatField(default=0.0)),
                ('liquidity', models.FloatField(default=0.0)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='simulation.stock')),
            ],
            options={
                'verbose_name_plural': 'Stock Price Histories',
                'ordering': ['timestamp'],
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
        migrations.AddField(
            model_name='scenario',
            name='simulation_settings',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='simulation.simulationsettings'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='stocks',
            field=models.ManyToManyField(related_name='scenarios_stocks', to='simulation.stock'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='teams',
            field=models.ManyToManyField(related_name='scenarios_teams', to='simulation.team'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='triggers',
            field=models.ManyToManyField(related_name='scenarios_triggers', to='simulation.trigger'),
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to='simulation.userprofile')),
                ('scenario', models.ManyToManyField(blank=True, to='simulation.scenario')),
            ],
            options={
                'verbose_name_plural': 'Portfolios',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.stock'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.userprofile'),
        ),
        migrations.AddField(
            model_name='news',
            name='scenario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_items', to='simulation.scenario'),
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
            name='StockPortfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_holding_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.IntegerField(default=0)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_portfolios', to='simulation.portfolio')),
                ('stock', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='simulation.stock')),
            ],
            options={
                'unique_together': {('stock', 'portfolio')},
            },
        ),
    ]
