# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user_profile', unique=True, to=orm['auth.User'])),
            ('gender', self.gf('django.db.models.fields.CharField')(default='', max_length=1)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(default='')),
            ('send_newsletters', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('address_2', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('country', self.gf('django_countries.fields.CountryField')(default='GB', max_length=2)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])

        # Adding model 'EmailNotification'
        db.create_table('accounts_emailnotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('annoying.fields.AutoOneToOneField')(related_name='email_notification', unique=True, to=orm['auth.User'])),
            ('product_inspirations', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('site_updates_features', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('stall_owner_tips', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('follower_notifications', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('love_list_notifications', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('private_messages', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('orders', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('customer_reviews', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('accounts', ['EmailNotification'])

        # Adding model 'Privacy'
        db.create_table('accounts_privacy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('annoying.fields.AutoOneToOneField')(related_name='privacy', unique=True, to=orm['auth.User'])),
            ('profile_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('share_purchases_in_activity', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('love_list_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('share_love_list_in_activity', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('accounts', ['Privacy'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')

        # Deleting model 'EmailNotification'
        db.delete_table('accounts_emailnotification')

        # Deleting model 'Privacy'
        db.delete_table('accounts_privacy')


    models = {
        'accounts.emailnotification': {
            'Meta': {'object_name': 'EmailNotification'},
            'customer_reviews': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'follower_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'love_list_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'orders': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'private_messages': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product_inspirations': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site_updates_features': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stall_owner_tips': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('annoying.fields.AutoOneToOneField', [], {'related_name': "'email_notification'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'accounts.privacy': {
            'Meta': {'object_name': 'Privacy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'love_list_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'profile_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'share_love_list_in_activity': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'share_purchases_in_activity': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('annoying.fields.AutoOneToOneField', [], {'related_name': "'privacy'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about_me': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'activation_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'address_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'address_2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'country': ('django_countries.fields.CountryField', [], {'default': "'GB'", 'max_length': '2'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_newsletters': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'})
        },
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']