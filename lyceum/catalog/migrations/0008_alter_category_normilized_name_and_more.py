# Generated by Django 4.2.5 on 2023-11-03 20:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0007_alter_category_normilized_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="normilized_name",
            field=models.CharField(
                editable=False,
                max_length=150,
                unique=True,
                verbose_name="Нормализоваванное имя",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="normilized_name",
            field=models.CharField(
                editable=False,
                max_length=150,
                unique=True,
                verbose_name="Нормализоваванное имя",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="normilized_name",
            field=models.CharField(
                editable=False,
                max_length=150,
                unique=True,
                verbose_name="Нормализоваванное имя",
            ),
        ),
    ]