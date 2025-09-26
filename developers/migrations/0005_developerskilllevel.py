# Generated manually for DeveloperSkillLevel model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('developers', '0004_developerprojects'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeveloperSkillLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(0, 'Basic Knowledge'), (1, 'Beginner'), (2, 'Advanced'), (3, 'Expert')], default=0)),
                ('project_count', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_levels', to='developers.developers')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='developer_levels', to='developers.skills')),
            ],
            options={
                'unique_together': {('developer', 'skill')},
            },
        ),
    ]
