"""
Beschreibung: Definiert die Datenmodelle der App, welche die Struktur der Datenbanktabellen abbilden. Diese Modelle werden von Django ORM (Object-Relational Mapping) verwendet, um Datenbankoperationen zu abstrahieren.
Zweck: Repräsentiert die Datenstruktur der App und bietet eine hochgradig abstrahierte Schnittstelle zur Datenmanipulation.
"""

from django.db import models


# 2022 ############################################################################################


class GSL_grouped_ISK_2022(models.Model):
    STR_NR = models.IntegerField(primary_key=True)
    LAENGE = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    STR_KURZNAME = models.CharField(max_length=255)
    STR_KM_ANF = models.CharField(max_length=255)
    STR_KM_END = models.CharField(max_length=255)
    ISK_NETZ = models.CharField(max_length=255)
    BAHNNUTZUNG = models.CharField(max_length=255)
    BETREIBERART = models.CharField(max_length=255)
    geometry = models.TextField()

    class Meta:
        db_table = 'GSL_grouped_ISK_2022'
    
    def __str__(self):
        return str(self.STR_NR)


class GSL_ISK_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    #STR_NR = models.IntegerField(primary_key=True)
    STR_KURZNAME = models.CharField(max_length=255)
    STR_KM_ANF = models.CharField(max_length=255)
    STR_KM_END = models.CharField(max_length=255)
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    RI = models.CharField(max_length=255)
    LAENGE = models.IntegerField()
    DB_BETRIEB = models.CharField(max_length=255)
    ISK_NETZ = models.CharField(max_length=255)
    BAHNNUTZUNG = models.CharField(max_length=255)
    BETREIBERART = models.CharField(max_length=255)
    SONDERFALL = models.CharField(max_length=255)
    SONST_VERTR = models.CharField(max_length=255)
    AUSLAND = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='gsl')

    class Meta:
        db_table = 'GSL_ISK_2022'




class SML_ISK_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    #STR_NR = models.IntegerField(primary_key=True)
    RI = models.CharField(max_length=255)
    STR_KURZNAME = models.CharField(max_length=255)
    STR_KM_ANF = models.CharField(max_length=255)
    STR_KM_END = models.CharField(max_length=255)
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    LAENGE = models.IntegerField()
    ELEKTR = models.CharField(max_length=255)
    BAHNART = models.CharField(max_length=255)
    GL_ANZ = models.IntegerField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='sml')


    class Meta:
        db_table = 'SML_ISK_2022'


class weichen_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255) 
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key = True)
    #STR_NR = models.IntegerField()
    LAGE_KM = models.CharField(max_length=255)
    LAGE_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    RIL_100 = models.CharField(max_length=255) 
    GLEISART = models.IntegerField()
    WK_NR = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()


    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='weichen')

    class Meta:
        db_table = 'weichen_ISK_2022'

class stuetzauwerke_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key=True)
    #STR_NR = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    LAGE = models.CharField(max_length=255)
    LAENGE = models.IntegerField()
    BAUART = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='stuetzbauwerke')


    class Meta:
        db_table = 'stuetzauwerke_ISK_2022'


class schallschutzwaende_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key=True)
    #STR_NR = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    LAENGE = models.IntegerField()
    LAGE = models.CharField(max_length=255)
    BAUART = models.CharField(max_length=255)
    MIN_HOEHE = models.FloatField()
    MAX_HOEHE = models.FloatField()
    GLEISABSTAND = models.FloatField()
    MATERIAL_WAND = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='schallschutzwaende')


    class Meta:
        db_table = 'schallschutzwaende_ISK_2022'



class ETCS_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    #str_nr = models.IntegerField(primary_key=True) 
    str_name = models.CharField(max_length=255)
    heute_ohne_ETCS = models.FloatField()
    heute_ETCS_Level_1 = models.FloatField()
    heute_ETCS_Level_2 = models.FloatField()
    geplant_ETCS_L1LS = models.FloatField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='ETCS')


    class Meta:
        db_table = 'ETCS_2022'



class traffic_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    #STR_NR = models.IntegerField(primary_key=True)
    AverageAnualTFlow = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='traffic')

    class Meta:
        db_table = 'traffic_2022'


