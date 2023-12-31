# Generated by Django 4.2.5 on 2023-11-09 13:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0004_alter_statuslog_from_status_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="statuslog",
            name="to_status",
        ),
        migrations.AddField(
            model_name="statuslog",
            name="to",
            field=models.TextField(
                choices=[
                    ("IN", "в обработке"),
                    ("GET", "получено"),
                    ("ANS", "ответ дан"),
                ],
                db_column="to",
                default="GET",
                max_length=4,
                verbose_name="новый статус обработки",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="statuslog",
            name="from_status",
            field=models.CharField(
                choices=[
                    ("IN", "в обработке"),
                    ("GET", "получено"),
                    ("ANS", "ответ дан"),
                ],
                db_column="from",
                max_length=4,
                verbose_name="старый статус обработки",
            ),
        ),
    ]
