# Generated by Django 4.1.6 on 2023-02-13 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divulgar', '0003_pet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='status',
            field=models.CharField(choices=[('P', 'Para adoção'), ('A', 'Adotado')], default='P', max_length=1),
        ),
    ]
