# Generated by Django 5.0.6 on 2024-07-01 06:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0008_alter_skill_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="drinking_habit",
            field=models.CharField(
                choices=[
                    ("Non-drinker", "Non-drinker"),
                    ("Occasional drinker", "Occasional drinker"),
                    ("Social drinker", "Social drinker"),
                    ("Regular drinker", "Regular drinker"),
                    ("Heavy drinker", "Heavy drinker"),
                    ("Trying to quit", "Trying to quit"),
                ],
                default="Non-drinker",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="qualification",
            field=models.CharField(
                blank=True,
                choices=[
                    ("High School", "High School"),
                    ("Associate's Degree", "Associate's Degree"),
                    ("Bachelor's Degree", "Bachelor's Degree"),
                    ("Master's Degree", "Master's Degree"),
                    ("Doctorate", "Doctorate"),
                    ("Professional Degree", "Professional Degree"),
                    ("Certificate", "Certificate"),
                    ("Diploma", "Diploma"),
                    ("Postdoctoral", "Postdoctoral"),
                    ("Vocational", "Vocational"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="smoking_habit",
            field=models.CharField(
                choices=[
                    ("Non-smoker", "Non-smoker"),
                    ("Occasional smoker", "Occasional smoker"),
                    ("Regular smoker", "Regular smoker"),
                    ("Heavy smoker", "Heavy smoker"),
                    ("Trying to quit", "Trying to quit"),
                ],
                default="Non-smoker",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="education",
            name="degree",
            field=models.CharField(
                choices=[
                    ("High School", "High School"),
                    ("Associate's Degree", "Associate's Degree"),
                    ("Bachelor's Degree", "Bachelor's Degree"),
                    ("Master's Degree", "Master's Degree"),
                    ("Doctorate", "Doctorate"),
                    ("Professional Degree", "Professional Degree"),
                    ("Certificate", "Certificate"),
                    ("Diploma", "Diploma"),
                    ("Postdoctoral", "Postdoctoral"),
                    ("Vocational", "Vocational"),
                ],
                max_length=25,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="userskill",
            unique_together={("user", "skill")},
        ),
    ]
