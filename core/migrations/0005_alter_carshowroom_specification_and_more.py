# Generated by Django 4.2 on 2023-04-11 13:19

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_rename_offer_customer_specification_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carshowroom",
            name="specification",
            field=models.JSONField(
                encoder=django.core.serializers.json.DjangoJSONEncoder
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="specification",
            field=models.JSONField(
                encoder=django.core.serializers.json.DjangoJSONEncoder, null=True
            ),
        ),
    ]
