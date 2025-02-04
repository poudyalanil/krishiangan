# Generated by Django 3.1.2 on 2020-11-02 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_item_featured'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['upload_date']},
        ),
        migrations.AlterField(
            model_name='item',
            name='expiry_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='upload_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
