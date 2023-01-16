# Generated by Django 4.1.3 on 2022-12-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ApiSearchRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "claim",
                    models.CharField(
                        help_text="Verification claim", max_length=1000
                    ),
                ),
                (
                    "answer",
                    models.CharField(help_text="Answer", max_length=3000),
                ),
                ("datetime", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
