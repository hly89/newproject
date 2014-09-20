# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'UserProfile', fields ['institute_info']
        db.delete_unique('breeze_userprofile', ['institute_info_id'])


    def backwards(self, orm):
        # Adding unique constraint on 'UserProfile', fields ['institute_info']
        db.create_unique('breeze_userprofile', ['institute_info_id'])


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
        'breeze.apps': {
            'Meta': {'ordering': "['author']", 'object_name': 'apps', '_ormbases': ['shop.Product']},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shop.Product']", 'unique': 'True', 'primary_key': 'True'})
        },
        'breeze.cartinfo': {
            'Meta': {'ordering': "['active']", 'object_name': 'CartInfo'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['breeze.Rscripts']"}),
            'script_buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'type_app': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
        'breeze.institute': {
            'Meta': {'object_name': 'Institute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.CharField', [], {'max_length': '75'})
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
            'access': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'default': 'None', 'to': "orm['auth.User']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['breeze.Script_categories']", 'to_field': "'category'"}),
            'code': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '5500', 'blank': 'True'}),
            'docxml': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'header': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inln': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'install_date': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'installdate'", 'default': 'None', 'to': "orm['breeze.User_date']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'istag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'must': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'order': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '1', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '19', 'decimal_places': '2'}),
            'report_type': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['breeze.ReportType']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'})
        },
        'breeze.script_categories': {
            'Meta': {'object_name': 'Script_categories'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '55'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '350', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'breeze.statistics': {
            'Meta': {'ordering': "['-times']", 'object_name': 'Statistics'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'istag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'script': ('django.db.models.fields.CharField', [], {'max_length': '55'}),
            'times': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'breeze.user_date': {
            'Meta': {'object_name': 'User_date'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'breeze.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'fimm_group': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['breeze.Institute']"}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shop.product': {
            'Meta': {'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_shop.product_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'})
        }
    }

    complete_apps = ['breeze']