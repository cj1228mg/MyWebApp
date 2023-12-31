# Generated by Django 4.0.3 on 2022-03-23 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, unique=True, verbose_name='カテゴリー')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
            ],
            options={
                'verbose_name': 'カテゴリー',
                'verbose_name_plural': 'カテゴリー',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english', models.CharField(max_length=100, unique=True, verbose_name='英語')),
                ('japanese', models.CharField(max_length=100, unique=True, verbose_name='日本語')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz.category', verbose_name='カテゴリー')),
            ],
            options={
                'verbose_name': '単語',
                'verbose_name_plural': '単語',
                'db_table': 'words',
            },
        ),
        migrations.CreateModel(
            name='IncorrectJP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('japanese', models.CharField(max_length=100, unique=True, verbose_name='日本語')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz.category', verbose_name='カテゴリー')),
            ],
            options={
                'verbose_name': '不正解日本語',
                'verbose_name_plural': '不正解日本語',
                'db_table': 'incorrect_jp',
            },
        ),
    ]
