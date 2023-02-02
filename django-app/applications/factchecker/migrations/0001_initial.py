# Generated by Django 4.1.5 on 2023-01-23 08:11

import applications.factchecker.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SearchRequest",
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
                        help_text="Verification claim", max_length=30
                    ),
                ),
                (
                    "verification_method",
                    models.CharField(
                        default="dpr",
                        help_text="Verification method",
                        max_length=30,
                    ),
                ),
                ("datetime", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SearchResponse",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "claim",
                    models.CharField(
                        help_text="Verification claim", max_length=10000
                    ),
                ),
                (
                    "results",
                    models.JSONField(
                        default=[dict],
                        help_text="List of results",
                        validators=[
                            applications.factchecker.models.result_json_validator
                        ],
                    ),
                ),
                (
                    "verdict",
                    models.CharField(
                        help_text="Is the claim supportive, refuted or not enough info",
                        max_length=20,
                    ),
                ),
                (
                    "request",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="factchecker.searchrequest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of an article", max_length=30
                    ),
                ),
                (
                    "content",
                    models.CharField(
                        help_text="Content of an article", max_length=300
                    ),
                ),
                (
                    "verdict",
                    models.CharField(
                        help_text="How true the claim is", max_length=10
                    ),
                ),
                (
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="factchecker.searchrequest",
                    ),
                ),
            ],
        ),
    ]
