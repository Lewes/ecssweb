# Generated by Django 2.0.5 on 2018-09-23 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0007_auto_20180923_0737'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityChallengeScoreAuditlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=150)),
                ('challenge', models.CharField(max_length=150)),
                ('score', models.IntegerField()),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jumpstart.Group')),
            ],
        ),
    ]
