# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Order.ship_date'
        db.alter_column(u'core_order', 'ship_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Order.pay_date'
        db.alter_column(u'core_order', 'pay_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Order.ship_date'
        db.alter_column(u'core_order', 'ship_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Order.pay_date'
        db.alter_column(u'core_order', 'pay_date', self.gf('django.db.models.fields.DateTimeField')())

    models = {
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
        },
        u'core.author': {
            'Meta': {'object_name': 'Author'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.givermaterial': {
            'Meta': {'object_name': 'GiverMaterial'},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Material']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'core.material': {
            'Meta': {'object_name': 'Material'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Author']", 'null': 'True', 'blank': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'default': "'Good'", 'max_length': '10'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'has_pic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'pages': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pdf': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Publisher']", 'null': 'True', 'blank': 'True'}),
            'publisher_book_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'})
        },
        u'core.order': {
            'Meta': {'object_name': 'Order'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Material']"}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'pay_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'payment_detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'ship_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'})
        },
        u'core.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['core']