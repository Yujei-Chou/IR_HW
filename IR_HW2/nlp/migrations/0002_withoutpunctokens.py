# Generated by Django 2.2 on 2021-10-25 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nlp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='withoutPuncTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=1000)),
                ('count', models.IntegerField()),
            ],
        ),
    ]
