from django.db import migrations


def create_authors_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Authors')


def remove_authors_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Authors').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_authors_group, remove_authors_group),
    ]