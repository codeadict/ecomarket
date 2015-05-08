# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ProductFormErrors.rules_error'
        db.delete_column('analytics_productformerrors', 'rules_error')

        # Adding field 'ProductFormErrors.had_error'
        db.add_column('analytics_productformerrors', 'had_error',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ProductFormErrors.rules_error'
        db.add_column('analytics_productformerrors', 'rules_error',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'ProductFormErrors.had_error'
        db.delete_column('analytics_productformerrors', 'had_error')


    models = {
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
        'analytics.aggregatedata': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'AggregateData'},
            'campaign': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'campaign_cost': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer_acquistion_cost': ('django.db.models.fields.FloatField', [], {}),
            'daily_acquired': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'gross_merchant_value': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'revenue_after_commission': ('django.db.models.fields.FloatField', [], {})
        },
        'analytics.campaigntrack': {
            'Meta': {'unique_together': "(('user', 'name'),)", 'object_name': 'CampaignTrack'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'cookie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['analytics.LifetimeTrack']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_lead': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'campaigns'", 'null': 'True', 'to': "orm['mailing_lists.MailingListSignup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'query_string': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'sent_to_sailthru': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'campaigns'", 'null': 'True', 'to': "orm['auth.User']"}),
            'utmz': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'analytics.lifetimetrack': {
            'Meta': {'object_name': 'LifetimeTrack'},
            'acquired_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'activated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'actual_activated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'actual_referred_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'actual_retained_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cookie_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_lead': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['mailing_lists.MailingListSignup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchased_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'referred_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'retained_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'url_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'analytics.productformerrors': {
            'Meta': {'object_name': 'ProductFormErrors'},
            'amount_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'colors_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'had_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images_formset_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords_field_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_form_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'primary_category_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Product']", 'null': 'True', 'blank': 'True'}),
            'product_form_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipients_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipping_form_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipping_profile_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stall': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Stall']"}),
            'title_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        'mailing_lists.mailinglistsignup': {
            'Meta': {'object_name': 'MailingListSignup'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Category']", 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Country']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('mailing_lists.models.EditableAutoNowAddDateTimeField', [], {'auto_now_add': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_seller_lead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'marketing_optin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'member_type': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'RP'", 'max_length': '2'}),
            'telephone_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'marketplace.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_src': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'navigation_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['marketplace.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'marketplace.cause': {
            'Meta': {'object_name': 'Cause'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'marketplace.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'cause': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certificates'", 'to': "orm['marketplace.Cause']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'marketplace.color': {
            'Meta': {'object_name': 'Color'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'marketplace.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'marketplace.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'marketplace.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'marketplace.material': {
            'Meta': {'object_name': 'Material'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'marketplace.occasion': {
            'Meta': {'object_name': 'Occasion'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'marketplace.product': {
            'Meta': {'object_name': 'Product'},
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Cause']"}),
            'certificates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Certificate']"}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'to': "orm['marketplace.Color']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Ingredient']"}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Keyword']"}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Material']"}),
            'number_of_recent_sales': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'number_of_sales': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'occasions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Occasion']"}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'to': "orm['marketplace.Category']"}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'to': "orm['marketplace.Recipient']"}),
            'secondary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secondary_products'", 'null': 'True', 'to': "orm['marketplace.Category']"}),
            'shipping_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['marketplace.ShippingProfile']"}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'stall': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['marketplace.Stall']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'}),
            'stock': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'marketplace.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '511', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'marketplace.shippingprofile': {
            'Meta': {'unique_together': "(('stall', 'title'),)", 'object_name': 'ShippingProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'others_delivery_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'others_delivery_time_max': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'others_price': ('marketplace.fields.NullableMoneyField', [], {'decimal_places': '2', 'default': 'None', 'no_currency_field': 'True', 'max_digits': '6', 'blank': 'True', 'null': 'True'}),
            'others_price_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': '"GBP"', 'max_length': '3'}),
            'others_price_extra': ('marketplace.fields.NullableMoneyField', [], {'decimal_places': '2', 'default': 'None', 'no_currency_field': 'True', 'max_digits': '6', 'blank': 'True', 'null': 'True'}),
            'others_price_extra_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': '"GBP"', 'max_length': '3'}),
            'shipping_country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shipping_profile'", 'to': "orm['marketplace.Country']"}),
            'shipping_postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'stall': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shipping_profile'", 'to': "orm['marketplace.Stall']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.stall': {
            'Meta': {'object_name': 'Stall'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stalls'", 'null': 'True', 'to': "orm['marketplace.StallCategory']"}),
            'chat_operator_uri': ('django.db.models.fields.URLField', [], {'default': 'False', 'max_length': '200', 'blank': 'True'}),
            'chat_stall_uri': ('django.db.models.fields.URLField', [], {'default': 'False', 'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description_full': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'description_short': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '90', 'blank': 'True'}),
            'email_opt_in': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'holiday_message': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'holiday_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '8'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_chat_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_stock_checked_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'message_after_purchasing': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'number_of_calls': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'paypal_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'phone_landline': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'reason_for_suspension': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'refunds_policy': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'renewal_tier': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'returns_policy': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '60'}),
            'total_gmv_till_yesterday': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'total_live_products_till_yesterday': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'total_messages_received_till_yesterday': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'total_orders_till_yesterday': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'total_products_till_yesterday': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'total_suspensions_till_yesterday': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'stall'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'marketplace.stallcategory': {
            'Meta': {'object_name': 'StallCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['marketplace.StallCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['analytics']