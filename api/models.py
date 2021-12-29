from django.db import models

# Create your models here.
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BmKolInfos(models.Model):
    id = models.BigAutoField(primary_key=True)
    kol_code = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    public_site = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    account_name = models.CharField(max_length=100, blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    account = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bm_kol_infos'


class BmPair(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    kol = models.ForeignKey(BmKolInfos, models.DO_NOTHING)
    product = models.ForeignKey('BmProducts', models.DO_NOTHING)
    is_active = models.IntegerField()
    share_percent = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bm_pair'


class BmProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_code = models.CharField(unique=True, max_length=45)
    categories = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    vendor = models.ForeignKey('BmVendorInfos', models.DO_NOTHING)
    image_path = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bm_products'

class BmRedirectRecords(models.Model):
    id = models.BigAutoField(primary_key=True)
    pair = models.ForeignKey(BmPair, models.DO_NOTHING)
    device = models.CharField(max_length=45, blank=True, null=True)
    device_id = models.CharField(max_length=100)
    locate_ip = models.CharField(max_length=45, blank=True, null=True)
    recorded_at = models.DateTimeField(blank=True, null=True)
    is_pc = models.IntegerField(blank=True, null=True)
    is_mobile = models.IntegerField(blank=True, null=True)
    device_family = models.CharField(max_length=100, blank=True, null=True)
    os_family = models.CharField(max_length=100, blank=True, null=True)
    browser_family = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bm_redirect_records'

class BmProductRecords(models.Model):
    id = models.BigAutoField(primary_key=True)
    pair_id = models.CharField(max_length=45)
    recorded_at = models.DateTimeField(blank=True, null=True)
    total_amount = models.IntegerField(blank=True, null=True)
    share_percentage = models.FloatField(blank=True, null=True)
    share_amount = models.IntegerField(blank=True, null=True)
    device_id = models.CharField(max_length=100, null=True)
    locate_ip = models.CharField(max_length=45, blank=True, null=True)
    is_pc = models.IntegerField(blank=True, null=True)
    is_mobile = models.IntegerField(blank=True, null=True)
    device_family = models.CharField(max_length=100, blank=True, null=True)
    os_family = models.CharField(max_length=100, blank=True, null=True)
    browser_family = models.CharField(max_length=100, blank=True, null=True)
    is_collect = models.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'bm_product_records'

class BmVendorInfos(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    note = models.TextField(blank=True, null=True)
    public_site = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bm_vendor_infos'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

