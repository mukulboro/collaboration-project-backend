# Generated by Django 4.2.4 on 2023-11-04 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        ('endusers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usersinteams',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersinprojects',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project'),
        ),
        migrations.AddField(
            model_name='usersinprojects',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersinorganizations',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endusers.organization'),
        ),
        migrations.AddField(
            model_name='usersinorganizations',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='todo',
            name='assigned_to',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='todo',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.team'),
        ),
        migrations.AddField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project'),
        ),
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endusers.organization'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project'),
        ),
    ]
