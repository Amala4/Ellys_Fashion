# Generated by Django 4.1.5 on 2023-01-13 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productlist',
            name='category',
        ),
        migrations.AlterField(
            model_name='productlist',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('both', 'both')], default='female', max_length=50),
        ),
        migrations.AddField(
            model_name='productlist',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.category'),
        ),
    ]
