# Generated by Django 3.0.4 on 2021-04-01 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=127, unique=True)),
                ('title', models.CharField(max_length=127)),
                ('current_info', models.CharField(max_length=255)),
                ('avatar', models.ImageField(default='/users/user.jpg', upload_to='community')),
                ('closed', models.BooleanField(blank=True, default=False)),
            ],
        ),
    ]
