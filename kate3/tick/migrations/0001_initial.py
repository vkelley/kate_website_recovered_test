# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CoreContent'
        db.create_table('tick_corecontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('bigidea', self.gf('django.db.models.fields.IntegerField')()),
            ('subcategory', self.gf('django.db.models.fields.IntegerField')()),
            ('catpoint', self.gf('django.db.models.fields.IntegerField')()),
            ('dok', self.gf('django.db.models.fields.IntegerField')()),
            ('tested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('content_area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ContentArea'])),
        ))
        db.send_create_signal('tick', ['CoreContent'])

        # Adding model 'TechIndicator'
        db.create_table('tick_techindicator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('standard', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('tick', ['TechIndicator'])

        # Adding M2M table for field tech_standards on 'TechIndicator'
        db.create_table('tick_techindicator_tech_standards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('techindicator', models.ForeignKey(orm['tick.techindicator'], null=False)),
            ('technologystandard', models.ForeignKey(orm['tick.technologystandard'], null=False))
        ))
        db.create_unique('tick_techindicator_tech_standards', ['techindicator_id', 'technologystandard_id'])

        # Adding model 'TechnologyComponent'
        db.create_table('tick_technologycomponent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('tick', ['TechnologyComponent'])

        # Adding model 'TechnologySubComponent'
        db.create_table('tick_technologysubcomponent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tech_component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tick.TechnologyComponent'])),
        ))
        db.send_create_signal('tick', ['TechnologySubComponent'])

        # Adding model 'Focus'
        db.create_table('tick_focus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('tick', ['Focus'])

        # Adding model 'SubFocus'
        db.create_table('tick_subfocus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('focus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tick.Focus'])),
        ))
        db.send_create_signal('tick', ['SubFocus'])

        # Adding model 'TechnologyStandard'
        db.create_table('tick_technologystandard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('point', self.gf('django.db.models.fields.IntegerField')()),
            ('subpoint', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('tick', ['TechnologyStandard'])

        # Adding model 'ProgramOfStudy'
        db.create_table('tick_programofstudy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('bigidea', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('point', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('tick', ['ProgramOfStudy'])

        # Adding M2M table for field tech_standards on 'ProgramOfStudy'
        db.create_table('tick_programofstudy_tech_standards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('programofstudy', models.ForeignKey(orm['tick.programofstudy'], null=False)),
            ('technologystandard', models.ForeignKey(orm['tick.technologystandard'], null=False))
        ))
        db.create_unique('tick_programofstudy_tech_standards', ['programofstudy_id', 'technologystandard_id'])

        # Adding model 'CommonCoreStandard'
        db.create_table('tick_commoncorestandard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('grade', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('strand', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('standard', self.gf('django.db.models.fields.IntegerField')()),
            ('sub_standard', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('stem', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('tick', ['CommonCoreStandard'])

        # Adding model 'Resource'
        db.create_table('tick_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('focus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tick.Focus'], null=True, blank=True)),
            ('sub_focus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tick.SubFocus'], null=True, blank=True)),
            ('tech_component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tick.TechnologyComponent'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 2, 14))),
            ('resource_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('source', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('filename', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('feebased', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('entered_by', self.gf('django.db.models.fields.CharField')(default='none', max_length=255)),
            ('loti_level', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('disabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('aligned_to_common_core', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('aligned_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='aligned_by', null=True, to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='none', max_length=55, null=True, blank=True)),
        ))
        db.send_create_signal('tick', ['Resource'])

        # Adding M2M table for field levels on 'Resource'
        db.create_table('tick_resource_levels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['tick.resource'], null=False)),
            ('level', models.ForeignKey(orm['core.level'], null=False))
        ))
        db.create_unique('tick_resource_levels', ['resource_id', 'level_id'])

        # Adding M2M table for field content_areas on 'Resource'
        db.create_table('tick_resource_content_areas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['tick.resource'], null=False)),
            ('contentarea', models.ForeignKey(orm['core.contentarea'], null=False))
        ))
        db.create_unique('tick_resource_content_areas', ['resource_id', 'contentarea_id'])

        # Adding M2M table for field tech_standards on 'Resource'
        db.create_table('tick_resource_tech_standards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['tick.resource'], null=False)),
            ('technologystandard', models.ForeignKey(orm['tick.technologystandard'], null=False))
        ))
        db.create_unique('tick_resource_tech_standards', ['resource_id', 'technologystandard_id'])

        # Adding M2M table for field content_standards on 'Resource'
        db.create_table('tick_resource_content_standards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['tick.resource'], null=False)),
            ('corecontent', models.ForeignKey(orm['tick.corecontent'], null=False))
        ))
        db.create_unique('tick_resource_content_standards', ['resource_id', 'corecontent_id'])

        # Adding M2M table for field programs_of_studies on 'Resource'
        db.create_table('tick_resource_programs_of_studies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['tick.resource'], null=False)),
            ('programofstudy', models.ForeignKey(orm['tick.programofstudy'], null=False))
        ))
        db.create_unique('tick_resource_programs_of_studies', ['resource_id', 'programofstudy_id'])

        # Adding M2M table for field common_core_standards on 'Resource'
        db.create_table('tick_resource_common_core_standards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['tick.resource'], null=False)),
            ('commoncorestandard', models.ForeignKey(orm['tick.commoncorestandard'], null=False))
        ))
        db.create_unique('tick_resource_common_core_standards', ['resource_id', 'commoncorestandard_id'])

        # Adding M2M table for field tech_indicators on 'Resource'
        db.create_table('tick_resource_tech_indicators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['tick.resource'], null=False)),
            ('techindicator', models.ForeignKey(orm['tick.techindicator'], null=False))
        ))
        db.create_unique('tick_resource_tech_indicators', ['resource_id', 'techindicator_id'])

        # Adding M2M table for field tech_sub_component on 'Resource'
        db.create_table('tick_resource_tech_sub_component', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['tick.resource'], null=False)),
            ('technologysubcomponent', models.ForeignKey(orm['tick.technologysubcomponent'], null=False))
        ))
        db.create_unique('tick_resource_tech_sub_component', ['resource_id', 'technologysubcomponent_id'])

        # Adding model 'Favorite'
        db.create_table('tick_favorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tick.Resource'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('tick', ['Favorite'])

        # Adding model 'Announcement'
        db.create_table('tick_announcement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body_filter', self.gf('django.db.models.fields.CharField')(default='Markdown', max_length=100)),
            ('picture', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('tick', ['Announcement'])

        # Adding model 'Notice'
        db.create_table('tick_notice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body_filter', self.gf('django.db.models.fields.CharField')(default='Markdown', max_length=100)),
        ))
        db.send_create_signal('tick', ['Notice'])

        # Adding M2M table for field winner on 'Notice'
        db.create_table('tick_notice_winner', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notice', models.ForeignKey(orm['tick.notice'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('tick_notice_winner', ['notice_id', 'user_id'])


    def backwards(self, orm):
        
        # Deleting model 'CoreContent'
        db.delete_table('tick_corecontent')

        # Deleting model 'TechIndicator'
        db.delete_table('tick_techindicator')

        # Removing M2M table for field tech_standards on 'TechIndicator'
        db.delete_table('tick_techindicator_tech_standards')

        # Deleting model 'TechnologyComponent'
        db.delete_table('tick_technologycomponent')

        # Deleting model 'TechnologySubComponent'
        db.delete_table('tick_technologysubcomponent')

        # Deleting model 'Focus'
        db.delete_table('tick_focus')

        # Deleting model 'SubFocus'
        db.delete_table('tick_subfocus')

        # Deleting model 'TechnologyStandard'
        db.delete_table('tick_technologystandard')

        # Deleting model 'ProgramOfStudy'
        db.delete_table('tick_programofstudy')

        # Removing M2M table for field tech_standards on 'ProgramOfStudy'
        db.delete_table('tick_programofstudy_tech_standards')

        # Deleting model 'CommonCoreStandard'
        db.delete_table('tick_commoncorestandard')

        # Deleting model 'Resource'
        db.delete_table('tick_resource')

        # Removing M2M table for field levels on 'Resource'
        db.delete_table('tick_resource_levels')

        # Removing M2M table for field content_areas on 'Resource'
        db.delete_table('tick_resource_content_areas')

        # Removing M2M table for field tech_standards on 'Resource'
        db.delete_table('tick_resource_tech_standards')

        # Removing M2M table for field content_standards on 'Resource'
        db.delete_table('tick_resource_content_standards')

        # Removing M2M table for field programs_of_studies on 'Resource'
        db.delete_table('tick_resource_programs_of_studies')

        # Removing M2M table for field common_core_standards on 'Resource'
        db.delete_table('tick_resource_common_core_standards')

        # Removing M2M table for field tech_indicators on 'Resource'
        db.delete_table('tick_resource_tech_indicators')

        # Removing M2M table for field tech_sub_component on 'Resource'
        db.delete_table('tick_resource_tech_sub_component')

        # Deleting model 'Favorite'
        db.delete_table('tick_favorite')

        # Deleting model 'Announcement'
        db.delete_table('tick_announcement')

        # Deleting model 'Notice'
        db.delete_table('tick_notice')

        # Removing M2M table for field winner on 'Notice'
        db.delete_table('tick_notice_winner')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.contentarea': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContentArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.level': {
            'Meta': {'ordering': "['order']", 'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'tick.announcement': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Announcement'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_filter': ('django.db.models.fields.CharField', [], {'default': "'Markdown'", 'max_length': '100'}),
            'body_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'tick.commoncorestandard': {
            'Meta': {'ordering': "('id',)", 'object_name': 'CommonCoreStandard'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'standard': ('django.db.models.fields.IntegerField', [], {}),
            'stem': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'strand': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'sub_standard': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'tick.corecontent': {
            'Meta': {'ordering': "['code']", 'object_name': 'CoreContent'},
            'bigidea': ('django.db.models.fields.IntegerField', [], {}),
            'catpoint': ('django.db.models.fields.IntegerField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'content_area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ContentArea']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'dok': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'subcategory': ('django.db.models.fields.IntegerField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'tested': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'tick.favorite': {
            'Meta': {'object_name': 'Favorite'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tick.Resource']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'tick.focus': {
            'Meta': {'ordering': "['name']", 'object_name': 'Focus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tick.notice': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Notice'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_filter': ('django.db.models.fields.CharField', [], {'default': "'Markdown'", 'max_length': '100'}),
            'body_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'winner': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'tick.programofstudy': {
            'Meta': {'ordering': "['code']", 'object_name': 'ProgramOfStudy'},
            'bigidea': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'point': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'tech_standards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tick.TechnologyStandard']", 'null': 'True', 'blank': 'True'})
        },
        'tick.resource': {
            'Meta': {'ordering': "['title']", 'object_name': 'Resource'},
            'aligned_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'aligned_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'aligned_to_common_core': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'common_core_standards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tick.CommonCoreStandard']", 'null': 'True', 'blank': 'True'}),
            'content_areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.ContentArea']", 'symmetrical': 'False', 'blank': 'True'}),
            'content_standards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tick.CoreContent']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 2, 14)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entered_by': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '255'}),
            'feebased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'focus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tick.Focus']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'levels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Level']", 'symmetrical': 'False', 'blank': 'True'}),
            'loti_level': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'programs_of_studies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tick.ProgramOfStudy']", 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resource_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'source': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '55', 'null': 'True', 'blank': 'True'}),
            'sub_focus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tick.SubFocus']", 'null': 'True', 'blank': 'True'}),
            'tech_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tick.TechnologyComponent']", 'null': 'True', 'blank': 'True'}),
            'tech_indicators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tick.TechIndicator']", 'null': 'True', 'blank': 'True'}),
            'tech_standards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tick.TechnologyStandard']", 'null': 'True', 'blank': 'True'}),
            'tech_sub_component': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tick.TechnologySubComponent']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tick.subfocus': {
            'Meta': {'ordering': "['name']", 'object_name': 'SubFocus'},
            'focus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tick.Focus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tick.techindicator': {
            'Meta': {'ordering': "['id']", 'object_name': 'TechIndicator'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standard': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tech_standards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tick.TechnologyStandard']", 'symmetrical': 'False'})
        },
        'tick.technologycomponent': {
            'Meta': {'ordering': "['name']", 'object_name': 'TechnologyComponent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tick.technologystandard': {
            'Meta': {'ordering': "['name']", 'object_name': 'TechnologyStandard'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'point': ('django.db.models.fields.IntegerField', [], {}),
            'subpoint': ('django.db.models.fields.IntegerField', [], {})
        },
        'tick.technologysubcomponent': {
            'Meta': {'ordering': "['name']", 'object_name': 'TechnologySubComponent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tech_component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tick.TechnologyComponent']"})
        }
    }

    complete_apps = ['tick']
