# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'core_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Author'])

        # Adding model 'Material'
        db.create_table(u'core_material', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('publisher_book_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pages', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('has_pic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pdf', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'core', ['Material'])

        # Adding M2M table for field author on 'Material'
        m2m_table_name = db.shorten_name(u'core_material_author')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('material', models.ForeignKey(orm[u'core.material'], null=False)),
            ('author', models.ForeignKey(orm[u'core.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['material_id', 'author_id'])

        # Adding model 'GiverMaterial'
        db.create_table(u'core_givermaterial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('giver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('material', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Material'])),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['GiverMaterial'])

        # Adding model 'Order'
        db.create_table(u'core_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reader', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reader_orders', to=orm['auth.User'])),
            ('giver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='giver_orders', to=orm['auth.User'])),
            ('shipping_cost', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('order_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('ship_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('pay_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('payment_detail', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['Order'])

        # Adding model 'OrderDetail'
        db.create_table(u'core_orderdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Order'])),
            ('giver_material', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.GiverMaterial'])),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['OrderDetail'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'core_author')

        # Deleting model 'Material'
        db.delete_table(u'core_material')

        # Removing M2M table for field author on 'Material'
        db.delete_table(db.shorten_name(u'core_material_author'))

        # Deleting model 'GiverMaterial'
        db.delete_table(u'core_givermaterial')

        # Deleting model 'Order'
        db.delete_table(u'core_order')

        # Deleting model 'OrderDetail'
        db.delete_table(u'core_orderdetail')


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
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Author']", 'symmetrical': 'False'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'has_pic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pages': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pdf': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'publisher_book_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'})
        },
        u'core.order': {
            'Meta': {'object_name': 'Order'},
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'giver_orders'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'pay_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'payment_detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reader_orders'", 'to': u"orm['auth.User']"}),
            'ship_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'shipping_cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'})
        },
        u'core.orderdetail': {
            'Meta': {'object_name': 'OrderDetail'},
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'giver_material': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.GiverMaterial']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Order']"})
        }
    }

    complete_apps = ['core']