class hlk_zeitraum_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    HLK_Name = models.CharField(max_length=255)
    #STR_NR = models.IntegerField(primary_key=True)
    Zeitraum = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='HLK_Zeitraum')


    class Meta:
        db_table = 'hlk_zeitraum_2022'


class bruecken_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key=True)
    ANLAGEN_UNR = models.IntegerField()
    #STR_NR = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    RIL_100 = models.CharField(max_length=255)
    STR_MEHRFACHZUORD = models.CharField(max_length=255)
    FLAECHE = models.CharField(max_length=255)
    BR_BEZ = models.CharField(max_length=255)
    BAUART = models.CharField(max_length=255)
    BESCHREIBUNG = models.CharField(max_length=255)
    ZUST_KAT = models.CharField(max_length=255)
    WL_SERVICEEINR = models.CharField(max_length=255)
    Match = models.CharField(max_length=255)
    GEOGR_BREITE = models.FloatField()
    GEOGR_LAENGE = models.FloatField()
    lat = models.FloatField()
    lon = models.FloatField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='bruecken')


    class Meta:
        db_table = 'bruecken_ISK_2022'


class bahnuebergaenge_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR_FABA = models.IntegerField(primary_key=True)
    ANLAGEN_NR_LST = models.CharField(max_length=255)
    #STR_NR = models.IntegerField()
    LAGE_KM = models.CharField(max_length=255)
    LAGE_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    RIL_100 = models.CharField(max_length=255)
    UEB_WACH_ART = models.CharField(max_length=255)
    ZUGGEST = models.CharField(max_length=255)
    WL_SERVICEEINR = models.CharField(max_length=255)
    Matching = models.FloatField()
    Abs_Dif_cm = models.CharField(max_length=255)
    breite = models.FloatField()
    laenge = models.FloatField()
    lat = models.FloatField()
    lon = models.FloatField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='bahnuebergaenge')


    class Meta:
        db_table = 'bahnuebergaenge_ISK_2022'


class tunnel_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key=True)
    #STR_NR = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    RIL_100 = models.CharField(max_length=255)
    STR_MEHRFACHZUORD = models.CharField(max_length=255)
    LAENGE = models.IntegerField()
    ANZ_STR_GL = models.IntegerField()
    QUERSCHN = models.CharField(max_length=255)
    BAUWEISE = models.CharField(max_length=255)
    WL_SERVICEEINR = models.CharField(max_length=255)
    Matching = models.CharField(max_length=255)
    geometry = models.TextField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='tunnel')

    class Meta:
        db_table = 'tunnel_ISK_2022'


