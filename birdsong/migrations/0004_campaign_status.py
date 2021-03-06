# Generated by Django 3.0.6 on 2020-06-11 20:41

from django.db import migrations, models


def set_status(apps, schema_editor):
    Campaign = apps.get_model('birdsong', 'campaign')
    for campaign in Campaign.objects.all():
        if campaign.sent_date:
            campaign.status = 2
            campaign.save()


class Migration(migrations.Migration):

    dependencies = [
        ('birdsong', '0003_drop_unique_constraint'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='status',
            field=models.IntegerField(choices=[(0, 'Unsent'), (1, 'Sending'), (2, 'Sent'), (3, 'Failed')], default=0),
            preserve_default=False,
        ),
        migrations.RunPython(set_status),
    ]
