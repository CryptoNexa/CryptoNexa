# Generated by Django 4.2.6 on 2023-11-14 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_slug', models.SlugField()),
                ('currency_symbol', models.CharField(max_length=50)),
                ('data', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('num_market_pairs', models.IntegerField(null=True)),
                ('circulating_supply', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_supply', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('max_supply', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('infinite_supply', models.BooleanField(null=True)),
                ('last_updated', models.DateTimeField(null=True)),
                ('date_added', models.DateTimeField(null=True)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.quote')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]