class stationen_ISK_2022(models.Model):
    Bf_NR = models.IntegerField(primary_key=True)
    ifopt = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    priceCategory = models.CharField(max_length=255)
    hasParking = models.BooleanField()
    hasBicycleParking = models.BooleanField()
    hasLocalPublicTransport = models.BooleanField()
    hasPublicFacilities = models.BooleanField()
    hasLockerSystem = models.BooleanField()
    hasTaxiRank = models.BooleanField()
    hasTravelNecessities = models.BooleanField()
    hasSteplessAccess = models.BooleanField()
    hasMobilityService = models.BooleanField()
    hasWiFi = models.BooleanField()
    hasTravelCenter = models.BooleanField()
    hasRailwayMission = models.BooleanField()
    hasDBLounge = models.BooleanField()
    hasLostAndFound = models.BooleanField()
    hasCarRental = models.BooleanField()
    federalState = models.CharField(max_length=255)
    regionalbereich_number = models.IntegerField()
    regionalbereich_name = models.CharField(max_length=255)
    regionalbereich_shortName = models.CharField(max_length=255)
    aufgabentraeger_shortName = models.CharField(max_length=255)
    aufgabentraeger_name = models.CharField(max_length=255)
    localServiceStaff_availability_monday_fromTime = models.CharField(max_length=255)
    localServiceStaff_availability_monday_toTime = models.CharField(max_length=255)
    localServiceStaff_availability_tuesday_fromTime = models.CharField(max_length=255)
    localServiceStaff_availability_tuesday_toTime = models.CharField(max_length=255)
    localServiceStaff_availability_wednesday_fromTime = models.CharField(max_length=255)
    localServiceStaff_availability_wednesday_toTime = models.CharField(max_length=255)
    localServiceStaff_availability_thursday_fromTime = models.CharField(max_length=255)
    localServiceStaff_availability_thursday_toTime = models.CharField(max_length=255)
    localServiceStaff_availability_friday_fromTime = models.CharField(max_length=255)
    localServiceStaff_availability_friday_toTime = models.CharField(max_length=255)
    localServiceStaff_availability_saturday_fromTime = models.CharField(max_length=255)
    localServiceStaff_availability_saturday_toTime = models.CharField(max_length=255)
    localServiceStaff_availability_sunday_fromTime = models.CharField(max_length=255)
    localServiceStaff_availability_sunday_toTime = models.CharField(max_length=255)
    localServiceStaff_availability_holiday_fromTime = models.CharField(max_length=255)
    localServiceStaff_availability_holiday_toTime = models.CharField(max_length=255)
    timeTableOffice_email = models.EmailField()
    timeTableOffice_name = models.CharField(max_length=255)
    szentrale_number = models.IntegerField()
    szentrale_publicPhoneNumber = models.CharField(max_length=255)
    szentrale_name = models.CharField(max_length=255)
    stationManagement_number = models.IntegerField()
    stationManagement_name = models.CharField(max_length=255)
    evaNumbers_number = models.IntegerField()
    evaNumbers_geographicCoordinates = models.CharField(max_length=255)
    ril100Identifiers_rilIdentifier = models.CharField(max_length=255)
    ril100Identifiers_isMain = models.BooleanField()
    ril100Identifiers_hasSteamPermission = models.BooleanField()
    ril100Identifiers_steamPermission = models.CharField(max_length=255)
    ril100Identifiers_geographicCoordinates = models.CharField(max_length=255)
    ril100Identifiers_primaryLocationCode = models.CharField(max_length=255)
    productLine_productLine = models.CharField(max_length=255)
    productLine_segment = models.CharField(max_length=255)

    class Meta:
        db_table = 'stationen_ISK_2022'


class bahnsteige_ISK_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    Land = models.CharField(max_length=255)
    Regionalbereich = models.CharField(max_length=255)
    Bahnhofsmanagement = models.CharField(max_length=255)
    Streckenbezeichnung = models.CharField(max_length=255)
    Ril_100 = models.CharField(max_length=255)
    Verkehrsstation = models.CharField(max_length=255)
    Reisende_je_Tag_und_Station_2019 = models.IntegerField()
    Bahnsteig = models.CharField(max_length=255)
    Gleisbezeichnung = models.CharField(max_length=255)
    Anlagengruppe = models.CharField(max_length=255)
    Bahnsteigart = models.CharField(max_length=255)
    Baulänge_Bahnsteig_m = models.FloatField()
    davon_nicht_öffentlich_zugänglich_m = models.FloatField()
    Bauhöhe_cm = models.IntegerField()
    Zielehöhe_cm = models.IntegerField()
    Bahnsteig_mittlere_Baubreite_m = models.FloatField()
    Nutzungsaufnahme_IBN_Jahr = models.IntegerField()
    Zugangsmöglichkeit = models.CharField(max_length=255)
    Stufenfreiheit = models.CharField(max_length=255)
    Fahrgastinformationsanlagen_FIA = models.CharField(max_length=255)
    Lautsprecher_DSA_Akustikmodul = models.CharField(max_length=255)
    Taktiles_Leitsystem_auf_dem_Bstg = models.CharField(max_length=255)
    Taktiler_Weg_vom_öffentlichen_Bereich_zum_Bstg = models.CharField(max_length=255)
    Stufenmarkierung_an_Treppen = models.CharField(max_length=255)
    Taktile_Handlaufschilder_Treppen_und_Rampen = models.CharField(max_length=255)
    Wegeleitsystem_WLS = models.CharField(max_length=255)
    Ist_Baulänge_Bstg_dach_dächer_im_eigentum_DB_Station_Service = models.FloatField()
    Ist_Baulänge_Bstg_dach_dächer_Eigentum_Dritter = models.FloatField()
    davon_über_nicht_zugänglichem_Bereich = models.FloatField()
    Denkmalschutz_Bstg_dach = models.CharField(max_length=255)
    Länge_Bstg_unter_Halle_m = models.FloatField()
    Länge_Überbauung_20_m = models.FloatField()
    Anzahl_WSH = models.IntegerField()
    davon_Anzahl_WSH_unter_Halle_Dach_Überb = models.CharField(max_length=255)
    stufenfrei_cod = models.CharField(max_length=255)
    fia_cod = models.CharField(max_length=255)
    akustik_cod = models.CharField(max_length=255)
    bstgtakleitsys_cod = models.CharField(max_length=255)
    takbereichbstg_cod = models.CharField(max_length=255)
    stufmark_cod = models.CharField(max_length=255)
    takhandlauf_cod = models.CharField(max_length=255)
    wls_cod = models.CharField(max_length=255)
    weitreichend_barrierefrei = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='bahnsteige_2022_gsl')
    Bf_NR = models.ForeignKey(stationen_ISK_2022, on_delete=models.CASCADE, db_column='Bf_NR', related_name='bahnsteige_2022_Bf')    

    class Meta:
        db_table = 'bahnsteige_ISK_2022'


