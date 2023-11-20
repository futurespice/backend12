from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0005_alter_item_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="readymadeproduct",
            name="description",
        ),
        migrations.RemoveField(
            model_name="readymadeproduct",
            name="price",
        ),
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images"),
        ),
        # If you have other operations, keep them here
    ]