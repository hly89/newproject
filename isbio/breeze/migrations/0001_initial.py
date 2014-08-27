# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table('breeze_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=3500)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('breeze', ['Post'])

        # Adding model 'Project'
        db.create_table('breeze_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('manager', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pi', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('collaborative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wbs', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1100, blank=True)),
        ))
        db.send_create_signal('breeze', ['Project'])

        # Adding model 'Group'
        db.create_table('breeze_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('breeze', ['Group'])

        # Adding M2M table for field team on 'Group'
        db.create_table('breeze_group_team', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['breeze.group'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('breeze_group_team', ['group_id', 'user_id'])

        # Adding model 'ReportType'
        db.create_table('breeze_reporttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=17)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=5500, blank=True)),
            ('search', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('config', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('breeze', ['ReportType'])

        # Adding M2M table for field access on 'ReportType'
        db.create_table('breeze_reporttype_access', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reporttype', models.ForeignKey(orm['breeze.reporttype'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('breeze_reporttype_access', ['reporttype_id', 'user_id'])

        # Adding model 'Rscripts'
        db.create_table('breeze_rscripts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=35)),
            ('inln', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=5500, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(default=u'general', max_length=25)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('istag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('must', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=3, decimal_places=1, blank=True)),
            ('docxml', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('code', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('header', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('breeze', ['Rscripts'])

        # Adding M2M table for field report_type on 'Rscripts'
        db.create_table('breeze_rscripts_report_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rscripts', models.ForeignKey(orm['breeze.rscripts'], null=False)),
            ('reporttype', models.ForeignKey(orm['breeze.reporttype'], null=False))
        ))
        db.create_unique('breeze_rscripts_report_type', ['rscripts_id', 'reporttype_id'])

        # Adding model 'Jobs'
        db.create_table('breeze_jobs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jname', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('jdetails', self.gf('django.db.models.fields.CharField')(max_length=4900, blank=True)),
            ('juser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('script', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['breeze.Rscripts'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('staged', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('progress', self.gf('django.db.models.fields.IntegerField')()),
            ('sgeid', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('docxml', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('rexecut', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('breeze', ['Jobs'])

        # Adding model 'DataSet'
        db.create_table('breeze_dataset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=55)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=350, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('rdata', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('breeze', ['DataSet'])

        # Adding model 'InputTemplate'
        db.create_table('breeze_inputtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=55)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=350, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('breeze', ['InputTemplate'])

        # Adding model 'UserProfile'
        db.create_table('breeze_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('fimm_group', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('logo', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('breeze', ['UserProfile'])

        # Adding model 'Report'
        db.create_table('breeze_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['breeze.ReportType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=55)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=350, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('home', self.gf('django.db.models.fields.CharField')(max_length=155, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('progress', self.gf('django.db.models.fields.IntegerField')()),
            ('sgeid', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['breeze.Project'], null=True, blank=True)),
            ('rexec', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('dochtml', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('breeze', ['Report'])

        # Adding M2M table for field shared on 'Report'
        db.create_table('breeze_report_shared', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm['breeze.report'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('breeze_report_shared', ['report_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table('breeze_post')

        # Deleting model 'Project'
        db.delete_table('breeze_project')

        # Deleting model 'Group'
        db.delete_table('breeze_group')

        # Removing M2M table for field team on 'Group'
        db.delete_table('breeze_group_team')

        # Deleting model 'ReportType'
        db.delete_table('breeze_reporttype')

        # Removing M2M table for field access on 'ReportType'
        db.delete_table('breeze_reporttype_access')

        # Deleting model 'Rscripts'
        db.delete_table('breeze_rscripts')

        # Removing M2M table for field report_type on 'Rscripts'
        db.delete_table('breeze_rscripts_report_type')

        # Deleting model 'Jobs'
        db.delete_table('breeze_jobs')

        # Deleting model 'DataSet'
        db.delete_table('breeze_dataset')

        # Deleting model 'InputTemplate'
        db.delete_table('breeze_inputtemplate')

        # Deleting model 'UserProfile'
        db.delete_table('breeze_userprofile')

        # Deleting model 'Report'
        db.delete_table('breeze_report')

        # Removing M2M table for field shared on 'Report'
        db.delete_table('breeze_report_shared')


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
        'breeze.dataset': {
            'Meta': {'object_name': 'DataSet'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '350', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'}),
            'rdata': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'breeze.group': {
            'Meta': {'object_name': 'Group'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'group_content'", 'default': 'None', 'to': "orm['auth.User']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        'breeze.inputtemplate': {
            'Meta': {'object_name': 'InputTemplate'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '350', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'})
        },
        'breeze.jobs': {
            'Meta': {'object_name': 'Jobs'},
            'docxml': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jdetails': ('django.db.models.fields.CharField', [], {'max_length': '4900', 'blank': 'True'}),
            'jname': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'juser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'progress': ('django.db.models.fields.IntegerField', [], {}),
            'rexecut': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'script': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['breeze.Rscripts']"}),
            'sgeid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'staged': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'breeze.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '3500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'breeze.project': {
            'Meta': {'object_name': 'Project'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'collaborative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1100', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'pi': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'wbs': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'breeze.report': {
            'Meta': {'object_name': 'Report'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '350', 'blank': 'True'}),
            'dochtml': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'home': ('django.db.models.fields.CharField', [], {'max_length': '155', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'progress': ('django.db.models.fields.IntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['breeze.Project']", 'null': 'True', 'blank': 'True'}),
            'rexec': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'sgeid': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'shared': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'report_shares'", 'default': 'None', 'to': "orm['auth.User']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['breeze.ReportType']"})
        },
        'breeze.reporttype': {
            'Meta': {'ordering': "('type',)", 'object_name': 'ReportType'},
            'access': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pipeline_access'", 'default': 'None', 'to': "orm['auth.User']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'config': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '5500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '17'})
        },
        'breeze.rscripts': {
            'Meta': {'ordering': "['name']", 'object_name': 'Rscripts'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'category': ('django.db.models.fields.CharField', [], {'default': "u'general'", 'max_length': '25'}),
            'code': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '5500', 'blank': 'True'}),
            'docxml': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'header': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inln': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'istag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'must': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'order': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '1', 'blank': 'True'}),
            'report_type': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['breeze.ReportType']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'})
        },
        'breeze.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'fimm_group': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['breeze']