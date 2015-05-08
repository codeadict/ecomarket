# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OldCategory'
        db.create_table('product_tmp_oldcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['product_tmp.OldCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('product_tmp', ['OldCategory'])

        # Adding model 'TempProduct'
        db.create_table('product_tmp_tempproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('colors', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('old_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product_tmp.OldCategory'], null=True, blank=True)),
            ('primary_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marketplace.Category'], null=True, blank=True)),
            ('secondary_category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tmp_products_sec', null=True, to=orm['marketplace.Category'])),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal('product_tmp', ['TempProduct'])


    def backwards(self, orm):
        # Deleting model 'OldCategory'
        db.delete_table('product_tmp_oldcategory')

        # Deleting model 'TempProduct'
        db.delete_table('product_tmp_tempproduct')


    models = {
        'marketplace.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['marketplace.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'product_tmp.oldcategory': {
            'Meta': {'object_name': 'OldCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['product_tmp.OldCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'product_tmp.tempproduct': {
            'Meta': {'object_name': 'TempProduct'},
            'colors': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'old_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product_tmp.OldCategory']", 'null': 'True', 'blank': 'True'}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Category']", 'null': 'True', 'blank': 'True'}),
            'secondary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tmp_products_sec'", 'null': 'True', 'to': "orm['marketplace.Category']"}),
            'slug': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['product_tmp']