class vst_sts_ISK_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    Anzahl_Bahnsteige = models.IntegerField()
    Reisende_je_Tag_und_Station_2019 = models.CharField(max_length=255)
    Land = models.CharField(max_length=255)
    Regionalbereich = models.CharField(max_length=255)
    #Bf_NR = models.IntegerField()
    Bahnhofsmanagement = models.CharField(max_length=255)
    Ril_100 = models.CharField(max_length=255)
    Verkehrsstation = models.CharField(max_length=255)
    Aufzüge = models.CharField(max_length=255)
    Fahrtreppen = models.CharField(max_length=255)
    Rampen = models.CharField(max_length=255)
    stufenfrei_cod = models.CharField(max_length=255)
    fia_cod = models.CharField(max_length=255)
    akustik_cod = models.CharField(max_length=255)
    bstgtakleitsys_cod = models.CharField(max_length=255)
    takbereichbstg_cod = models.CharField(max_length=255)
    stufmark_cod = models.CharField(max_length=255)
    takhandlauf_cod = models.CharField(max_length=255)
    wls_cod = models.CharField(max_length=255)
    weitreichend_barrierefrei = models.CharField(max_length=255)

    Bf_NR = models.ForeignKey(stationen_ISK_2022, on_delete=models.CASCADE, db_column='Bf_NR', related_name='vst_sts_ISK_2022')    

    
    class Meta:
        db_table = 'vst_sts_ISK_2022'


