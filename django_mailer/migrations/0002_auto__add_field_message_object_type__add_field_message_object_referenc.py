# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Message.object_type'
        db.add_column('django_mailer_message', 'object_type',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Message.object_reference'
        db.add_column('django_mailer_message', 'object_reference',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Message.object_type'
        db.delete_column('django_mailer_message', 'object_type')

        # Deleting field 'Message.object_reference'
        db.delete_column('django_mailer_message', 'object_reference')


    models = {
        'django_mailer.blacklist': {
            'Meta': {'ordering': "('-date_added',)", 'object_name': 'Blacklist'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'django_mailer.log': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Log'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_message': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_mailer.Message']"}),
            'result': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'django_mailer.message': {
            'Meta': {'ordering': "('date_created',)", 'object_name': 'Message'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'encoded_message': ('django.db.models.fields.TextField', [], {}),
            'from_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_reference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'object_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'to_address': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'django_mailer.queuedmessage': {
            'Meta': {'ordering': "('priority', 'date_queued')", 'object_name': 'QueuedMessage'},
            'date_queued': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deferred': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_mailer.Message']", 'unique': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'retries': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['django_mailer']