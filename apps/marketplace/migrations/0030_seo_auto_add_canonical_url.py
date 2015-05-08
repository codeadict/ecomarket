# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.db.utils import DatabaseError


class Migration(SchemaMigration):

    def forwards(self, orm):
        try:
            # Adding field 'MarketplaceMetadataPath.canonical_url'
            db.add_column('seo_marketplacemetadatapath', 'canonical_url',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                          keep_default=False)

            # Adding field 'MarketplaceMetadataModel.canonical_url'
            db.add_column('seo_marketplacemetadatamodel', 'canonical_url',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                          keep_default=False)

            # Adding field 'MarketplaceMetadataView.canonical_url'
            db.add_column('seo_marketplacemetadataview', 'canonical_url',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                          keep_default=False)

            # Adding field 'MarketplaceMetadataModelInstance.canonical_url'
            db.add_column('seo_marketplacemetadatamodelinstance', 'canonical_url',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                          keep_default=False)
        except DatabaseError:
            # This is expected because the seo app does not use migrations
            print('Expected database error in seo migration')


    def backwards(self, orm):
        # Deleting field 'MarketplaceMetadataPath.canonical_url'
        db.delete_column('seo_marketplacemetadatapath', 'canonical_url')

        # Deleting field 'MarketplaceMetadataModel.canonical_url'
        db.delete_column('seo_marketplacemetadatamodel', 'canonical_url')

        # Deleting field 'MarketplaceMetadataView.canonical_url'
        db.delete_column('seo_marketplacemetadataview', 'canonical_url')

        # Deleting field 'MarketplaceMetadataModelInstance.canonical_url'
        db.delete_column('seo_marketplacemetadatamodelinstance', 'canonical_url')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'seo.marketplacemetadatamodel': {
            'Meta': {'unique_together': "(('_content_type',),)", 'object_name': 'MarketplaceMetadataModel'},
            '_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'canonical_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '155', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '68', 'blank': 'True'})
        },
        'seo.marketplacemetadatamodelinstance': {
            'Meta': {'unique_together': "(('_path',), ('_content_type', '_object_id'))", 'object_name': 'MarketplaceMetadataModelInstance'},
            '_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            '_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            '_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'canonical_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '155', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '68', 'blank': 'True'})
        },
        'seo.marketplacemetadatapath': {
            'Meta': {'unique_together': "(('_path',),)", 'object_name': 'MarketplaceMetadataPath'},
            '_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'canonical_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '155', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '68', 'blank': 'True'})
        },
        'seo.marketplacemetadataview': {
            'Meta': {'unique_together': "(('_view',),)", 'object_name': 'MarketplaceMetadataView'},
            '_view': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'canonical_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '155', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '68', 'blank': 'True'})
        }
    }

    complete_apps = ['seo']