class df_change_bstg_sts_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    Land = models.CharField(max_length=255)
    Regionalbereich = models.CharField(max_length=255)
    Bahnhofsmanagement = models.CharField(max_length=255)
    #STR_NR = models.CharField(max_length=255)
    Streckenbezeichnung = models.CharField(max_length=255)
    Ril_100 = models.CharField(max_length=255)
    Bf_Nr_2022 = models.CharField(max_length=255)
    Verkehrsstation_2022 = models.CharField(max_length=255)
    Reisende_je_Tag_und_Station_2019 = models.IntegerField()
    Bahnsteig = models.CharField(max_length=255)
    Gleisbezeichnung = models.CharField(max_length=255)
    Anlagengruppe = models.CharField(max_length=255)
    Bahnsteigart = models.CharField(max_length=255)
    Baulänge_Bahnsteig_m_2022 = models.FloatField()
    davon_nicht_öffentlich_zugänglich_m_2022 = models.FloatField()
    Bauhöhe_cm_2022 = models.IntegerField()
    Zielehöhe_cm_2022 = models.IntegerField()
    Bahnsteig_mittlere_Baubreite_m_2022 = models.FloatField()
    Nutzungsaufnahme_IBN_Jahr_2022 = models.IntegerField()
    Zugangsmöglichkeit_2022 = models.CharField(max_length=255)
    Stufenfreiheit = models.CharField(max_length=255)
    Fahrgastinformationsanlagen_FIA = models.CharField(max_length=255)
    Lautsprecher_DSA_Akustikmodul = models.CharField(max_length=255)
    Taktiles_Leitsystem_auf_dem_Bstg = models.CharField(max_length=255)
    Taktiler_Weg_vom_öffentlichen_Bereich_zum_Bstg = models.CharField(max_length=255)
    Stufenmarkierung_an_Treppen = models.CharField(max_length=255)
    Taktile_Handlaufschilder_Treppen_und_Rampen = models.CharField(max_length=255)
    Wegeleitsystem_WLS = models.CharField(max_length=255)
    Ist_Baulänge_Bstg_dach_dächer_im_eigentum_DB_Station_Service = models.FloatField()
    Ist_Baulänge_Bstg_dach_dächer_Eigentum_Dritter = models.FloatField()
    davon_über_nicht_zugänglichem_Bereich = models.FloatField()
    Denkmalschutz_Bstgdach = models.CharField(max_length=255)
    Länge_Bstg_unter_Halle_m = models.FloatField()
    Länge_Überbauung_20_m = models.FloatField()
    Anzahl_WSH = models.IntegerField()
    davon_Anzahl_WSH_unter_Halle_Dach_Überb = models.IntegerField()
    stufenfrei_cod_2022 = models.CharField(max_length=255)
    fia_cod_2022 = models.CharField(max_length=255)
    akustik_cod_2022 = models.CharField(max_length=255)
    bstgtakleitsys_cod_2022 = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='df_change_bstg_sts_2022')
    

    class Meta:
        db_table = 'df_change_bstg_sts_2022'



class df_change_vst_sts_2022(models.Model):
    Anzahl_Bahnsteige_x = models.IntegerField()
    Reisende_je_Tag_und_Station_2019 = models.IntegerField()
    Land = models.CharField(max_length=255)
    Regionalbereich = models.CharField(max_length=255)
    Bahnhofsmanagement = models.CharField(max_length=255)
    Ril_100 = models.CharField(max_length=255)
    #Bf_NR = models.IntegerField()
    Verkehrsstation_2022 = models.CharField(max_length=255)
    Aufzüge_2022 = models.IntegerField()
    Fahrtreppen_2022 = models.IntegerField()
    Rampen_2022 = models.IntegerField()
    stufenfrei_cod_2022 = models.CharField(max_length=255)
    fia_cod_2022 = models.CharField(max_length=255)
    akustik_cod_2022 = models.CharField(max_length=255)
    bstgtakleitsys_cod_2022 = models.CharField(max_length=255)
    takbereichbstg_cod_2022 = models.CharField(max_length=255)
    stufmark_cod_2022 = models.CharField(max_length=255)
    takhandlauf_cod_2022 = models.CharField(max_length=255)
    wls_cod_2022 = models.CharField(max_length=255)
    weitreichend_barrierefrei_2022 = models.CharField(max_length=255)
    Anzahl_Bahnsteige_2021 = models.IntegerField()
    Verkehrsstation_2021 = models.CharField(max_length=255)
    Aufzüge_2021 = models.IntegerField()
    Fahrtreppen_2021 = models.IntegerField()
    Rampen_2021 = models.IntegerField()
    stufenfrei_cod_2021 = models.CharField(max_length=255)
    fia_cod_2021 = models.CharField(max_length=255)
    akustik_cod_2021 = models.CharField(max_length=255)
    bstgtakleitsys_cod_2021 = models.CharField(max_length=255)
    takbereichbstg_cod_2021 = models.CharField(max_length=255)
    stufmark_cod_2021 = models.CharField(max_length=255)
    takhandlauf_cod_2021 = models.CharField(max_length=255)
    wls_cod_2021 = models.CharField(max_length=255)
    weitreichend_barrierefrei_2021 = models.CharField(max_length=255)
    stufenfrei_cod_21_22 = models.CharField(max_length=255)
    fia_cod_21_22 = models.CharField(max_length=255)
    akustik_cod_21_22 = models.CharField(max_length=255)
    bstgtakleitsys_cod_21_22 = models.CharField(max_length=255)
    takbereichbstg_cod_21_22 = models.CharField(max_length=255)
    stufmark_cod_21_22 = models.CharField(max_length=255)
    takhandlauf_cod_21_22 = models.CharField(max_length=255)
    wls_cod_21_22 = models.CharField(max_length=255)
    weitreichend_barrierefrei_21_22 = models.CharField(max_length=255)
    Anzahl_Bahnsteige_21_22 = models.IntegerField()
    Aufzüge_21_22 = models.IntegerField()
    Fahrtreppen_21_22 = models.IntegerField()
    Rampen_21_22 = models.IntegerField()
    Vst_21_22 = models.CharField(max_length=255)
    ID = models.IntegerField(primary_key=True)

    Bf_NR = models.ForeignKey(stationen_ISK_2022, on_delete=models.CASCADE, db_column='Bf_NR', related_name='df_change_vst_sts_2022_Bf')


    class Meta:
        db_table = 'df_change_vst_sts_2022'



