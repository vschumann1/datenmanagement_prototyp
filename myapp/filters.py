import django_filters
from .models import GSL_grouped_ISK_2022, weichen_ISK_2022, tunnel_ISK_2022, bahnuebergaenge_ISK_2022, bruecken_ISK_2022, stuetzauwerke_ISK_2022, schallschutzwaende_ISK_2022, bahnsteige_ISK_2022, df_change_vst_sts_2022, SML_ISK_2022
from django_filters import widgets
from django.forms import CharField, TextInput
from django.db.models import Q
from django_select2.forms import Select2MultipleWidget

from django import forms
from django_filters import Filter, ModelChoiceFilter, CharFilter, ChoiceFilter, BooleanFilter
from django.forms import ModelChoiceField
from django.forms.widgets import CheckboxSelectMultiple, Select



STATE_ABBREVIATIONS = {
    'Baden-Württemberg':'BW',
    'Bayern':'BY',
    'Hamburg':'HH',
    'Schleswig-Holstein':'SH',
    'Niedersachsen':'NI',
    'Rheinland-Pfalz':'RP',
    'Hessen':'HE',
    'Bremen':'HB',
    'Saarland':'SL',
    'Brandenburg':'BB',
    'Berlin':'BE',
    'Sachsen':'SN',
    'Thüringen':'TH',
    'Sachsen-Anhalt':'ST',
    'Mecklenburg-Vorpommern':'MV',
}

class CustomBooleanSelect(Select):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.choices = [
            ('', '-'),
            ('true', 'Ja'),
            ('false', 'Nein'),
        ]

