# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MetadataView.sailthru_tags'
        try:
            db.add_column('seo_metadataview', 'sailthru_tags',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                          keep_default=False)

            # Adding field 'MetadataPath.sailthru_tags'
            db.add_column('seo_metadatapath', 'sailthru_tags',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                          keep_default=False)

            # Adding field 'MetadataModel.sailthru_tags'
            db.add_column('seo_metadatamodel', 'sailthru_tags',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                          keep_default=False)

            # Adding field 'MetadataModelInstance.sailthru_tags'
            db.add_column('seo_metadatamodelinstance', 'sailthru_tags',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                          keep_default=False)
        except:
            pass


    def backwards(self, orm):
        # Deleting field 'MetadataView.sailthru_tags'
        db.delete_column('seo_metadataview', 'sailthru_tags')

        # Deleting field 'MetadataPath.sailthru_tags'
        db.delete_column('seo_metadatapath', 'sailthru_tags')

        # Deleting field 'MetadataModel.sailthru_tags'
        db.delete_column('seo_metadatamodel', 'sailthru_tags')

        # Deleting field 'MetadataModelInstance.sailthru_tags'
        db.delete_column('seo_metadatamodelinstance', 'sailthru_tags')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'seo.metadatamodel': {
            'Meta': {'unique_together': "(('_content_type',),)", 'object_name': 'MetadataModel'},
            '_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'canonical_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_tags': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'seo.metadatamodelinstance': {
            'Meta': {'unique_together': "(('_path',), ('_content_type', '_object_id'))", 'object_name': 'MetadataModelInstance'},
            '_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            '_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            '_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'canonical_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_tags': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'seo.metadatapath': {
            'Meta': {'unique_together': "(('_path',),)", 'object_name': 'MetadataPath'},
            '_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'canonical_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_tags': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'seo.metadataview': {
            'Meta': {'unique_together': "(('_view',),)", 'object_name': 'MetadataView'},
            '_view': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'canonical_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_tags': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['seo', 'main']