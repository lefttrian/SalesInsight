# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Abcdatadistr(models.Model):
    comid = models.IntegerField(db_column='COMID', primary_key=True)  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    akind = models.SmallIntegerField(db_column='AKIND')  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    coef = models.FloatField(db_column='COEF', blank=True, null=True)  # Field name made lowercase.
    contr = models.FloatField(db_column='CONTR', blank=True, null=True)  # Field name made lowercase.
    ftrspvalue = models.FloatField(db_column='FTRSPVALUE', blank=True, null=True)  # Field name made lowercase.
    ttrspvalue = models.FloatField(db_column='TTRSPVALUE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ABCDATADISTR'
        unique_together = (('comid', 'codeid', 'akind'),)


class Abcmodel(models.Model):
    comid = models.IntegerField(db_column='COMID', primary_key=True)  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=50)  # Field name made lowercase.
    autoanalisys = models.SmallIntegerField(db_column='AUTOANALISYS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ABCMODEL'
        unique_together = (('comid', 'codeid'),)


class Abcmodellines(models.Model):
    comid = models.ForeignKey(Abcmodel, models.DO_NOTHING, db_column='COMID', primary_key=True)  # Field name made lowercase.
    abmid = models.ForeignKey(Abcmodel, models.DO_NOTHING, db_column='ABMID')  # Field name made lowercase.
    linenum = models.IntegerField(db_column='LINENUM')  # Field name made lowercase.
    distrno = models.IntegerField(db_column='DISTRNO')  # Field name made lowercase.
    abcid1 = models.IntegerField(db_column='ABCID1')  # Field name made lowercase.
    abcid2 = models.IntegerField(db_column='ABCID2')  # Field name made lowercase.
    abcid3 = models.IntegerField(db_column='ABCID3')  # Field name made lowercase.
    abcid4 = models.IntegerField(db_column='ABCID4')  # Field name made lowercase.
    abcid5 = models.IntegerField(db_column='ABCID5')  # Field name made lowercase.
    coef = models.FloatField(db_column='COEF')  # Field name made lowercase.
    accid = models.IntegerField(db_column='ACCID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ABCMODELLINES'
        unique_together = (('comid', 'abmid', 'linenum'),)


class Abcparams(models.Model):
    comid = models.ForeignKey('Company', models.DO_NOTHING, db_column='COMID', primary_key=True)  # Field name made lowercase.
    dimstr1 = models.CharField(db_column='DIMSTR1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    dimstr2 = models.CharField(db_column='DIMSTR2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    dimstr3 = models.CharField(db_column='DIMSTR3', max_length=25, blank=True, null=True)  # Field name made lowercase.
    dimstr4 = models.CharField(db_column='DIMSTR4', max_length=25, blank=True, null=True)  # Field name made lowercase.
    dimstr5 = models.CharField(db_column='DIMSTR5', max_length=25, blank=True, null=True)  # Field name made lowercase.
    distrstr1 = models.CharField(db_column='DISTRSTR1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    distrstr2 = models.CharField(db_column='DISTRSTR2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    distrstr3 = models.CharField(db_column='DISTRSTR3', max_length=25, blank=True, null=True)  # Field name made lowercase.
    distrdims1 = models.IntegerField(db_column='DISTRDIMS1', blank=True, null=True)  # Field name made lowercase.
    distrdims2 = models.IntegerField(db_column='DISTRDIMS2', blank=True, null=True)  # Field name made lowercase.
    distrdims3 = models.IntegerField(db_column='DISTRDIMS3', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ABCPARAMS'


class Abctrans(models.Model):
    ftrid = models.IntegerField(db_column='FTRID', primary_key=True)  # Field name made lowercase.
    stlid = models.IntegerField(db_column='STLID')  # Field name made lowercase.
    linenum = models.IntegerField(db_column='LINENUM')  # Field name made lowercase.
    comid = models.IntegerField(db_column='COMID')  # Field name made lowercase.
    fyeid = models.IntegerField(db_column='FYEID')  # Field name made lowercase.
    fipid = models.IntegerField(db_column='FIPID')  # Field name made lowercase.
    distrno = models.IntegerField(db_column='DISTRNO')  # Field name made lowercase.
    abcid1 = models.IntegerField(db_column='ABCID1')  # Field name made lowercase.
    abcid2 = models.IntegerField(db_column='ABCID2')  # Field name made lowercase.
    abcid3 = models.IntegerField(db_column='ABCID3')  # Field name made lowercase.
    abcid4 = models.IntegerField(db_column='ABCID4')  # Field name made lowercase.
    abcid5 = models.IntegerField(db_column='ABCID5')  # Field name made lowercase.
    coef = models.FloatField(db_column='COEF')  # Field name made lowercase.
    lamount = models.FloatField(db_column='LAMOUNT')  # Field name made lowercase.
    accid = models.IntegerField(db_column='ACCID', blank=True, null=True)  # Field name made lowercase.
    inputstatus = models.SmallIntegerField(db_column='INPUTSTATUS')  # Field name made lowercase.
    trndate = models.DateTimeField(db_column='TRNDATE', blank=True, null=True)  # Field name made lowercase.
    source = models.SmallIntegerField(db_column='SOURCE', blank=True, null=True)  # Field name made lowercase.
    aceid = models.IntegerField(db_column='ACEID')  # Field name made lowercase.
    atrid = models.IntegerField(db_column='ATRID')  # Field name made lowercase.
    rootatrid = models.IntegerField(db_column='ROOTATRID')  # Field name made lowercase.
    pprid = models.IntegerField(db_column='PPRID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ABCTRANS'
        unique_together = (('ftrid', 'stlid', 'linenum', 'aceid', 'atrid'),)


class Accbalsheet(models.Model):
    comid = models.IntegerField(db_column='COMID')  # Field name made lowercase.
    masterid = models.ForeignKey('Account', models.DO_NOTHING, db_column='MASTERID', primary_key=True)  # Field name made lowercase.
    fyeid = models.IntegerField(db_column='FYEID')  # Field name made lowercase.
    fipid = models.IntegerField(db_column='FIPID')  # Field name made lowercase.
    lperiodcredit = models.FloatField(db_column='LPERIODCREDIT', blank=True, null=True)  # Field name made lowercase.
    lperioddebit = models.FloatField(db_column='LPERIODDEBIT', blank=True, null=True)  # Field name made lowercase.
    speriodcredit = models.FloatField(db_column='SPERIODCREDIT', blank=True, null=True)  # Field name made lowercase.
    sperioddebit = models.FloatField(db_column='SPERIODDEBIT', blank=True, null=True)  # Field name made lowercase.
    lperiodcreditupd = models.FloatField(db_column='LPERIODCREDITUPD', blank=True, null=True)  # Field name made lowercase.
    lperioddebitupd = models.FloatField(db_column='LPERIODDEBITUPD', blank=True, null=True)  # Field name made lowercase.
    speriodcreditupd = models.FloatField(db_column='SPERIODCREDITUPD', blank=True, null=True)  # Field name made lowercase.
    sperioddebitupd = models.FloatField(db_column='SPERIODDEBITUPD', blank=True, null=True)  # Field name made lowercase.
    kepyocount = models.FloatField(db_column='KEPYOCOUNT', blank=True, null=True)  # Field name made lowercase.
    kepyocountupd = models.FloatField(db_column='KEPYOCOUNTUPD', blank=True, null=True)  # Field name made lowercase.
    lkepyodebit = models.FloatField(db_column='LKEPYODEBIT', blank=True, null=True)  # Field name made lowercase.
    lkepyocredit = models.FloatField(db_column='LKEPYOCREDIT', blank=True, null=True)  # Field name made lowercase.
    skepyodebit = models.FloatField(db_column='SKEPYODEBIT', blank=True, null=True)  # Field name made lowercase.
    skepyocredit = models.FloatField(db_column='SKEPYOCREDIT', blank=True, null=True)  # Field name made lowercase.
    lkepyodebitupd = models.FloatField(db_column='LKEPYODEBITUPD', blank=True, null=True)  # Field name made lowercase.
    lkepyocreditupd = models.FloatField(db_column='LKEPYOCREDITUPD', blank=True, null=True)  # Field name made lowercase.
    skepyodebitupd = models.FloatField(db_column='SKEPYODEBITUPD', blank=True, null=True)  # Field name made lowercase.
    skepyocreditupd = models.FloatField(db_column='SKEPYOCREDITUPD', blank=True, null=True)  # Field name made lowercase.
    tdlperioddebit = models.FloatField(db_column='TDLPERIODDEBIT', blank=True, null=True)  # Field name made lowercase.
    tdlperiodcredit = models.FloatField(db_column='TDLPERIODCREDIT', blank=True, null=True)  # Field name made lowercase.
    tdsperioddebit = models.FloatField(db_column='TDSPERIODDEBIT', blank=True, null=True)  # Field name made lowercase.
    tdsperiodcredit = models.FloatField(db_column='TDSPERIODCREDIT', blank=True, null=True)  # Field name made lowercase.
    tdlperioddebitupd = models.FloatField(db_column='TDLPERIODDEBITUPD', blank=True, null=True)  # Field name made lowercase.
    tdlperiodcreditupd = models.FloatField(db_column='TDLPERIODCREDITUPD', blank=True, null=True)  # Field name made lowercase.
    tdsperioddebitupd = models.FloatField(db_column='TDSPERIODDEBITUPD', blank=True, null=True)  # Field name made lowercase.
    tdsperiodcreditupd = models.FloatField(db_column='TDSPERIODCREDITUPD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCBALSHEET'
        unique_together = (('masterid', 'fyeid', 'fipid'),)


class Accclosetemplate(models.Model):
    comid = models.ForeignKey('Acceventtype', models.DO_NOTHING, db_column='COMID', primary_key=True)  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dsrid = models.IntegerField(db_column='DSRID', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', unique=True)  # Field name made lowercase.
    justification = models.CharField(db_column='JUSTIFICATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aetid = models.ForeignKey('Acceventtype', models.DO_NOTHING, db_column='AETID')  # Field name made lowercase.
    istd = models.SmallIntegerField(db_column='ISTD')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCCLOSETEMPLATE'
        unique_together = (('comid', 'comid', 'codeid'),)


class Accclosetemplatelines(models.Model):
    comid = models.IntegerField(db_column='COMID')  # Field name made lowercase.
    aecid = models.IntegerField(db_column='AECID')  # Field name made lowercase.
    linenum = models.IntegerField(db_column='LINENUM')  # Field name made lowercase.
    linkid = models.ForeignKey(Accclosetemplate, models.DO_NOTHING, db_column='LINKID')  # Field name made lowercase.
    accfrom = models.CharField(db_column='ACCFROM', max_length=255)  # Field name made lowercase.
    accto = models.CharField(db_column='ACCTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accdebit = models.IntegerField(db_column='ACCDEBIT', blank=True, null=True)  # Field name made lowercase.
    acccredit = models.IntegerField(db_column='ACCCREDIT', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCCLOSETEMPLATELINES'


class Accdiffmodel(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', unique=True, max_length=25)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=100)  # Field name made lowercase.
    diffgroup = models.IntegerField(db_column='DIFFGROUP', blank=True, null=True)  # Field name made lowercase.
    employeenum = models.IntegerField(db_column='EMPLOYEENUM', blank=True, null=True)  # Field name made lowercase.
    mobilenum = models.IntegerField(db_column='MOBILENUM', blank=True, null=True)  # Field name made lowercase.
    akind = models.SmallIntegerField(db_column='AKIND')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCDIFFMODEL'


class Accdiffmodellines(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    accdiffmodelid = models.ForeignKey(Accdiffmodel, models.DO_NOTHING, db_column='ACCDIFFMODELID')  # Field name made lowercase.
    fromdate = models.DateTimeField(db_column='FROMDATE')  # Field name made lowercase.
    coef = models.FloatField(db_column='COEF')  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCDIFFMODELLINES'


class Acceventimport(models.Model):
    articlenum = models.IntegerField(db_column='ARTICLENUM', blank=True, null=True)  # Field name made lowercase.
    glcode = models.CharField(db_column='GLCODE', max_length=25)  # Field name made lowercase.
    dsrid = models.IntegerField(db_column='DSRID', blank=True, null=True)  # Field name made lowercase.
    justification = models.CharField(db_column='JUSTIFICATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tradecode = models.CharField(db_column='TRADECODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    transdate = models.DateTimeField(db_column='TRANSDATE')  # Field name made lowercase.
    trnvalue = models.FloatField(db_column='TRNVALUE')  # Field name made lowercase.
    iscredit = models.SmallIntegerField(db_column='ISCREDIT')  # Field name made lowercase.
    batchid = models.IntegerField(db_column='BATCHID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCEVENTIMPORT'


class Acceventtype(models.Model):
    comid = models.ForeignKey('Journal', models.DO_NOTHING, db_column='COMID', primary_key=True)  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    jouid = models.ForeignKey('Journal', models.DO_NOTHING, db_column='JOUID')  # Field name made lowercase.
    primaryaccount = models.ForeignKey('Account', models.DO_NOTHING, db_column='PRIMARYACCOUNT', blank=True, null=True)  # Field name made lowercase.
    atype = models.SmallIntegerField(db_column='ATYPE')  # Field name made lowercase.
    needauthority = models.SmallIntegerField(db_column='NEEDAUTHORITY')  # Field name made lowercase.
    justification = models.CharField(db_column='JUSTIFICATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    updkepyobalancesheet = models.SmallIntegerField(db_column='UPDKEPYOBALANCESHEET')  # Field name made lowercase.
    iscancelling = models.SmallIntegerField(db_column='ISCANCELLING')  # Field name made lowercase.
    isanal = models.SmallIntegerField(db_column='ISANAL')  # Field name made lowercase.
    daysrange = models.SmallIntegerField(db_column='DAYSRANGE', blank=True, null=True)  # Field name made lowercase.
    dlaid = models.IntegerField(db_column='DLAID', blank=True, null=True)  # Field name made lowercase.
    abcmode = models.SmallIntegerField(db_column='ABCMODE')  # Field name made lowercase.
    abcmodel = models.IntegerField(db_column='ABCMODEL', blank=True, null=True)  # Field name made lowercase.
    abcanal = models.SmallIntegerField(db_column='ABCANAL')  # Field name made lowercase.
    noupdkepyo = models.SmallIntegerField(db_column='NOUPDKEPYO')  # Field name made lowercase.
    noupdmyf = models.SmallIntegerField(db_column='NOUPDMYF')  # Field name made lowercase.
    zerovaluemode = models.SmallIntegerField(db_column='ZEROVALUEMODE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCEVENTTYPE'
        unique_together = (('comid', 'comid', 'codeid'),)


class Accevtemplate(models.Model):
    comid = models.ForeignKey(Acceventtype, models.DO_NOTHING, db_column='COMID', primary_key=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', unique=True)  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aetid = models.ForeignKey(Acceventtype, models.DO_NOTHING, db_column='AETID')  # Field name made lowercase.
    dsrid = models.IntegerField(db_column='DSRID', blank=True, null=True)  # Field name made lowercase.
    justification = models.CharField(db_column='JUSTIFICATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    periodicity = models.SmallIntegerField(db_column='PERIODICITY')  # Field name made lowercase.
    repeatondays = models.CharField(db_column='REPEATONDAYS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fastentry = models.SmallIntegerField(db_column='FASTENTRY', blank=True, null=True)  # Field name made lowercase.
    fastentrydata = models.TextField(db_column='FASTENTRYDATA', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    braid = models.IntegerField(db_column='BRAID', blank=True, null=True)  # Field name made lowercase.
    isactive = models.SmallIntegerField(db_column='ISACTIVE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCEVTEMPLATE'
        unique_together = (('comid', 'comid', 'codeid'),)


class Accevtemplines(models.Model):
    comid = models.IntegerField(db_column='COMID')  # Field name made lowercase.
    aepid = models.IntegerField(db_column='AEPID')  # Field name made lowercase.
    linenum = models.IntegerField(db_column='LINENUM')  # Field name made lowercase.
    accountmask = models.CharField(db_column='ACCOUNTMASK', max_length=25)  # Field name made lowercase.
    calcformula = models.CharField(db_column='CALCFORMULA', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cord = models.SmallIntegerField(db_column='CORD')  # Field name made lowercase.
    linkid = models.ForeignKey(Accevtemplate, models.DO_NOTHING, db_column='LINKID')  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    justification = models.CharField(db_column='JUSTIFICATION', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCEVTEMPLINES'


class Account(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    comid = models.ForeignKey('Isologcategory', models.DO_NOTHING, db_column='COMID')  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=25)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=255)  # Field name made lowercase.
    foreignaccount = models.CharField(db_column='FOREIGNACCOUNT', max_length=25, blank=True, null=True)  # Field name made lowercase.
    foreigndescr = models.CharField(db_column='FOREIGNDESCR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idprimary = models.ForeignKey('self', models.DO_NOTHING, db_column='IDPRIMARY', blank=True, null=True)  # Field name made lowercase.
    grade = models.SmallIntegerField(db_column='GRADE')  # Field name made lowercase.
    idcouple = models.ForeignKey('self', models.DO_NOTHING, db_column='IDCOUPLE', blank=True, null=True)  # Field name made lowercase.
    adsid = models.ForeignKey('Analdist', models.DO_NOTHING, db_column='ADSID', blank=True, null=True)  # Field name made lowercase.
    atype = models.SmallIntegerField(db_column='ATYPE')  # Field name made lowercase.
    uatid = models.ForeignKey('Useracctype', models.DO_NOTHING, db_column='UATID', blank=True, null=True)  # Field name made lowercase.
    behaviour = models.SmallIntegerField(db_column='BEHAVIOUR')  # Field name made lowercase.
    vtcid = models.ForeignKey('Vatcategory', models.DO_NOTHING, db_column='VTCID', blank=True, null=True)  # Field name made lowercase.
    vatid = models.ForeignKey('self', models.DO_NOTHING, db_column='VATID', blank=True, null=True)  # Field name made lowercase.
    minbalance = models.FloatField(db_column='MINBALANCE', blank=True, null=True)  # Field name made lowercase.
    maxbalance = models.FloatField(db_column='MAXBALANCE', blank=True, null=True)  # Field name made lowercase.
    isolog = models.ForeignKey('Isologcategory', models.DO_NOTHING, db_column='ISOLOG', blank=True, null=True)  # Field name made lowercase.
    ismoving = models.SmallIntegerField(db_column='ISMOVING')  # Field name made lowercase.
    balancetransfer = models.SmallIntegerField(db_column='BALANCETRANSFER')  # Field name made lowercase.
    vdcid = models.IntegerField(db_column='VDCID', blank=True, null=True)  # Field name made lowercase.
    vatdocmode = models.SmallIntegerField(db_column='VATDOCMODE', blank=True, null=True)  # Field name made lowercase.
    remarks = models.TextField(db_column='REMARKS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    isactive = models.SmallIntegerField(db_column='ISACTIVE', blank=True, null=True)  # Field name made lowercase.
    insynthetic = models.SmallIntegerField(db_column='INSYNTHETIC', blank=True, null=True)  # Field name made lowercase.
    uagid = models.ForeignKey('Useraccgroup', models.DO_NOTHING, db_column='UAGID', blank=True, null=True)  # Field name made lowercase.
    almode = models.SmallIntegerField(db_column='ALMODE')  # Field name made lowercase.
    fldstring1 = models.CharField(db_column='FLDSTRING1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fldstring2 = models.CharField(db_column='FLDSTRING2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fldstring3 = models.CharField(db_column='FLDSTRING3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fldstring4 = models.CharField(db_column='FLDSTRING4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fldstring5 = models.CharField(db_column='FLDSTRING5', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fldstring6 = models.CharField(db_column='FLDSTRING6', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flddate1 = models.DateTimeField(db_column='FLDDATE1', blank=True, null=True)  # Field name made lowercase.
    flddate2 = models.DateTimeField(db_column='FLDDATE2', blank=True, null=True)  # Field name made lowercase.
    flddate3 = models.DateTimeField(db_column='FLDDATE3', blank=True, null=True)  # Field name made lowercase.
    fldfloat1 = models.FloatField(db_column='FLDFLOAT1', blank=True, null=True)  # Field name made lowercase.
    fldfloat2 = models.FloatField(db_column='FLDFLOAT2', blank=True, null=True)  # Field name made lowercase.
    fldfloat3 = models.FloatField(db_column='FLDFLOAT3', blank=True, null=True)  # Field name made lowercase.
    fldfloat4 = models.FloatField(db_column='FLDFLOAT4', blank=True, null=True)  # Field name made lowercase.
    fldfloat5 = models.FloatField(db_column='FLDFLOAT5', blank=True, null=True)  # Field name made lowercase.
    fldfloat6 = models.FloatField(db_column='FLDFLOAT6', blank=True, null=True)  # Field name made lowercase.
    fltid1 = models.IntegerField(db_column='FLTID1', blank=True, null=True)  # Field name made lowercase.
    fltid2 = models.IntegerField(db_column='FLTID2', blank=True, null=True)  # Field name made lowercase.
    fltid3 = models.IntegerField(db_column='FLTID3', blank=True, null=True)  # Field name made lowercase.
    lgtaxcategoryid = models.ForeignKey('Lgtaxcategory', models.DO_NOTHING, db_column='LGTAXCATEGORYID', blank=True, null=True)  # Field name made lowercase.
    vatupdmode = models.SmallIntegerField(db_column='VATUPDMODE', blank=True, null=True)  # Field name made lowercase.
    warning = models.CharField(db_column='WARNING', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isvatwholesale = models.SmallIntegerField(db_column='ISVATWHOLESALE', blank=True, null=True)  # Field name made lowercase.
    accdiffmodelid = models.IntegerField(db_column='ACCDIFFMODELID', blank=True, null=True)  # Field name made lowercase.
    cfyeid = models.IntegerField(db_column='CFYEID', blank=True, null=True)  # Field name made lowercase.
    fromaccount = models.CharField(db_column='FROMACCOUNT', max_length=25, blank=True, null=True)  # Field name made lowercase.
    taxdisputes = models.IntegerField(db_column='TAXDISPUTES', blank=True, null=True)  # Field name made lowercase.
    inventoryrest = models.IntegerField(db_column='INVENTORYREST', blank=True, null=True)  # Field name made lowercase.
    taxkind = models.IntegerField(db_column='TAXKIND', blank=True, null=True)  # Field name made lowercase.
    kadfin_categoryid = models.ForeignKey('KadfinCategory', models.DO_NOTHING, db_column='KADFIN_CATEGORYID', blank=True, null=True)  # Field name made lowercase.
    kadact_categoryid = models.ForeignKey('KadactivityCategory', models.DO_NOTHING, db_column='KADACT_CATEGORYID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCOUNT'
        unique_together = (('comid', 'comid', 'comid', 'comid', 'code'),)


class Accountevent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    aceid = models.IntegerField(db_column='ACEID', blank=True, null=True)  # Field name made lowercase.
    aetid = models.ForeignKey(Acceventtype, models.DO_NOTHING, db_column='AETID')  # Field name made lowercase.
    approvaldate = models.DateTimeField(db_column='APPROVALDATE', blank=True, null=True)  # Field name made lowercase.
    approvaluser = models.IntegerField(db_column='APPROVALUSER', blank=True, null=True)  # Field name made lowercase.
    approved = models.SmallIntegerField(db_column='APPROVED')  # Field name made lowercase.
    atrid = models.IntegerField(db_column='ATRID', blank=True, null=True)  # Field name made lowercase.
    braid = models.ForeignKey('Branch', models.DO_NOTHING, db_column='BRAID')  # Field name made lowercase.
    comid = models.ForeignKey(Acceventtype, models.DO_NOTHING, db_column='COMID')  # Field name made lowercase.
    curid = models.ForeignKey('Currency', models.DO_NOTHING, db_column='CURID')  # Field name made lowercase.
    dsrid = models.IntegerField(db_column='DSRID')  # Field name made lowercase.
    fipid = models.IntegerField(db_column='FIPID')  # Field name made lowercase.
    fyeid = models.IntegerField(db_column='FYEID')  # Field name made lowercase.
    isbalanced = models.SmallIntegerField(db_column='ISBALANCED')  # Field name made lowercase.
    iscancelled = models.SmallIntegerField(db_column='ISCANCELLED')  # Field name made lowercase.
    isprinted = models.SmallIntegerField(db_column='ISPRINTED')  # Field name made lowercase.
    jouid = models.ForeignKey('Journal', models.DO_NOTHING, db_column='JOUID')  # Field name made lowercase.
    journalnum = models.IntegerField(db_column='JOURNALNUM')  # Field name made lowercase.
    updcount = models.IntegerField(db_column='UPDCOUNT', blank=True, null=True)  # Field name made lowercase.
    justification = models.CharField(db_column='JUSTIFICATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    localrate = models.FloatField(db_column='LOCALRATE', blank=True, null=True)  # Field name made lowercase.
    dsrnumber = models.IntegerField(db_column='DSRNUMBER')  # Field name made lowercase.
    source = models.SmallIntegerField(db_column='SOURCE')  # Field name made lowercase.
    tradecode = models.CharField(db_column='TRADECODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    transdate = models.DateTimeField(db_column='TRANSDATE')  # Field name made lowercase.
    atype = models.SmallIntegerField(db_column='ATYPE')  # Field name made lowercase.
    rootatrid = models.IntegerField(db_column='ROOTATRID', blank=True, null=True)  # Field name made lowercase.
    secondaryrate = models.FloatField(db_column='SECONDARYRATE', blank=True, null=True)  # Field name made lowercase.
    anallevel = models.SmallIntegerField(db_column='ANALLEVEL', blank=True, null=True)  # Field name made lowercase.
    ftrid = models.IntegerField(db_column='FTRID', blank=True, null=True)  # Field name made lowercase.
    aepid = models.IntegerField(db_column='AEPID', blank=True, null=True)  # Field name made lowercase.
    entrydata = models.BinaryField(db_column='ENTRYDATA', blank=True, null=True)  # Field name made lowercase.
    batchid = models.IntegerField(db_column='BATCHID', blank=True, null=True)  # Field name made lowercase.
    cfoid = models.IntegerField(db_column='CFOID', blank=True, null=True)  # Field name made lowercase.
    relaceid = models.IntegerField(db_column='RELACEID', blank=True, null=True)  # Field name made lowercase.
    reltype = models.SmallIntegerField(db_column='RELTYPE', blank=True, null=True)  # Field name made lowercase.
    adsid = models.IntegerField(db_column='ADSID', blank=True, null=True)  # Field name made lowercase.
    analdistcode = models.CharField(db_column='ANALDISTCODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    traderaccid = models.IntegerField(db_column='TRADERACCID', blank=True, null=True)  # Field name made lowercase.
    batchdeprid = models.IntegerField(db_column='BATCHDEPRID', blank=True, null=True)  # Field name made lowercase.
    rootaceline = models.IntegerField(db_column='ROOTACELINE', blank=True, null=True)  # Field name made lowercase.
    svftrid = models.IntegerField(db_column='SVFTRID', blank=True, null=True)  # Field name made lowercase.
    coraceid = models.IntegerField(db_column='CORACEID', blank=True, null=True)  # Field name made lowercase.
    corotheraceid = models.IntegerField(db_column='COROTHERACEID', blank=True, null=True)  # Field name made lowercase.
    cororiginaceid = models.IntegerField(db_column='CORORIGINACEID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCOUNTEVENT'
        unique_together = (('comid', 'comid', 'comid', 'fyeid', 'dsrid', 'dsrnumber'),)


class Accountext(models.Model):
    comid = models.IntegerField(db_column='COMID')  # Field name made lowercase.
    accid = models.ForeignKey(Account, models.DO_NOTHING, db_column='ACCID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=80, blank=True, null=True)  # Field name made lowercase.
    jobdescr = models.CharField(db_column='JOBDESCR', max_length=80, blank=True, null=True)  # Field name made lowercase.
    doyid = models.IntegerField(db_column='DOYID', blank=True, null=True)  # Field name made lowercase.
    afm = models.CharField(db_column='AFM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cntid = models.IntegerField(db_column='CNTID', blank=True, null=True)  # Field name made lowercase.
    street = models.CharField(db_column='STREET', max_length=50, blank=True, null=True)  # Field name made lowercase.
    geoid = models.IntegerField(db_column='GEOID', blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='DISTRICT', max_length=25, blank=True, null=True)  # Field name made lowercase.
    faxnumber = models.CharField(db_column='FAXNUMBER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='PHONE1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='PHONE2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    telex = models.CharField(db_column='TELEX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='MANAGER', max_length=80, blank=True, null=True)  # Field name made lowercase.
    sumkepyo = models.SmallIntegerField(db_column='SUMKEPYO', blank=True, null=True)  # Field name made lowercase.
    refacccode = models.CharField(db_column='REFACCCODE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    refaccdescr = models.CharField(db_column='REFACCDESCR', max_length=80, blank=True, null=True)  # Field name made lowercase.
    updkepyo = models.SmallIntegerField(db_column='UPDKEPYO', blank=True, null=True)  # Field name made lowercase.
    atype = models.SmallIntegerField(db_column='ATYPE', blank=True, null=True)  # Field name made lowercase.
    myfnotobject = models.SmallIntegerField(db_column='MYFNOTOBJECT')  # Field name made lowercase.
    myfacctype = models.SmallIntegerField(db_column='MYFACCTYPE', blank=True, null=True)  # Field name made lowercase.
    closingdate = models.DateTimeField(db_column='CLOSINGDATE', blank=True, null=True)  # Field name made lowercase.
    fathername = models.CharField(db_column='FATHERNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isgdpr = models.SmallIntegerField(db_column='ISGDPR')  # Field name made lowercase.
    consentdate = models.DateTimeField(db_column='CONSENTDATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCOUNTEXT'


class Acctrn(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    aetid = models.IntegerField(db_column='AETID')  # Field name made lowercase.
    atrid = models.IntegerField(db_column='ATRID', blank=True, null=True)  # Field name made lowercase.
    rootatrid = models.IntegerField(db_column='ROOTATRID', blank=True, null=True)  # Field name made lowercase.
    aceid = models.ForeignKey(Accountevent, models.DO_NOTHING, db_column='ACEID')  # Field name made lowercase.
    atype = models.SmallIntegerField(db_column='ATYPE')  # Field name made lowercase.
    jouid = models.IntegerField(db_column='JOUID')  # Field name made lowercase.
    journalnum = models.IntegerField(db_column='JOURNALNUM')  # Field name made lowercase.
    transdate = models.DateTimeField(db_column='TRANSDATE')  # Field name made lowercase.
    approved = models.SmallIntegerField(db_column='APPROVED')  # Field name made lowercase.
    tradecode = models.CharField(db_column='TRADECODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    justification = models.CharField(db_column='JUSTIFICATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    linenum = models.IntegerField(db_column='LINENUM')  # Field name made lowercase.
    curid = models.IntegerField(db_column='CURID')  # Field name made lowercase.
    accid = models.ForeignKey(Account, models.DO_NOTHING, db_column='ACCID')  # Field name made lowercase.
    trnvalue = models.FloatField(db_column='TRNVALUE')  # Field name made lowercase.
    localvalue = models.FloatField(db_column='LOCALVALUE')  # Field name made lowercase.
    secondaryvalue = models.FloatField(db_column='SECONDARYVALUE', blank=True, null=True)  # Field name made lowercase.
    doccode = models.CharField(db_column='DOCCODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    comid = models.IntegerField(db_column='COMID')  # Field name made lowercase.
    braid = models.IntegerField(db_column='BRAID')  # Field name made lowercase.
    fyeid = models.IntegerField(db_column='FYEID')  # Field name made lowercase.
    fipid = models.IntegerField(db_column='FIPID')  # Field name made lowercase.
    isdebit = models.SmallIntegerField(db_column='ISDEBIT', blank=True, null=True)  # Field name made lowercase.
    iscredit = models.SmallIntegerField(db_column='ISCREDIT', blank=True, null=True)  # Field name made lowercase.
    isopening = models.SmallIntegerField(db_column='ISOPENING', blank=True, null=True)  # Field name made lowercase.
    isclosing = models.SmallIntegerField(db_column='ISCLOSING', blank=True, null=True)  # Field name made lowercase.
    isflag5 = models.SmallIntegerField(db_column='ISFLAG5', blank=True, null=True)  # Field name made lowercase.
    isflag6 = models.SmallIntegerField(db_column='ISFLAG6', blank=True, null=True)  # Field name made lowercase.
    isflag7 = models.SmallIntegerField(db_column='ISFLAG7', blank=True, null=True)  # Field name made lowercase.
    isflag8 = models.SmallIntegerField(db_column='ISFLAG8', blank=True, null=True)  # Field name made lowercase.
    isflag9 = models.SmallIntegerField(db_column='ISFLAG9', blank=True, null=True)  # Field name made lowercase.
    isflag10 = models.SmallIntegerField(db_column='ISFLAG10', blank=True, null=True)  # Field name made lowercase.
    isflag11 = models.SmallIntegerField(db_column='ISFLAG11', blank=True, null=True)  # Field name made lowercase.
    isflag12 = models.SmallIntegerField(db_column='ISFLAG12', blank=True, null=True)  # Field name made lowercase.
    isflag13 = models.SmallIntegerField(db_column='ISFLAG13', blank=True, null=True)  # Field name made lowercase.
    isflag14 = models.SmallIntegerField(db_column='ISFLAG14', blank=True, null=True)  # Field name made lowercase.
    isflag15 = models.SmallIntegerField(db_column='ISFLAG15', blank=True, null=True)  # Field name made lowercase.
    isflag16 = models.SmallIntegerField(db_column='ISFLAG16', blank=True, null=True)  # Field name made lowercase.
    isflag17 = models.SmallIntegerField(db_column='ISFLAG17', blank=True, null=True)  # Field name made lowercase.
    isflag18 = models.SmallIntegerField(db_column='ISFLAG18', blank=True, null=True)  # Field name made lowercase.
    isflag19 = models.SmallIntegerField(db_column='ISFLAG19', blank=True, null=True)  # Field name made lowercase.
    isflag20 = models.SmallIntegerField(db_column='ISFLAG20', blank=True, null=True)  # Field name made lowercase.
    analperc = models.FloatField(db_column='ANALPERC', blank=True, null=True)  # Field name made lowercase.
    ftrid = models.IntegerField(db_column='FTRID', blank=True, null=True)  # Field name made lowercase.
    source = models.SmallIntegerField(db_column='SOURCE', blank=True, null=True)  # Field name made lowercase.
    adsid = models.CharField(db_column='ADSID', max_length=25, blank=True, null=True)  # Field name made lowercase.
    kepyocount = models.FloatField(db_column='KEPYOCOUNT', blank=True, null=True)  # Field name made lowercase.
    kepyovalue = models.FloatField(db_column='KEPYOVALUE', blank=True, null=True)  # Field name made lowercase.
    lkepyovalue = models.FloatField(db_column='LKEPYOVALUE', blank=True, null=True)  # Field name made lowercase.
    skepyovalue = models.FloatField(db_column='SKEPYOVALUE', blank=True, null=True)  # Field name made lowercase.
    dateendcheck = models.DateTimeField(db_column='DATEENDCHECK', blank=True, null=True)  # Field name made lowercase.
    updatekepyo = models.SmallIntegerField(db_column='UPDATEKEPYO', blank=True, null=True)  # Field name made lowercase.
    accdifmodelid = models.IntegerField(db_column='ACCDIFMODELID', blank=True, null=True)  # Field name made lowercase.
    difatrid = models.IntegerField(db_column='DIFATRID', blank=True, null=True)  # Field name made lowercase.
    myfcount = models.FloatField(db_column='MYFCOUNT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACCTRN'


class Acqways(models.Model):
    comid = models.IntegerField(db_column='COMID', primary_key=True)  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACQWAYS'
        unique_together = (('comid', 'codeid'),)


class Actbasecost(models.Model):
    comid = models.IntegerField(db_column='COMID', primary_key=True)  # Field name made lowercase.
    domaintype = models.SmallIntegerField(db_column='DOMAINTYPE')  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    strorder = models.CharField(db_column='STRORDER', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shortdescr = models.CharField(db_column='SHORTDESCR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isactive = models.SmallIntegerField(db_column='ISACTIVE')  # Field name made lowercase.
    ismoving = models.SmallIntegerField(db_column='ISMOVING', blank=True, null=True)  # Field name made lowercase.
    accmask = models.CharField(db_column='ACCMASK', max_length=25, blank=True, null=True)  # Field name made lowercase.
    distr1 = models.SmallIntegerField(db_column='DISTR1', blank=True, null=True)  # Field name made lowercase.
    distr2 = models.SmallIntegerField(db_column='DISTR2', blank=True, null=True)  # Field name made lowercase.
    distr3 = models.SmallIntegerField(db_column='DISTR3', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ACTBASECOST'
        unique_together = (('comid', 'domaintype', 'codeid'),)


class Agecategory(models.Model):
    comid = models.IntegerField(db_column='COMID', primary_key=True)  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AGECATEGORY'
        unique_together = (('comid', 'codeid'),)


class Analdist(models.Model):
    comid = models.ForeignKey(Acceventtype, models.DO_NOTHING, db_column='COMID')  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=25)  # Field name made lowercase.
    aetid = models.ForeignKey(Acceventtype, models.DO_NOTHING, db_column='AETID')  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    justification = models.CharField(db_column='JUSTIFICATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    atype = models.SmallIntegerField(db_column='ATYPE')  # Field name made lowercase.
    dsrid = models.IntegerField(db_column='DSRID', blank=True, null=True)  # Field name made lowercase.
    dmode = models.SmallIntegerField(db_column='DMODE')  # Field name made lowercase.
    dlpdsrid = models.IntegerField(db_column='DLPDSRID', blank=True, null=True)  # Field name made lowercase.
    isactive = models.SmallIntegerField(db_column='ISACTIVE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ANALDIST'
        unique_together = (('comid', 'comid', 'code'),)


class Analdistlines(models.Model):
    comid = models.IntegerField(db_column='COMID', primary_key=True)  # Field name made lowercase.
    adsid = models.ForeignKey(Analdist, models.DO_NOTHING, db_column='ADSID')  # Field name made lowercase.
    linenum = models.IntegerField(db_column='LINENUM')  # Field name made lowercase.
    accid = models.IntegerField(db_column='ACCID')  # Field name made lowercase.
    percentage = models.FloatField(db_column='PERCENTAGE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ANALDISTLINES'
        unique_together = (('comid', 'adsid', 'linenum'),)


class Apdnewcodes(models.Model):
    kpkcode = models.CharField(db_column='KPKCODE', primary_key=True, max_length=25)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    occcodemode = models.SmallIntegerField(db_column='OCCCODEMODE')  # Field name made lowercase.
    occcodepstid = models.IntegerField(db_column='OCCCODEPSTID', blank=True, null=True)  # Field name made lowercase.
    occcode = models.CharField(db_column='OCCCODE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    occcodemulti = models.CharField(db_column='OCCCODEMULTI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ikacodesmulti = models.CharField(db_column='IKACODESMULTI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    hasanallines = models.SmallIntegerField(db_column='HASANALLINES')  # Field name made lowercase.
    kadcode = models.CharField(db_column='KADCODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    zeroinsdays = models.SmallIntegerField(db_column='ZEROINSDAYS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'APDNEWCODES'


class Application(models.Model):
    comid = models.ForeignKey('Company', models.DO_NOTHING, db_column='COMID', primary_key=True)  # Field name made lowercase.
    codeid = models.IntegerField(db_column='CODEID')  # Field name made lowercase.
    id = models.AutoField(db_column='ID', unique=True)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'APPLICATION'
        unique_together = (('comid', 'codeid'),)
