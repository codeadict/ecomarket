# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.social_auth'
        db.add_column('accounts_userprofile', 'social_auth',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.social_auth'
        db.delete_column('accounts_userprofile', 'social_auth')


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
        'accounts.shippingaddress': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'ShippingAddress'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Country']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': "orm['auth.User']"})
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
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Country']"}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_newsletters': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'social_auth': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'})
        },
        'actstream.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_object'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        },
        'marketplace.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['accounts']