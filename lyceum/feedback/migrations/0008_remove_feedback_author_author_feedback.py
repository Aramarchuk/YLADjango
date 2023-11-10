# Generated by Django 4.2.5 on 2023-11-10 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "feedback",
            "0007_alter_feedback_author_alter_feedbackfile_feedback_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feedback",
            name="author",
        ),
        migrations.AddField(
            model_name="author",
            name="feedback",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author",
                to="feedback.feedback",
                verbose_name="фидбек",
            ),
        ),
    ]