# 2021 ############################################################################################

class bahnsteige_ISK_2021(models.Model):
    ID = models.IntegerField(primary_key=True)
    Land = models.CharField(max_length=255)
    Regionalbereich = models.CharField(max_length=255)
    Bahnhofsmanagement = models.CharField(max_length=255)
    Streckenbezeichnung = models.CharField(max_length=255)
    Ril_100 = models.CharField(max_length=255)
    #Bf_NR = models.IntegerField()
    Verkehrsstation = models.CharField(max_length=255)
    Reisende_je_Tag_und_Station_2019 = models.IntegerField()
    Bahnsteig = models.CharField(max_length=255)
    Anlagengruppe = models.CharField(max_length=255)
    Bahnsteigart = models.CharField(max_length=255)
    Baulänge_Bahnsteig_m = models.FloatField()
    davon_nicht_öffentlich_zugänglich_m = models.FloatField()
    Bauhöhe_cm = models.IntegerField()
    Zielehöhe_cm = models.IntegerField()
    Bahnsteig_mittlere_Baubreite_m = models.FloatField()
    Nutzungsaufnahme_IBN_Jahr = models.IntegerField()
    Zugangsmöglichkeit = models.CharField(max_length=255)
    Stufenfreiheit = models.CharField(max_length=255)
    Fahrgastinformationsanlagen_FIA = models.CharField(max_length=255)
    Lautsprecher_DSA_Akustikmodul = models.CharField(max_length=255)
    Taktiles_Leitsystem_auf_dem_Bstg = models.CharField(max_length=255)
    Taktiler_Weg_vom_öffentlichen_Bereich_zum_Bstg = models.CharField(max_length=255)
    Stufenmarkierung_an_Treppen = models.CharField(max_length=255)
    Taktile_Handlaufschilder_Treppen_und_Rampen = models.CharField(max_length=255)
    Wegeleitsystem_WLS = models.CharField(max_length=255)
    Ist_Baulänge_Bstg_dach_dächer_im_eigentum_DB_Station_Service = models.FloatField()
    Ist_Baulänge_Bstg_dach_dächer_Eigentum_Dritter = models.FloatField()
    davon_über_nicht_zugänglichem_Bereich = models.FloatField()
    Denkmalschutz_Bstg_dach = models.CharField(max_length=255)
    Länge_Bstg_unter_Halle_m = models.FloatField()
    Länge_Überbauung_20_m = models.FloatField()
    Anzahl_WSH = models.IntegerField()
    davon_Anzahl_WSH_unter_Halle_Dach_Überb = models.IntegerField()
    stufenfrei_cod = models.CharField(max_length=255)
    fia_cod = models.CharField(max_length=255)
    akustik_cod = models.CharField(max_length=255)
    bstgtakleitsys_cod = models.CharField(max_length=255)
    takbereichbstg_cod = models.CharField(max_length=255)
    stufmark_cod = models.CharField(max_length=255)
    takhandlauf_cod = models.CharField(max_length=255)
    wls_cod = models.CharField(max_length=255)
    weitreichend_barrierefrei = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='bahnsteige_ISK_2021_gsl')
    Bf_NR = models.ForeignKey(stationen_ISK_2022, on_delete=models.CASCADE, db_column='Bf_NR', related_name='bahnsteige_ISK_2021_gsl_Bf')

    
    class Meta:
        db_table = 'bahnsteige_ISK_2021'


