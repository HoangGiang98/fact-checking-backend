# Generated by Django 4.1.5 on 2023-02-02 17:01

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
                        help_text="Verification claim", max_length=250
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
                (
                    "verdict",
                    models.CharField(
                        help_text="Is the claim supportive, refuted or not enough info",
                        max_length=20,
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
                        help_text="Title of an article", max_length=300
                    ),
                ),
                (
                    "url",
                    models.CharField(
                        default="",
                        help_text="Link of an article",
                        max_length=2000,
                    ),
                ),
                (
                    "content",
                    models.CharField(
                        help_text="Content of an article", max_length=300
                    ),
                ),
                (
                    "refuted_nli",
                    models.IntegerField(help_text="Refuted score", null=True),
                ),
                (
                    "not_enough_info_nli",
                    models.IntegerField(
                        help_text="Not enough info score", null=True
                    ),
                ),
                (
                    "supported_nli",
                    models.IntegerField(
                        help_text="Supported score", null=True
                    ),
                ),
                (
                    "similarity_dpr",
                    models.IntegerField(
                        help_text="Similarity score(only for dpr)", null=True
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
