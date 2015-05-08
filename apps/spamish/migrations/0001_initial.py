# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BannedWord'
        db.create_table('spamish_bannedword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('spamish', ['BannedWord'])


    def backwards(self, orm):
        # Deleting model 'BannedWord'
        db.delete_table('spamish_bannedword')


    models = {
        'spamish.bannedword': {
            'Meta': {'ordering': "('word',)", 'object_name': 'BannedWord'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['spamish']