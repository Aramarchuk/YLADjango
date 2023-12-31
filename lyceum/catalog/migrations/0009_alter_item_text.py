# Generated by Django 4.2.5 on 2023-11-06 15:22

import catalog.validators
import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0008_alter_category_normilized_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=ckeditor.fields.RichTextField(
                help_text="Должно содержать по крайней мере одно слово 'Превосходно' или 'Роскошно'",
                validators=[
                    catalog.validators.ValidateMustContain(
                        "превосходно", "роскошно"
                    )
                ],
                verbose_name="текст",
            ),
        ),
    ]
