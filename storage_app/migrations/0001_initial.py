# Generated by Django 4.1.7 on 2023-03-30 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(auto_created=True, primary_key=True, serialize=False)),
                ('filepath', models.FilePathField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=18, unique=True)),
                ('description', models.CharField(max_length=512)),
                ('portrait', models.ImageField(default='default.jpg', upload_to='profile_images')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_access', models.CharField(choices=[['PUBLIC', 'public'], ['FRIENDLY', 'friendly'], ['LINKABLE', 'linkable'], ['PRIVATE', 'private']], default='private', max_length=9)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='FilePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_app.file')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_app.page')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(auto_created=True, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_app.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_app.user')),
            ],
        ),
    ]
