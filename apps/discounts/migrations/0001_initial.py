# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CurebitSite'
        db.create_table('discounts_curebitsite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('discounts', ['CurebitSite'])

        # Adding model 'UTMCode'
        db.create_table('discounts_utmcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=127)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(related_name='discounts', to=orm['discounts.CurebitSite'])),
        ))
        db.send_create_signal('discounts', ['UTMCode'])

        # Adding model 'Discount'
        db.create_table('discounts_discount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('percent_discount', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('price_discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('discounts', ['Discount'])


    def backwards(self, orm):
        # Deleting model 'CurebitSite'
        db.delete_table('discounts_curebitsite')

        # Deleting model 'UTMCode'
        db.delete_table('discounts_utmcode')

        # Deleting model 'Discount'
        db.delete_table('discounts_discount')


    models = {
        'discounts.curebitsite': {
            'Meta': {'object_name': 'CurebitSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'discounts.discount': {
            'Meta': {'object_name': 'Discount'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_discount': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'price_discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'})
        },
        'discounts.utmcode': {
            'Meta': {'object_name': 'UTMCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '127'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discounts'", 'to': "orm['discounts.CurebitSite']"})
        }
    }

    complete_apps = ['discounts']