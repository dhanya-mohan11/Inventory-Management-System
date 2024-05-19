# Generated by Django 5.0.3 on 2024-03-19 07:13

import django.db.models.deletion
import inventory.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('billno', models.CharField(default=inventory.models.key_generator, editable=False, max_length=6, unique=True)),
                ('quantity', models.FloatField()),
                ('price', models.FloatField()),
                ('total_amount', models.FloatField(default=0, editable=False)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Purchases',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('billno', models.CharField(default=inventory.models.key_generator, editable=False, max_length=6, unique=True)),
                ('quantity', models.FloatField()),
                ('price', models.FloatField()),
                ('total_amount', models.FloatField(default=0, editable=False)),
                ('sale_date', models.DateTimeField(auto_now_add=True)),
                ('customer_name', models.CharField(max_length=150)),
                ('customer_phone', models.CharField(max_length=12, unique=True)),
                ('customer_address', models.TextField(blank=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='SaleBill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('eway', models.CharField(blank=True, max_length=50, null=True)),
                ('veh', models.CharField(blank=True, max_length=50, null=True)),
                ('destination', models.CharField(blank=True, max_length=50, null=True)),
                ('po', models.CharField(blank=True, max_length=50, null=True)),
                ('cgst', models.CharField(blank=True, max_length=50, null=True)),
                ('sgst', models.CharField(blank=True, max_length=50, null=True)),
                ('igst', models.CharField(blank=True, max_length=50, null=True)),
                ('cess', models.CharField(blank=True, max_length=50, null=True)),
                ('tcs', models.CharField(blank=True, max_length=50, null=True)),
                ('total', models.IntegerField(default=0)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salebillno', to='inventory.sale')),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customername', to='inventory.sale')),
                ('customer_phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customerphone', to='inventory.sale')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('sale_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.sale')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=30, unique=True, verbose_name='Name')),
                ('short_name', models.CharField(default='', max_length=10, unique=True, verbose_name='ShortName')),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Units',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.unit'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=40, null=True)),
                ('mobile', models.CharField(max_length=12, null=True)),
                ('picture', models.ImageField(default='avatar.jpeg', upload_to='Pictures')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=12, unique=True)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Vendors',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('purchase_quantity', models.FloatField(default=0, null=True)),
                ('sale_quantity', models.FloatField(default=0, null=True)),
                ('total_balance_quantity', models.FloatField(default=0)),
                ('customer_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='inventory.sale')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('purchase', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.purchase')),
                ('sale', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.sale')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.vendor')),
            ],
            options={
                'verbose_name_plural': 'Inventory',
            },
        ),
        migrations.CreateModel(
            name='PurchaseBill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('eway', models.CharField(blank=True, max_length=50, null=True)),
                ('veh', models.CharField(blank=True, max_length=50, null=True)),
                ('destination', models.CharField(blank=True, max_length=50, null=True)),
                ('po', models.CharField(blank=True, max_length=50, null=True)),
                ('cgst', models.CharField(blank=True, max_length=50, null=True)),
                ('sgst', models.CharField(blank=True, max_length=50, null=True)),
                ('igst', models.CharField(blank=True, max_length=50, null=True)),
                ('cess', models.CharField(blank=True, max_length=50, null=True)),
                ('tcs', models.CharField(blank=True, max_length=50, null=True)),
                ('total', models.IntegerField(default=0)),
                ('billno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchasebillno', to='inventory.purchase')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('purchase_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.purchase')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.vendor')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.vendor'),
        ),
    ]
