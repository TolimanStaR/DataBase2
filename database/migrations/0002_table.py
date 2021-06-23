# Generated by Django 3.2 on 2021-06-20 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('db', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='database.database')),
            ],
        ),
    ]
