# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Type'
        db.create_table('mobile_apps_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('mobile_apps', ['Type'])

        # Adding model 'App'
        db.create_table('mobile_apps_app', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mobile_apps.Type'])),
            ('cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('mobile_apps', ['App'])

        # Adding M2M table for field levels on 'App'
        db.create_table('mobile_apps_app_levels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('app', models.ForeignKey(orm['mobile_apps.app'], null=False)),
            ('level', models.ForeignKey(orm['core.level'], null=False))
        ))
        db.create_unique('mobile_apps_app_levels', ['app_id', 'level_id'])

        # Adding M2M table for field content_areas on 'App'
        db.create_table('mobile_apps_app_content_areas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('app', models.ForeignKey(orm['mobile_apps.app'], null=False)),
            ('level', models.ForeignKey(orm['core.level'], null=False))
        ))
        db.create_unique('mobile_apps_app_content_areas', ['app_id', 'level_id'])


    def backwards(self, orm):
        
        # Deleting model 'Type'
        db.delete_table('mobile_apps_type')

        # Deleting model 'App'
        db.delete_table('mobile_apps_app')

        # Removing M2M table for field levels on 'App'
        db.delete_table('mobile_apps_app_levels')

        # Removing M2M table for field content_areas on 'App'
        db.delete_table('mobile_apps_app_content_areas')


    models = {
        'core.level': {
            'Meta': {'ordering': "['order']", 'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'mobile_apps.app': {
            'Meta': {'object_name': 'App'},
            'content_areas': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'content_areas'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Level']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'levels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'levels'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Level']"}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mobile_apps.Type']"})
        },
        'mobile_apps.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mobile_apps']
