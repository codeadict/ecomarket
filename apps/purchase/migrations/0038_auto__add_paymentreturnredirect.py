# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaymentReturnRedirect'
        db.create_table('purchase_paymentreturnredirect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('payment_already_processed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('purchase', ['PaymentReturnRedirect'])


    def backwards(self, orm):
        # Deleting model 'PaymentReturnRedirect'
        db.delete_table('purchase_paymentreturnredirect')


    models = {
        'accounts.shippingaddress': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'ShippingAddress'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Country']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_select_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'line1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': "orm['auth.User']"})
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
            'is_chat_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message_after_purchasing': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'paypal_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'phone_landline': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'refunds_policy': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'returns_policy': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '60'}),
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
        },
        'purchase.cart': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Cart'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'cart'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'purchase.cartproduct': {
            'Meta': {'ordering': "('cart_stall',)", 'object_name': 'CartProduct'},
            'cart_stall': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cart_products'", 'to': "orm['purchase.CartStall']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'unit_price': ('marketplace.fields.NullableMoneyField', [], {'default': 'None', 'no_currency_field': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'unit_price_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'GBP'", 'max_length': '3'})
        },
        'purchase.cartstall': {
            'Meta': {'object_name': 'CartStall'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cart_stalls'", 'null': 'True', 'to': "orm['accounts.ShippingAddress']"}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cart_stalls'", 'to': "orm['purchase.Cart']"}),
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'checked_out_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'coupon_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'speculative_country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Country']", 'null': 'True'}),
            'stall': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Stall']"})
        },
        'purchase.lineitem': {
            'Meta': {'object_name': 'LineItem'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_items'", 'to': "orm['purchase.Order']"}),
            'price': ('marketplace.fields.NullableMoneyField', [], {'default': 'None', 'no_currency_field': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'price_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'GBP'", 'max_length': '3'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marketplace.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'refund': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'line_items'", 'null': 'True', 'to': "orm['purchase.Refund']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'purchase.order': {
            'Meta': {'object_name': 'Order'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.ShippingAddress']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_charge': ('marketplace.fields.NullableMoneyField', [], {'default': 'None', 'no_currency_field': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'delivery_charge_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'GBP'", 'max_length': '3'}),
            'discount_amount': ('marketplace.fields.NullableMoneyField', [], {'default': '0', 'no_currency_field': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'discount_amount_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'GBP'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_joomla_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'note': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'stall': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['marketplace.Stall']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['auth.User']"})
        },
        'purchase.orderfeedback': {
            'Meta': {'object_name': 'OrderFeedback'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feedback_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'feedback'", 'unique': 'True', 'null': 'True', 'to': "orm['purchase.Order']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'purchase.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('marketplace.fields.NullableMoneyField', [], {'default': 'None', 'no_currency_field': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'amount_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'GBP'", 'max_length': '3'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'debug_request': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'debug_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'discount_amount': ('marketplace.fields.NullableMoneyField', [], {'default': '0', 'no_currency_field': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'discount_amount_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'GBP'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logged_to_google': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'payment'", 'unique': 'True', 'null': 'True', 'to': "orm['purchase.Order']"}),
            'pay_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_made'", 'to': "orm['auth.User']"}),
            'secret_uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '200'}),
            'status_detail': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'purchase.paymentattempt': {
            'Meta': {'object_name': 'PaymentAttempt'},
            'cart_stall': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_attempts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['purchase.CartStall']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'payment_attempt'", 'unique': 'True', 'to': "orm['purchase.Payment']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'purchase.paymentreturnredirect': {
            'Meta': {'object_name': 'PaymentReturnRedirect'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_already_processed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'purchase.refund': {
            'Meta': {'object_name': 'Refund'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'refunds'", 'to': "orm['purchase.Order']"}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['purchase']