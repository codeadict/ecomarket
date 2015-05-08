# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db.utils import DatabaseError


class Migration(SchemaMigration):

    def forwards(self, orm):
        try:
            db.rename_table("seo_marketplacemetadatamodel", "seo_metadatamodel")
            db.rename_table("seo_marketplacemetadatamodelinstance", "seo_metadatamodelinstance")
            db.rename_table("seo_marketplacemetadatapath", "seo_metadatapath")
            db.rename_table("seo_marketplacemetadataview", "seo_metadataview")
        except DatabaseError:
            # The SEO app makes us cry
            pass

    def backwards(self, orm):
        try:
            db.rename_table("seo_metadatamodel", "seo_marketplacemetadatamodel")
            db.rename_table("seo_metadatamodelinstance", "seo_marketplacemetadatamodelinstance")
            db.rename_table("seo_metadatapath", "seo_marketplacemetadatapath")
            db.rename_table("seo_metadataview", "seo_marketplacemetadataview")
        except DatabaseError:
            # The SEO app makes us cry
            pass

    models = {}

    complete_apps = ['main']
