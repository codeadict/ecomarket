# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('marketplace_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['marketplace.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('marketplace', ['Category'])

        # Adding model 'Cause'
        db.create_table('marketplace_cause', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('marketplace', ['Cause'])

        # Adding model 'Certificate'
        db.create_table('marketplace_certificate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('marketplace', ['Certificate'])

        # Adding model 'Color'
        db.create_table('marketplace_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('marketplace', ['Color'])

        # Adding model 'Ingredient'
        db.create_table('marketplace_ingredient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('marketplace', ['Ingredient'])

        # Adding model 'Material'
        db.create_table('marketplace_material', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('marketplace', ['Material'])

        # Adding model 'Keyword'
        db.create_table('marketplace_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('marketplace', ['Keyword'])

        # Adding model 'Occasion'
        db.create_table('marketplace_occasion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('marketplace', ['Occasion'])

        # Adding model 'Recipient'
        db.create_table('marketplace_recipient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('marketplace', ['Recipient'])

        # Adding model 'StallCategory'
        db.create_table('marketplace_stallcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['marketplace.StallCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('marketplace', ['StallCategory'])

        # Adding model 'Stall'
        db.create_table('marketplace_stall', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='stall', unique=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=60)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('description_short', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('description_full', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('paypal_email', self.gf('django.db.models.fields.EmailField')(default='', max_length=255, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('twitter_username', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('message_after_purchasing', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('refunds_policy', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('returns_policy', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('holiday_mode', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('holiday_message', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='stalls', null=True, to=orm['marketplace.StallCategory'])),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal('marketplace', ['Stall'])

        # Adding model 'Price'
        db.create_table('marketplace_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prices', to=orm['marketplace.Product'])),
            ('price', self.gf('money.contrib.django.models.fields.MoneyField')(default=None, no_currency_field=True, max_digits=6, decimal_places=2, blank=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('price_currency', self.gf('money.contrib.django.models.fields.CurrencyField')(default='GBP', max_length=3)),
            ('updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('marketplace', ['Price'])

        # Adding model 'Product'
        db.create_table('marketplace_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stall', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['marketplace.Stall'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
            ('stock', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('primary_category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='products', null=True, to=orm['marketplace.Category'])),
            ('secondary_category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='secondary_products', null=True, to=orm['marketplace.Category'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='d', max_length=1)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('marketplace', ['Product'])

        # Adding M2M table for field causes on 'Product'
        db.create_table('marketplace_product_causes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['marketplace.product'], null=False)),
            ('cause', models.ForeignKey(orm['marketplace.cause'], null=False))
        ))
        db.create_unique('marketplace_product_causes', ['product_id', 'cause_id'])

        # Adding M2M table for field certificates on 'Product'
        db.create_table('marketplace_product_certificates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['marketplace.product'], null=False)),
            ('certificate', models.ForeignKey(orm['marketplace.certificate'], null=False))
        ))
        db.create_unique('marketplace_product_certificates', ['product_id', 'certificate_id'])

        # Adding M2M table for field colors on 'Product'
        db.create_table('marketplace_product_colors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['marketplace.product'], null=False)),
            ('color', models.ForeignKey(orm['marketplace.color'], null=False))
        ))
        db.create_unique('marketplace_product_colors', ['product_id', 'color_id'])

        # Adding M2M table for field ingredients on 'Product'
        db.create_table('marketplace_product_ingredients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['marketplace.product'], null=False)),
            ('ingredient', models.ForeignKey(orm['marketplace.ingredient'], null=False))
        ))
        db.create_unique('marketplace_product_ingredients', ['product_id', 'ingredient_id'])

        # Adding M2M table for field materials on 'Product'
        db.create_table('marketplace_product_materials', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['marketplace.product'], null=False)),
            ('material', models.ForeignKey(orm['marketplace.material'], null=False))
        ))
        db.create_unique('marketplace_product_materials', ['product_id', 'material_id'])

        # Adding M2M table for field keywords on 'Product'
        db.create_table('marketplace_product_keywords', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['marketplace.product'], null=False)),
            ('keyword', models.ForeignKey(orm['marketplace.keyword'], null=False))
        ))
        db.create_unique('marketplace_product_keywords', ['product_id', 'keyword_id'])

        # Adding M2M table for field occasions on 'Product'
        db.create_table('marketplace_product_occasions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['marketplace.product'], null=False)),
            ('occasion', models.ForeignKey(orm['marketplace.occasion'], null=False))
        ))
        db.create_unique('marketplace_product_occasions', ['product_id', 'occasion_id'])

        # Adding M2M table for field recipients on 'Product'
        db.create_table('marketplace_product_recipients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['marketplace.product'], null=False)),
            ('recipient', models.ForeignKey(orm['marketplace.recipient'], null=False))
        ))
        db.create_unique('marketplace_product_recipients', ['product_id', 'recipient_id'])

        # Adding model 'ProductImage'
        db.create_table('marketplace_productimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['marketplace.Product'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='name', overwrite=False)),
            ('data', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('marketplace', ['ProductImage'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('marketplace_category')

        # Deleting model 'Cause'
        db.delete_table('marketplace_cause')

        # Deleting model 'Certificate'
        db.delete_table('marketplace_certificate')

        # Deleting model 'Color'
        db.delete_table('marketplace_color')

        # Deleting model 'Ingredient'
        db.delete_table('marketplace_ingredient')

        # Deleting model 'Material'
        db.delete_table('marketplace_material')

        # Deleting model 'Keyword'
        db.delete_table('marketplace_keyword')

        # Deleting model 'Occasion'
        db.delete_table('marketplace_occasion')

        # Deleting model 'Recipient'
        db.delete_table('marketplace_recipient')

        # Deleting model 'StallCategory'
        db.delete_table('marketplace_stallcategory')

        # Deleting model 'Stall'
        db.delete_table('marketplace_stall')

        # Deleting model 'Price'
        db.delete_table('marketplace_price')

        # Deleting model 'Product'
        db.delete_table('marketplace_product')

        # Removing M2M table for field causes on 'Product'
        db.delete_table('marketplace_product_causes')

        # Removing M2M table for field certificates on 'Product'
        db.delete_table('marketplace_product_certificates')

        # Removing M2M table for field colors on 'Product'
        db.delete_table('marketplace_product_colors')

        # Removing M2M table for field ingredients on 'Product'
        db.delete_table('marketplace_product_ingredients')

        # Removing M2M table for field materials on 'Product'
        db.delete_table('marketplace_product_materials')

        # Removing M2M table for field keywords on 'Product'
        db.delete_table('marketplace_product_keywords')

        # Removing M2M table for field occasions on 'Product'
        db.delete_table('marketplace_product_occasions')

        # Removing M2M table for field recipients on 'Product'
        db.delete_table('marketplace_product_recipients')

        # Deleting model 'ProductImage'
        db.delete_table('marketplace_productimage')


    models = {
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
        'marketplace.cause': {
            'Meta': {'object_name': 'Cause'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.color': {
            'Meta': {'object_name': 'Color'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.material': {
            'Meta': {'object_name': 'Material'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.occasion': {
            'Meta': {'object_name': 'Occasion'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.price': {
            'Meta': {'object_name': 'Price'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('money.contrib.django.models.fields.MoneyField', [], {'default': 'None', 'no_currency_field': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'price_currency': ('money.contrib.django.models.fields.CurrencyField', [], {'default': "'GBP'", 'max_length': '3'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prices'", 'to': "orm['marketplace.Product']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'marketplace.product': {
            'Meta': {'object_name': 'Product'},
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Cause']"}),
            'certificates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Certificate']"}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Color']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Ingredient']"}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Keyword']"}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Material']"}),
            'occasions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Occasion']"}),
            'primary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'to': "orm['marketplace.Category']"}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['marketplace.Recipient']"}),
            'secondary_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secondary_products'", 'null': 'True', 'to': "orm['marketplace.Category']"}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'stall': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['marketplace.Stall']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'}),
            'stock': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'marketplace.productimage': {
            'Meta': {'ordering': "('created',)", 'object_name': 'ProductImage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['marketplace.Product']"}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'marketplace.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'marketplace.stall': {
            'Meta': {'object_name': 'Stall'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stalls'", 'null': 'True', 'to': "orm['marketplace.StallCategory']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description_full': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'description_short': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'holiday_message': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'holiday_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_after_purchasing': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'paypal_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'refunds_policy': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'returns_policy': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '60'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
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

    complete_apps = ['marketplace']
