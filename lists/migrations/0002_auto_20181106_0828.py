# Generated by Django 2.1.2 on 2018-11-06 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("lists", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="list",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        )
    ]
