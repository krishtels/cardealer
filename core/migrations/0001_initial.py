# Generated by Django 4.2 on 2023-04-06 21:58

import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        choices=[("Male", "M"), ("Female", "F")], max_length=6
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, null=True, region=None, unique=True
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "age",
                    models.IntegerField(
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(max_length=2, null=True),
                ),
                ("offer", models.JSONField(null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Car",
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
                    "engine_t",
                    models.CharField(
                        choices=[
                            ("Gasoline", "Gasoline"),
                            ("Diesel", "Diesel"),
                            ("Hybrid", "Hybrid"),
                            ("Electric", "Electric"),
                        ],
                        default="Gasoline",
                        max_length=20,
                    ),
                ),
                ("brand", models.CharField(max_length=20, null=True)),
                ("model", models.CharField(max_length=20, null=True)),
                ("color", models.CharField(max_length=20, null=True)),
                (
                    "engine_v",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
            ],
            options={
                "unique_together": {("brand", "model", "color", "engine_v")},
            },
        ),
        migrations.CreateModel(
            name="CarShowroom",
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
                ("is_active", models.BooleanField(default=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(auto_now_add=True)),
                ("name", models.CharField(max_length=100)),
                (
                    "country",
                    django_countries.fields.CountryField(max_length=2, null=True),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("specification", models.JSONField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Provider",
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
                ("is_active", models.BooleanField(default=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(auto_now_add=True)),
                ("name", models.CharField(max_length=100)),
                ("year_founded", models.DateField(null=True)),
                ("unique_customers_amount", models.IntegerField(default=0)),
                (
                    "country",
                    django_countries.fields.CountryField(max_length=2, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShowroomCars",
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
                ("is_active", models.BooleanField(default=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(auto_now_add=True)),
                ("amount", models.IntegerField(default=0)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.car"
                    ),
                ),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.carshowroom",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProviderSalesHistory",
            fields=[
                ("is_active", models.BooleanField(default=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.IntegerField(default=0)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.car"
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.provider"
                    ),
                ),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.carshowroom",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProviderDiscount",
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
                ("is_active", models.BooleanField(default=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(auto_now_add=True)),
                ("date_start", models.DateField(auto_now_add=True)),
                ("date_end", models.DateField(auto_now_add=True)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(null=True)),
                ("amount_to_get_sale", models.IntegerField(default=0)),
                (
                    "percent",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=4,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("cars", models.ManyToManyField(to="core.car")),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.provider"
                    ),
                ),
                ("shops", models.ManyToManyField(to="core.carshowroom")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProviderCars",
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
                ("is_active", models.BooleanField(default=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.car"
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.provider"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="provider",
            name="cars",
            field=models.ManyToManyField(through="core.ProviderCars", to="core.car"),
        ),
        migrations.CreateModel(
            name="CarShowroomSalesHistory",
            fields=[
                ("is_active", models.BooleanField(default=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("amount", models.IntegerField(default=0)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.car"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.carshowroom",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CarShowroomDiscount",
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
                ("is_active", models.BooleanField(default=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(auto_now_add=True)),
                ("date_start", models.DateField(auto_now_add=True)),
                ("date_end", models.DateField(auto_now_add=True)),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(null=True)),
                ("amount_to_get_sale", models.IntegerField(default=0)),
                (
                    "percent",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=4,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                ("cars", models.ManyToManyField(to="core.car")),
                (
                    "shop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.carshowroom",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="carshowroom",
            name="cars",
            field=models.ManyToManyField(through="core.ShowroomCars", to="core.car"),
        ),
    ]