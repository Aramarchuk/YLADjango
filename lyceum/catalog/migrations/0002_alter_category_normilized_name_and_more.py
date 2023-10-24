# Generated by Django 4.2.5 on 2023-10-21 08:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="normilized_name",
            field=models.CharField(
                auto_created=True,
                max_length=150,
                unique=True,
                verbose_name="Нормализоваванное имя",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="normilized_name",
            field=models.CharField(
                auto_created=True,
                max_length=150,
                unique=True,
                verbose_name="Нормализоваванное имя",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="normilized_name",
            field=models.CharField(
                auto_created=True,
                max_length=150,
                unique=True,
                verbose_name="Нормализоваванное имя",
            ),
        ),
    ]