# Generated by Django 4.2.5 on 2023-10-06 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('payout', models.DecimalField(decimal_places=2, max_digits=7)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