class vst_sts_ISK_2021(models.Model):
    ID = models.IntegerField(primary_key=True)
    Anzahl_Bahnsteige = models.IntegerField()
    Reisende_je_Tag_und_Station_2019 = models.IntegerField()
    Land = models.CharField(max_length=255)
    Regionalbereich = models.CharField(max_length=255)
    Bahnhofsmanagement = models.CharField(max_length=255)
    Ril_100 = models.CharField(max_length=255)
    #Bf_NR = models.IntegerField()
    Verkehrsstation = models.CharField(max_length=255)
    Aufzüge = models.IntegerField()
    Fahrtreppen = models.IntegerField()
    Rampen = models.IntegerField()
    stufenfrei_cod = models.CharField(max_length=255)
    fia_cod = models.CharField(max_length=255)
    akustik_cod = models.CharField(max_length=255)
    bstgtakleitsys_cod = models.CharField(max_length=255)
    takbereichbstg_cod = models.CharField(max_length=255)
    stufmark_cod = models.CharField(max_length=255)
    takhandlauf_cod = models.CharField(max_length=255)
    wls_cod = models.CharField(max_length=255)
    weitreichend_barrierefrei = models.CharField(max_length=255)

    Bf_NR = models.ForeignKey(stationen_ISK_2022, on_delete=models.CASCADE, db_column='Bf_NR', related_name='df_change_vst_sts_2022_stationen')

    
    class Meta:
        db_table = 'vst_sts_ISK_2021'



