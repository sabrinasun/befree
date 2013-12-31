# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'accounts_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mugshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('privacy', self.gf('django.db.models.fields.CharField')(default='registered', max_length=15)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('is_nonprofit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paypal_email', self.gf('django.db.models.fields.EmailField')(max_length=100, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('payment_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('max_per_order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('international_free_shipping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('domestic_free_shipping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('is_reader', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_giver', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'accounts', ['Profile'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'accounts_profile')


    models = {
        u'accounts.profile': {
            'Meta': {'object_name': 'Profile'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '50'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domestic_free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international_free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_giver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_nonprofit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_reader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_per_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'payment_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paypal_email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']