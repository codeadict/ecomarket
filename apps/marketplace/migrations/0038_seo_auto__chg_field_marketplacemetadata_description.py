# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import DatabaseError


class Migration(SchemaMigration):

    def forwards(self, orm):

        try:
            # Changing field 'MarketplaceMetadataPath.description'
            db.alter_column('seo_marketplacemetadatapath', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

            # Changing field 'MarketplaceMetadataPath.title'
            db.alter_column('seo_marketplacemetadatapath', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

            # Changing field 'MarketplaceMetadataModel.description'
            db.alter_column('seo_marketplacemetadatamodel', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

            # Changing field 'MarketplaceMetadataModel.title'
            db.alter_column('seo_marketplacemetadatamodel', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

            # Changing field 'MarketplaceMetadataView.description'
            db.alter_column('seo_marketplacemetadataview', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

            # Changing field 'MarketplaceMetadataView.title'
            db.alter_column('seo_marketplacemetadataview', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

            # Changing field 'MarketplaceMetadataModelInstance.description'
            db.alter_column('seo_marketplacemetadatamodelinstance', 'description', self.gf('django.db.models.fields.CharField')(max_length=255))

            # Changing field 'MarketplaceMetadataModelInstance.title'
            db.alter_column('seo_marketplacemetadatamodelinstance', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))
        except DatabaseError:
            # SEO app makes us cry
            pass

    def backwards(self, orm):

        try:
            # Changing field 'MarketplaceMetadataPath.description'
            db.alter_column('seo_marketplacemetadatapath', 'description', self.gf('django.db.models.fields.CharField')(max_length=155))

            # Changing field 'MarketplaceMetadataPath.title'
            db.alter_column('seo_marketplacemetadatapath', 'title', self.gf('django.db.models.fields.CharField')(max_length=68))

            # Changing field 'MarketplaceMetadataModel.description'
            db.alter_column('seo_marketplacemetadatamodel', 'description', self.gf('django.db.models.fields.CharField')(max_length=155))

            # Changing field 'MarketplaceMetadataModel.title'
            db.alter_column('seo_marketplacemetadatamodel', 'title', self.gf('django.db.models.fields.CharField')(max_length=68))

            # Changing field 'MarketplaceMetadataView.description'
            db.alter_column('seo_marketplacemetadataview', 'description', self.gf('django.db.models.fields.CharField')(max_length=155))

            # Changing field 'MarketplaceMetadataView.title'
            db.alter_column('seo_marketplacemetadataview', 'title', self.gf('django.db.models.fields.CharField')(max_length=68))

            # Changing field 'MarketplaceMetadataModelInstance.description'
            db.alter_column('seo_marketplacemetadatamodelinstance', 'description', self.gf('django.db.models.fields.CharField')(max_length=155))

            # Changing field 'MarketplaceMetadataModelInstance.title'
            db.alter_column('seo_marketplacemetadatamodelinstance', 'title', self.gf('django.db.models.fields.CharField')(max_length=68))
        except DatabaseError:
            # SEO app makes us cry
            pass

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
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'og_video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '155', 'blank': 'True'})
        },
        'seo.marketplacemetadatamodelinstance': {
            'Meta': {'unique_together': "(('_path',), ('_content_type', '_object_id'))", 'object_name': 'MarketplaceMetadataModelInstance'},
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
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '155', 'blank': 'True'})
        },
        'seo.marketplacemetadatapath': {
            'Meta': {'unique_together': "(('_path',),)", 'object_name': 'MarketplaceMetadataPath'},
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
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '155', 'blank': 'True'})
        },
        'seo.marketplacemetadataview': {
            'Meta': {'unique_together': "(('_view',),)", 'object_name': 'MarketplaceMetadataView'},
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
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '155', 'blank': 'True'})
        }
    }

    complete_apps = ['seo']