class df_change_merge_stationen(models.Model):
    Anzahl_Bahnsteige_x = models.IntegerField()
    Reisende_je_Tag_und_Station_2019 = models.IntegerField()
    Land = models.CharField(max_length=255)
    Regionalbereich = models.CharField(max_length=255)
    Bahnhofsmanagement = models.CharField(max_length=255)
    Ril_100 = models.CharField(max_length=255)
    Verkehrsstation_2022 = models.CharField(max_length=255)
    Aufzüge_2022 = models.IntegerField()
    Fahrtreppen_2022 = models.IntegerField()
    Rampen_2022 = models.IntegerField()
    stufenfrei_cod_2022 = models.CharField(max_length=255)
    fia_cod_2022 = models.CharField(max_length=255)
    akustik_cod_2022 = models.CharField(max_length=255)
    bstgtakleitsys_cod_2022 = models.CharField(max_length=255)
    takbereichbstg_cod_2022 = models.CharField(max_length=255)
    stufmark_cod_2022 = models.CharField(max_length=255)
    takhandlauf_cod_2022 = models.CharField(max_length=255)
    wls_cod_2022 = models.CharField(max_length=255)
    weitreichend_barrierefrei_2022 = models.CharField(max_length=255)
    Anzahl_Bahnsteige_2021 = models.IntegerField()
    Verkehrsstation_2021 = models.CharField(max_length=255)
    Aufzüge_2021 = models.IntegerField()
    Fahrtreppen_2021 = models.IntegerField()
    Rampen_2021 = models.IntegerField()
    stufenfrei_cod_2021 = models.CharField(max_length=255)
    fia_cod_2021 = models.CharField(max_length=255)
    akustik_cod_2021 = models.CharField(max_length=255)
    bstgtakleitsys_cod_2021 = models.CharField(max_length=255)
    takbereichbstg_cod_2021 = models.CharField(max_length=255)
    stufmark_cod_2021 = models.CharField(max_length=255)
    takhandlauf_cod_2021 = models.CharField(max_length=255)
    wls_cod_2021 = models.CharField(max_length=255)
    weitreichend_barrierefrei_2021 = models.CharField(max_length=255)
    stufenfrei_cod_21_22 = models.CharField(max_length=255)
    fia_cod_21_22 = models.CharField(max_length=255)
    akustik_cod_21_22 = models.CharField(max_length=255)
    bstgtakleitsys_cod_21_22 = models.CharField(max_length=255)
    takbereichbstg_cod_21_22 = models.CharField(max_length=255)
    stufmark_cod_21_22 = models.CharField(max_length=255)
    takhandlauf_cod_21_22 = models.CharField(max_length=255)
    wls_cod_21_22 = models.CharField(max_length=255)
    weitreichend_barrierefrei_21_22 = models.CharField(max_length=255)
    Anzahl_Bahnsteige_21_22 = models.IntegerField()
    Aufzüge_21_22 = models.IntegerField()
    Fahrtreppen_21_22 = models.IntegerField()
    Rampen_21_22 = models.IntegerField()
    Vst_21_22 = models.CharField(max_length=255)
    ID = models.IntegerField(primary_key=True)
    ifopt = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    priceCategory = models.CharField(max_length=255)
    hasParking = models.BooleanField()
    hasBicycleParking = models.BooleanField()
    hasLocalPublicTransport = models.BooleanField()
    hasPublicFacilities = models.BooleanField()
    hasLockerSystem = models.BooleanField()
    hasTaxiRank = models.BooleanField()
    hasTravelNecessities = models.BooleanField()
    hasSteplessAccess = models.BooleanField()
    hasMobilityService = models.BooleanField()
    hasWiFi = models.BooleanField()
    hasTravelCenter = models.BooleanField()
    hasRailwayMission = models.BooleanField()
    hasDBLounge = models.BooleanField()
    hasLostAndFound = models.BooleanField()
    hasCarRental = models.BooleanField()
    federalState = models.CharField(max_length=255)
    regionalbereich_number = models.IntegerField()
    regionalbereich_name = models.CharField(max_length=255)
    regionalbereich_shortName = models.CharField(max_length=255)
    aufgabentraeger_shortName = models.CharField(max_length=255)
    aufgabentraeger_name = models.CharField(max_length=255)
    localServiceStaff_availability_monday_fromTime = models.TimeField()
    localServiceStaff_availability_monday_toTime = models.TimeField()
    localServiceStaff_availability_tuesday_fromTime = models.TimeField()
    localServiceStaff_availability_tuesday_toTime = models.TimeField()
    localServiceStaff_availability_wednesday_fromTime = models.TimeField()
    localServiceStaff_availability_wednesday_toTime = models.TimeField()
    localServiceStaff_availability_thursday_fromTime = models.TimeField()
    localServiceStaff_availability_thursday_toTime = models.TimeField()
    localServiceStaff_availability_friday_fromTime = models.TimeField()
    localServiceStaff_availability_friday_toTime = models.TimeField()
    localServiceStaff_availability_saturday_fromTime = models.TimeField()
    localServiceStaff_availability_saturday_toTime = models.TimeField()
    localServiceStaff_availability_sunday_fromTime = models.TimeField()
    localServiceStaff_availability_sunday_toTime = models.TimeField()
    localServiceStaff_availability_holiday_fromTime = models.TimeField()
    localServiceStaff_availability_holiday_toTime = models.TimeField()
    timeTableOffice_email = models.EmailField()
    timeTableOffice_name = models.CharField(max_length=255)
    szentrale_number = models.IntegerField()
    szentrale_publicPhoneNumber = models.CharField(max_length=255)
    szentrale_name = models.CharField(max_length=255)
    stationManagement_number = models.IntegerField()
    stationManagement_name = models.CharField(max_length=255)
    evaNumbers_number = models.IntegerField()
    evaNumbers_geographicCoordinates = models.CharField(max_length=255)
    ril100Identifiers_rilIdentifier = models.CharField(max_length=255)
    ril100Identifiers_isMain = models.BooleanField()
    ril100Identifiers_hasSteamPermission = models.BooleanField()
    ril100Identifiers_steamPermission = models.CharField(max_length=255)
    ril100Identifiers_geographicCoordinates = models.CharField(max_length=255)
    ril100Identifiers_primaryLocationCode = models.CharField(max_length=255)
    productLine_productLine = models.CharField(max_length=255)
    productLine_segment = models.CharField(max_length=255)

    Bf_NR = models.ForeignKey(stationen_ISK_2022, on_delete=models.CASCADE, db_column='Bf_NR', related_name='df_change_merge_stationen_BF_ISK')

    class Meta:
        db_table = 'df_change_merge_stationen'
