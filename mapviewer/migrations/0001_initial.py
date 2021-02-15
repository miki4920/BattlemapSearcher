# Generated by Django 3.1.5 on 2021-02-15 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('extension', models.CharField(max_length=3)),
                ('picture', models.ImageField(upload_to='maps')),
                ('uploader', models.CharField(max_length=50)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('square_width', models.IntegerField()),
                ('square_height', models.IntegerField()),
                ('tags', models.ManyToManyField(to='mapviewer.Tag')),
            ],
        ),
    ]
