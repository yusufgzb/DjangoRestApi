# Generated by Django 3.2.12 on 2022-04-10 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haberler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gazeteci',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=120)),
                ('soyisim', models.CharField(max_length=120)),
                ('biyografi', models.TextField()),
            ],
        ),
    ]