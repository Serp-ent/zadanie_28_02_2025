# Generated by Django 5.1.6 on 2025-02-28 14:36

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
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=100)),
                ('opis', models.TextField()),
                ('status', models.CharField(choices=[('NOWY', 'Nowy'), ('W TOKU', 'W toku'), ('ROZWIĄZANY', 'Rozwiązany')], max_length=10)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
