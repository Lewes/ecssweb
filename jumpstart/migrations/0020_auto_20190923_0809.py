# Generated by Django 2.2.1 on 2019-09-23 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jumpstart', '0019_auto_20190922_2210'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HintRecord',
            new_name='ScavengerHuntHintRecord',
        ),
        migrations.DeleteModel(
            name='CityChallengeScoreAuditlog',
        ),
    ]