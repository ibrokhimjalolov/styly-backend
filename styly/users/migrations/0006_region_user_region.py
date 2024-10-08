# Generated by Django 5.1.1 on 2024-09-15 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_user_birth_date_user_gender"),
    ]

    operations = [
        migrations.CreateModel(
            name="Region",
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
                ("name", models.CharField(max_length=512, verbose_name="name")),
            ],
            options={
                "verbose_name": "Region",
                "verbose_name_plural": "Regions",
                "ordering": ("name",),
            },
        ),
        migrations.AddField(
            model_name="user",
            name="region",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.region",
                verbose_name="region",
            ),
        ),
    ]
