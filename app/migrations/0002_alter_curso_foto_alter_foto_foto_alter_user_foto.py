# Generated by Django 5.1.3 on 2024-11-08 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='foto',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='foto',
            name='foto',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='foto',
            field=models.ImageField(upload_to='images/'),
        ),
    ]