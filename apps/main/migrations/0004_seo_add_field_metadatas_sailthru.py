# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    field_names = [
        "sailthru_image",
        "sailthru_image_thumb",
        "sailthru_title",
        "sailthru_stall_title",
        "sailthru_stall_url",
        "sailthru_stall_owner_id",
    ]

    def forwards(self, orm):
        for field_name in self.field_names:
            try:
                # Adding field to 'MetadataView'
                db.add_column('seo_metadataview', field_name,
                              self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                              keep_default=False)

                # Adding field to 'MetadataPath'
                db.add_column('seo_metadatapath', field_name,
                              self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                              keep_default=False)

                # Adding field to 'MetadataModel'
                db.add_column('seo_metadatamodel', field_name,
                              self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                              keep_default=False)

                # Adding field to 'MetadataModelInstance'
                db.add_column('seo_metadatamodelinstance', field_name,
                              self.gf('django.db.models.fields.CharField')(default='', max_length=511, blank=True),
                              keep_default=False)
            except:
                print "Error adding {}".format(field_name)


    def backwards(self, orm):
        for field_name in self.field_names:
            # Deleting field from 'MetadataView'
            db.delete_column('seo_metadataview', field_name)

            # Deleting field from 'MetadataPath'
            db.delete_column('seo_metadatapath', field_name)

            # Deleting field from 'MetadataModel'
            db.delete_column('seo_metadatamodel', field_name)

            # Deleting field from 'MetadataModelInstance'
            db.delete_column('seo_metadatamodelinstance', field_name)

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
            'sailthru_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_image_thumb': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_owner_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
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
            'sailthru_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_image_thumb': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_owner_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
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
            'sailthru_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_image_thumb': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_owner_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
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
            'sailthru_image': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_image_thumb': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'sailthru_stall_owner_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '511', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['seo', 'main']