class CustomBooleanFilter(BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = CustomBooleanSelect()
        super().__init__(*args, **kwargs)



class CommaSeparatedCharFilter(Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            # Split the value by commas and strip whitespace
            values = [v.strip() for v in value.split(',')]
            # Create a Q object for each value and combine them with OR
            q_objects = Q()
            for val in values:
                q_objects |= Q(**{f"{self.field_name}__iexact": val})
            return qs.filter(q_objects)
        return qs       
    
class BundeslandCheckboxFilter(django_filters.MultipleChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = CheckboxSelectMultiple
        kwargs['choices'] = [(abbr, name) for name, abbr in STATE_ABBREVIATIONS.items()]
        super(BundeslandCheckboxFilter, self).__init__(*args, **kwargs)

class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.STR_NR}"  # Customize the label here

class CustomModelChoiceFilter(ModelChoiceFilter):
    field_class = CustomModelChoiceField

    def filter(self, qs, value):
        print("Filtering value:", value)
        filtered_qs = super().filter(qs, value)
        print("Filtered queryset count:", filtered_qs.count())
        return filtered_qs

class ListCharFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value not in (None, '', 'alle'):  # 'alle' acts as a bypass keyword
            values = [v.strip() for v in value.split(',')]
            return qs.filter(**{f'{self.field_name}__in': values})
        return qs

class GSLFilter(django_filters.FilterSet):
    STR_NR = ListCharFilter(field_name='STR_NR', lookup_expr='in', label='Streckennummer:', widget=TextInput(attrs={'placeholder': '4010'}))

    def __init__(self, *args, **kwargs):
        super(GSLFilter, self).__init__(*args, **kwargs)
        if not self.data.get('STR_NR'):
            self.queryset = self.queryset.filter(STR_NR__in=['4010'])

    class Meta:
        model = GSL_grouped_ISK_2022
        fields = ['STR_NR']


class SMLFilter(django_filters.FilterSet):
    gsl_grouped_isk_2022 =CommaSeparatedCharFilter(
        field_name='gsl_grouped_isk_2022__STR_NR',  # Adjust as needed
        label='Streckennummer',
    )

    LAND = BundeslandCheckboxFilter(
        field_name='LAND',  # Adjust if your model field is named differently
        label='Bundesland',
    )






class ChangeVSTSTSFilter(django_filters.FilterSet):
    Verkehrsstation_2022 = django_filters.CharFilter(lookup_expr='icontains')
    Aufzüge_2022 = django_filters.NumberFilter()
    Fahrtreppen_2022 = django_filters.NumberFilter()
    Rampen_2022 = django_filters.NumberFilter()

    Verkehrsstation_2021 = django_filters.CharFilter(lookup_expr='icontains')
    Aufzüge_2021 = django_filters.NumberFilter()
    Fahrtreppen_2021 = django_filters.NumberFilter()
    Rampen_2021 = django_filters.NumberFilter()

    #ab hier seperat
    hasParking = CustomBooleanFilter(
        field_name='hasParking',  # Adjust as needed
        label='hasParking',
    )

    hasBicycleParking = CustomBooleanFilter(
        field_name='hasBicycleParking',  # Adjust as needed
        label='hasBicycleParking',
    )
    hasLocalPublicTransport = CustomBooleanFilter(
        field_name='hasLocalPublicTransport',  # Adjust as needed
        label='hasLocalPublicTransport',
    )
    hasPublicFacilities = CustomBooleanFilter(
        field_name='hasPublicFacilities',  # Adjust as needed
        label='hasPublicFacilities',
    )
    hasLockerSystem = CustomBooleanFilter(
        field_name='hasLockerSystem',  # Adjust as needed
        label='hasLockerSystem',
    )
    hasTaxiRank = CustomBooleanFilter(
        field_name='hasTaxiRank',  # Adjust as needed
        label='hasTaxiRank',
    )
    hasTravelNecessities = CustomBooleanFilter(
        field_name='hasTravelNecessities',  # Adjust as needed
        label='hasTravelNecessities',
    )
    hasSteplessAccess = CustomBooleanFilter(
        field_name='hasSteplessAccess',  # Adjust as needed
        label='hasSteplessAccess',
    )
    hasMobilityService = CustomBooleanFilter(
        field_name='hasMobilityService',  # Adjust as needed
        label='hasMobilityService',
    )
    hasWiFi = CustomBooleanFilter(
        field_name='hasWiFi',  # Adjust as needed
        label='hasWiFi',
    )
    hasTravelCenter = CustomBooleanFilter(
        field_name='hasTravelCenter',  # Adjust as needed
        label='hasTravelCenter',
    )
    hasRailwayMission = CustomBooleanFilter(
        field_name='hasRailwayMission',  # Adjust as needed
        label='hasRailwayMission',
    )
    hasParking = CustomBooleanFilter(
        field_name='hasParking',  # Adjust as needed
        label='Parkplatz',
    )
    hasDBLounge = CustomBooleanFilter(
        field_name='hasDBLounge',  # Adjust as needed
        label='hasDBLounge',
    )
    hasLostAndFound = CustomBooleanFilter(
        field_name='hasLostAndFound',  # Adjust as needed
        label='hasLostAndFound',
    )
    hasCarRental = CustomBooleanFilter(
        field_name='hasCarRental',  # Adjust as needed
        label='hasCarRental',
    )

    Bf_NR = CommaSeparatedCharFilter(
        field_name='Bf_NR__Bf_NR',  # Adjust as needed
        label='Bf_NR',
    )

    

    class Meta:
        model = df_change_vst_sts_2022
        fields = [
            'Land', 
            'Bf_NR', 
            'hasParking',
    

            # Add any other default fields here
        ]













from .models import stationen_ISK_2022

class StationenFilter(django_filters.FilterSet):
    Bf_NR = CharFilter(field_name='Bf_NR', lookup_expr='iexact', label='Bahnhofnummer')
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Bahnhofname')
    federalState = CharFilter(field_name='federalState', lookup_expr='icontains', label='Bundesland')
    hasSteplessAccess = CustomBooleanFilter(field_name='hasSteplessAccess', label='Stufenloser Zugang')
    hasParking = CustomBooleanFilter(field_name='hasParking', label='Parkplatz')
    hasBicycleParking = CustomBooleanFilter(field_name='hasBicycleParking', label='Fahrradparkplatz')
    hasLocalPublicTransport = CustomBooleanFilter(field_name='hasLocalPublicTransport', label='Öffentlicher Nahverkehr')
    hasPublicFacilities = CustomBooleanFilter(field_name='hasPublicFacilities', label='WC')
    hasLockerSystem = CustomBooleanFilter(field_name='hasLockerSystem', label='Schließfächer')
    hasTaxiRank = CustomBooleanFilter(field_name='hasTaxiRank', label='Taxistand')
    hasTravelNecessities = CustomBooleanFilter(field_name='hasTravelNecessities', label='Reisebedarf')
    hasMobilityService = CustomBooleanFilter(field_name='hasMobilityService', label='Mobilitätsservice')
    hasWiFi = CustomBooleanFilter(field_name='hasWiFi', label='WLAN')
    hasTravelCenter = CustomBooleanFilter(field_name='hasTravelCenter', label='Reisezentrum')
    hasRailwayMission = CustomBooleanFilter(field_name='hasRailwayMission', label='Bahnhofsmission')
    hasDBLounge = CustomBooleanFilter(field_name='hasDBLounge', label='DB Lounge')
    hasLostAndFound = CustomBooleanFilter(field_name='hasLostAndFound', label='Fundbüro')
    hasCarRental = CustomBooleanFilter(field_name='hasCarRental', label='Autovermietung')
    

    class Meta:
        model = stationen_ISK_2022
        fields = [
            'Bf_NR', 'name', 'federalState', 'hasSteplessAccess', 'hasParking', 'hasBicycleParking', 
            'hasLocalPublicTransport', 'hasPublicFacilities', 'hasLockerSystem', 
            'hasTaxiRank', 'hasTravelNecessities', 'hasMobilityService', 'hasWiFi',
            'hasTravelCenter', 'hasRailwayMission', 'hasDBLounge', 'hasLostAndFound',
            'hasCarRental'
        ]


















class BaseISKFilter(django_filters.FilterSet):
    gsl_grouped_isk_2022 = CommaSeparatedCharFilter(
        field_name='gsl_grouped_isk_2022__STR_NR',  # Adjust as needed
        label='Streckennummer',
    )
    
           
    
    # Filter for the 'LAND' field with support for comma-separated values (CSV)
    land = BundeslandCheckboxFilter(
        field_name='LAND',  # Adjust if your model field is named differently
        label='Bundesland',
    )

    class Meta:
        abstract = True

class WeichenFilter(BaseISKFilter):
    class Meta(BaseISKFilter.Meta):
        model = weichen_ISK_2022
        fields = ['gsl_grouped_isk_2022', 'LAND']

class TunnelFilter(BaseISKFilter):
    class Meta(BaseISKFilter.Meta):
        model = tunnel_ISK_2022
        fields = ['gsl_grouped_isk_2022', 'LAND']

class BahnuebergaengeFilter(BaseISKFilter):
    class Meta(BaseISKFilter.Meta):
        model = bahnuebergaenge_ISK_2022
        fields = ['gsl_grouped_isk_2022', 'LAND']

class BrueckenFilter(BaseISKFilter):
    zust_kat = CommaSeparatedCharFilter(field_name='ZUST_KAT', label='Zustandskategorie')
    bauart = django_filters.CharFilter(field_name='BAUART', label='Bauart')
    class Meta(BaseISKFilter.Meta):
        model = bruecken_ISK_2022
        fields = ['gsl_grouped_isk_2022', 'LAND', 'zust_kat', 'bauart']

class StuetzbauwerkeFilter(BaseISKFilter):
    class Meta(BaseISKFilter.Meta):
        model = stuetzauwerke_ISK_2022
        fields = ['gsl_grouped_isk_2022', 'LAND']

class SchallschutzwaendeFilter(BaseISKFilter):
    class Meta(BaseISKFilter.Meta):
        model = schallschutzwaende_ISK_2022
        fields = ['gsl_grouped_isk_2022', 'LAND']


