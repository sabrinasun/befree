# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'core_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('descr', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['Category'])

        # Adding model 'Group'
        db.create_table(u'core_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=50)),
            ('book_order_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('book_list_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('donation_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('website_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('is_nonprofit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('local_pickup', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('domestic_pay_shipping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('domestic_free_shipping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('international_free_shipping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shipping_other', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['Group'])

        # Adding model 'GroupMaterial'
        db.create_table(u'core_groupmaterial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Group'])),
            ('material', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Material'])),
            ('book_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('order_url', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['GroupMaterial'])

        # Deleting field 'Material.publisher'
        db.delete_column(u'core_material', 'publisher_id')

        # Adding field 'Material.editor_pick'
        db.add_column(u'core_material', 'editor_pick',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding M2M table for field publisher on 'Material'
        m2m_table_name = db.shorten_name(u'core_material_publisher')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('material', models.ForeignKey(orm[u'core.material'], null=False)),
            ('publisher', models.ForeignKey(orm[u'core.publisher'], null=False))
        ))
        db.create_unique(m2m_table_name, ['material_id', 'publisher_id'])

        # Adding M2M table for field category on 'Material'
        m2m_table_name = db.shorten_name(u'core_material_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('material', models.ForeignKey(orm[u'core.material'], null=False)),
            ('category', models.ForeignKey(orm[u'core.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['material_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'core_category')

        # Deleting model 'Group'
        db.delete_table(u'core_group')

        # Deleting model 'GroupMaterial'
        db.delete_table(u'core_groupmaterial')

        # Adding field 'Material.publisher'
        db.add_column(u'core_material', 'publisher',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['core.Publisher']),
                      keep_default=False)

        # Deleting field 'Material.editor_pick'
        db.delete_column(u'core_material', 'editor_pick')

        # Removing M2M table for field publisher on 'Material'
        db.delete_table(db.shorten_name(u'core_material_publisher'))

        # Removing M2M table for field category on 'Material'
        db.delete_table(db.shorten_name(u'core_material_category'))


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
            'donate_note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donate_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'core.category': {
            'Meta': {'object_name': 'Category'},
            'descr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'core.givermaterial': {
            'Meta': {'unique_together': "(('giver', 'material'),)", 'object_name': 'GiverMaterial'},
            'condition': ('django.db.models.fields.CharField', [], {'default': "'Good'", 'max_length': '10'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Material']"}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '10'})
        },
        u'core.group': {
            'Meta': {'object_name': 'Group'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'admin_id': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'book_list_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'book_order_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '50'}),
            'domestic_free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'domestic_pay_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'donation_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international_free_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_nonprofit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'local_pickup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_other': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'core.groupmaterial': {
            'Meta': {'object_name': 'GroupMaterial'},
            'book_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Material']"}),
            'order_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'core.material': {
            'Meta': {'object_name': 'Material'},
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Author']", 'symmetrical': 'False'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Category']", 'symmetrical': 'False'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor_pick': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pages': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'paperback': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pdf_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Publisher']", 'null': 'True', 'symmetrical': 'False'}),
            'publisher_book_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'core.order': {
            'Meta': {'object_name': 'Order'},
            'cancel_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'giver'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'pay_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'payment_detail': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reader'", 'to': u"orm['auth.User']"}),
            'ship_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NEW'", 'max_length': '10'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'})
        },
        u'core.orderdetail': {
            'Meta': {'object_name': 'OrderDetail'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.GiverMaterial']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Order']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'core.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donate_note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donate_url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'publish_free_book': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'core.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['core']