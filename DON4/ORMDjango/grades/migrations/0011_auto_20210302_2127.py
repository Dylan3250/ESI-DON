# Generated by Django 3.1.7 on 2021-03-02 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0010_notestudent'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NoteStudent',
            new_name='Enrolment',
        ),
    ]
