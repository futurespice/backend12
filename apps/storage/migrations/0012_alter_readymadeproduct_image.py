# Generated by Django 4.2.7 on 2023-11-21 18:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0011_alter_ingredient_name_alter_readymadeproduct_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="readymadeproduct",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images"),
        ),
    ]
