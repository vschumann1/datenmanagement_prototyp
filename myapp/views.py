# myapp/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import GSL_grouped_ISK_2022, bruecken_ISK_2022, df_change_merge_stationen, tunnel_ISK_2022, weichen_ISK_2022, stuetzauwerke_ISK_2022, ETCS_2022, schallschutzwaende_ISK_2022, bahnuebergaenge_ISK_2022, stationen_ISK_2022, bahnsteige_ISK_2022, df_change_vst_sts_2022, SML_ISK_2022
from django.core.paginator import Paginator
from .filters import GSLFilter
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
import csv
from django.utils.safestring import mark_safe
import numpy as np
from .forms import MultiSelectFilterForm 
from django.db.models import Sum, Count, Case, When, IntegerField, FloatField
from django.db.models.functions import Coalesce
from shapely.geometry import LineString, MultiLineString #checken!
from shapely import wkt
from .filters import WeichenFilter, TunnelFilter, BahnuebergaengeFilter, BrueckenFilter, StuetzbauwerkeFilter, SchallschutzwaendeFilter, StationenFilter, ChangeVSTSTSFilter, SMLFilter
from django.http import QueryDict
from django.db.models import F
from django.db.models.functions import Cast
from django.db.models import IntegerField
from .functions import generate_plot_html, calculate_sums_and_counts, get_station_details, get_field_names, generate_plotly_pb_details, generate_plotly_pb_view, get_fields, show_plot, get_api_cards
from django.shortcuts import render, redirect
from django.conf import settings


#benötigt für Plotly:
mapbox_access_token = 'pk.eyJ1IjoiYW5ka29jaDkzIiwiYSI6ImNsMTZiNnU4dTE5MzQzY3MwZnV1NjVqOGoifQ.ZxCDeRkr59lifDEm4PIWQA'




def get_model_fields(model):
    return [field for field in model._meta.get_fields() if field.concrete and not field.name.startswith('_')]




def sml_view(request):
    #Filter, dass nur Strecken mit Richtung == 1 ausgewählt werden
    initial_queryset = SML_ISK_2022.objects.filter(RI=1)

    #Filter auf HTML Seite
    filters = SMLFilter(request.GET, queryset=initial_queryset)
    data = filters.qs

    #Teilt data in einzelne Seiten
    paginator = Paginator(data, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #definiert in funtions.py
    #holt alle field names von SML_ISK_2022 außer ['ID', 'RI']
    #wenn True, wird STR_NR als erste Spalte gezeigt
    fields = get_fields(SML_ISK_2022, ['ID', 'RI'], False)

    summe_laenge = round(((data.aggregate(SummeLaenge=Sum('LAENGE'))['SummeLaenge'])/1000),1)
    
    context = {
        'filters': filters,
        'page_obj': page_obj,
        'fields': fields,
        'summe_laenge': summe_laenge,
    }
    return render(request, 'myapp/sml.html', context)

#prototyp_view
def hlk_view(request):
    return render(request, 'myapp/prototyp.html')

def main_view(request):
    return render(request, 'myapp/main.html')

def geo_view(request):
    return render(request, 'myapp/geo.html')

def pb_view(request):
    
    #Checkbox um Geoplot anzuzeigen
    show_geo_plot = 'show_geo_plot' in request.POST

    #Filter, um Daten für Jahr 2022 oder 2021 zu zeigen
    year_filter = request.GET.get('year', '2022')  # Default to showing 2022 if no filter is applied

    
    #Filter auf HTML Seite
    filter = ChangeVSTSTSFilter(request.GET, queryset=df_change_merge_stationen.objects.all())
    data = filter.qs

    missing_2021 = data.filter(Verkehrsstation_2021__isnull=True).count()
    
    # Count missing 'Verkehrsstation_2022'
    missing_2022 = data.filter(Verkehrsstation_2022__isnull=True).count()
    


    #definiert in functions.py
    #holt sich alle field names je nach ausgewähltem Jahr
    field_names, year_filter = get_field_names(df_change_vst_sts_2022, stationen_ISK_2022, request, year_filter, True)
    

    #Teilt data in einzelne Seiten
    paginator = Paginator(data, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    #berechnet die Anzahl der Reihen
    anzahl = data.count()

    columns_to_sum = [
        'Anzahl_Bahnsteige_2021', 'Verkehrsstation_2021', 'Aufzüge_2021', 
        'Fahrtreppen_2021', 'Rampen_2021', 'Anzahl_Bahnsteige_x', 
        'Verkehrsstation_2022', 'Aufzüge_2022', 'Fahrtreppen_2022', 'Rampen_2022'
    ]

    year_specific_columns = {
        '2022': {
            'Anzahl_Bahnsteige_x': 'Anzahl der Bahnsteige',
            'Verkehrsstation_2022': 'Anzahl Verkehrsstation',
            'Aufzüge_2022' : 'Anzahl Aufzüge',
            'Fahrtreppen_2022' : 'Anzahl Fahrteppen',
            'Rampen_2022' :'Anzahl Rampen',
            'stufenfrei_cod_2022': 'Stufenfreiheit',
            'fia_cod_2022': 'Fahrgastinformationsanlagen',
            'akustik_cod_2022': 'Lautsprecher_DSA_Akustikmodul',
            'bstgtakleitsys_cod_2022': 'Taktiles_Leitsystem_auf_dem_Bstg',
            'takbereichbstg_cod_2022': 'Taktiler_Weg_vom_öffentlichen_Bereich_zum_Bstg',
            'stufmark_cod_2022': 'Stufenmarkierung_an_Treppen',
            'takhandlauf_cod_2022': 'Taktile_Handlaufschilder_Treppen_und_Rampen',
            'weitreichend_barrierefrei_2022': 'Weitreichend barrierefreie Bahnhöfe',
            'stufenfrei_cod_21_22': 'Stufenfreiheit',
            'fia_cod_21_22': 'Fahrgastinformationsanlagen',
            'akustik_cod_21_22': 'Lautsprecher_DSA_Akustikmodul',
            'bstgtakleitsys_cod_21_22': 'Taktiles_Leitsystem_auf_dem_Bstg',
            'takbereichbstg_cod_21_22':'Taktiler_Weg_vom_öffentlichen_Bereich_zum_Bstg',
            'stufmark_cod_21_22':'Stufenmarkierung_an_Treppen', 
            'takhandlauf_cod_21_22':'Taktile_Handlaufschilder_Treppen_und_Rampen',
            'weitreichend_barrierefrei_21_22':'Weitreichend barrierefreie Bahnhöfe', 
            
        },
        '2021': {
            'Anzahl_Bahnsteige_2021': 'Anzahl der Bahnsteige',
            'Verkehrsstation_2021': 'Anzahl Verkehrsstation',
            'Aufzüge_2021': 'Anzahl Aufzüge',
            'Fahrtreppen_2021': 'Anzahl Fahrtreppen',
            'Rampen_2021': 'Anzahl Rampen',
            'stufenfrei_cod_2021': 'Stufenfreiheit',
            'fia_cod_2021': 'Fahrgastinformationsanlagen',
            'akustik_cod_2021': 'Lautsprecher_DSA_Akustikmodul',
            'bstgtakleitsys_cod_2021': 'Taktiles_Leitsystem_auf_dem_Bstg',
            'takbereichbstg_cod_2021': 'Taktiler_Weg_vom_öffentlichen_Bereich_zum_Bstg',
            'stufmark_cod_2021': 'Stufenmarkierung_an_Treppen',
            'takhandlauf_cod_2021': 'Taktile_Handlaufschilder_Treppen_und_Rampen',
            'weitreichend_barrierefrei_2021': 'Weitreichend barrierefreie Bahnhöfe',
            'stufenfrei_cod_21_22': 'Stufenfreiheit',
            'fia_cod_21_22': 'Fahrgastinformationsanlagen',
            'akustik_cod_21_22': 'Lautsprecher_DSA_Akustikmodul',
            'bstgtakleitsys_cod_21_22': 'Taktiles_Leitsystem_auf_dem_Bstg',
            'takbereichbstg_cod_21_22':'Taktiler_Weg_vom_öffentlichen_Bereich_zum_Bstg',
            'stufmark_cod_21_22':'Stufenmarkierung_an_Treppen', 
            'takhandlauf_cod_21_22':'Taktile_Handlaufschilder_Treppen_und_Rampen',
            'weitreichend_barrierefrei_21_22':'Weitreichend barrierefreie Bahnhöfe COD', 
            
        }
    }
    
    accessability_cards = {}
    Anzahl_sums = {}  # Dictionary to store sums for "Anzahl" related columns

    for year, columns in year_specific_columns.items():
        
        if year_filter == year:
            
            for column, title in columns.items():
                
                if "Anzahl" in title:  # Check if the title is related to "Anzahl"
                    # Sum the values for this column and store in Anzahl_sums
                    Anzahl_sums[title] = data.aggregate(Sum(column))[f'{column}__sum']
                
                else:
                    # logic for counts based on conditions
                    counts = data.aggregate(
                        keine=Count(Case(When(**{column: "Weniger"}, then=1), output_field=IntegerField())),
                        alle=Count(Case(When(**{column: "Mehr"}, then=1), output_field=IntegerField())),
                        manche=Count(Case(When(**{column: "Unverändert"}, then=1), output_field=IntegerField())),
                    )
                    
                    accessability_cards[title] = counts

    
    api_cards = get_api_cards(data)
    
    #definiert in functions.py    
    plot_html = show_plot(data, mapbox_access_token, show_geo_plot, 'pb')
    
    context = {
        'page_obj': page_obj, 
        'anzahl': anzahl,
        'field_names': field_names,
        'year_filter': year_filter,
        'filter': filter,
        'accessability_cards': accessability_cards,
        'plot_html': plot_html,
        'show_geo_plot': show_geo_plot,
        'api_cards': api_cards,
        'missing_2021': missing_2021,
        'missing_2022': missing_2022,

    }

    return render(request, 'myapp/personenbahn.html', context)

def station_detail(request, station_number):
    # Fetch the stationen_ISK_2022 object based on Bf_NR
    #station_number wird aus der URL genommen
    station = get_object_or_404(stationen_ISK_2022, Bf_NR=station_number)

    #definiert in functions.py  
    plot_html = generate_plotly_pb_details(station_number, mapbox_access_token)


    context={
        'station': station, 
        'plot_html': plot_html
        
    }

    return render(request, 'myapp/pb_detail.html', context)

def analysis_startseite(request):
    return render(request, 'myapp/analysis_startseite.html')

def streckeninfo(request):

    #Filter auf HTML Seite
    filters = GSLFilter(request.GET, queryset=GSL_grouped_ISK_2022.objects.all())
    gsllist = filters.qs

    #Download Buttons
    #Logik muss angepasst werden. Aktuell wird komplette Tabelle exportiert ohne Anwendung von Filtern
    if 'download-csv' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="filtered_data.csv"'

        writer = csv.writer(response)
        fields = [field for field in GSL_grouped_ISK_2022._meta.get_fields() if field.concrete]
        writer.writerow([field.name for field in fields])

        for obj in gsllist:
            writer.writerow([getattr(obj, field.name) for field in fields])

        return response

    if 'download-excel' in request.GET:
        df = pd.DataFrame(list(gsllist.values(*[field.name for field in GSL_grouped_ISK_2022._meta.get_fields() if field.concrete])))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="filtered_data.xlsx"'
        df.to_excel(response, index=False)

        return response
        
    #Code für Plotly
    all_bridges = bruecken_ISK_2022.objects.filter(gsl_grouped_isk_2022__in=gsllist).distinct()
    all_strecken = gsllist
    all_bahnuebergaenge =  bahnuebergaenge_ISK_2022.objects.filter(gsl_grouped_isk_2022__in=gsllist).distinct()
    all_weichen = weichen_ISK_2022.objects.filter(gsl_grouped_isk_2022__in=gsllist).distinct()
    all_tunnel = tunnel_ISK_2022.objects.filter(gsl_grouped_isk_2022__in=gsllist).distinct()
 
    #Umwandlung in pd.DataFrames
    #Anders für Tunnel und Strecken da Multilinestrings
    df_all_strecken = pd.DataFrame(all_strecken.values())
    print("huhu", df_all_strecken)


    if 'geometry' in df_all_strecken.columns:
        # The column exists, so proceed with the operation
        print('99')
        valid_geometries_strecke = df_all_strecken['geometry'].apply(lambda x: isinstance(x, str) and x.strip().upper() not in ['', 'NONE'])
    else:
        # Column does not exist - handle gracefully
        # Option 1: Log a warning or print a message
        print("Warning: 'geometry' column not found in the DataFrame.")
        valid_geometries_strecke = pd.Series()
    df_all_strecken = df_all_strecken[valid_geometries_strecke]
    try:
        df_all_strecken["geometry"] = df_all_strecken["geometry"].apply(wkt.loads)
        print('98')
    except KeyError:
        print('97')

        df_all_strecken = pd.DataFrame(columns = list(df_all_strecken.columns))


    print(df_all_strecken)


    
    df_all_bahnuebergaenge = pd.DataFrame(all_bahnuebergaenge.values())

    df_all_weichen = pd.DataFrame(all_weichen.values())
    
    df_all_tunnel = pd.DataFrame(all_tunnel.values())
    try:

        df_all_tunnel["geometry"] = df_all_tunnel["geometry"].apply(wkt.loads)
    except KeyError:
        df_all_tunnel = pd.DataFrame(columns = list(df_all_tunnel.columns))


    
    

    #print(df_all_strecken)

    try:
        hover_text_bu = df_all_bahnuebergaenge.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>LAGE_KM: {row['LAGE_KM']}", axis=1) #STR_NR
            
        # Für Brücken (df_br_new)
        hover_text_br = [
            f"LAND: {bridge.LAND}<br>EIU: {bridge.EIU}<br>REGION: {bridge.REGION}<br>NETZ: {bridge.NETZ}<br>"
            f"ANLAGEN_NR: {bridge.ANLAGEN_NR}<br>ANLAGEN_UNR: {bridge.ANLAGEN_UNR}<br>"
            f"VON_KM: {bridge.VON_KM}<br>BIS_KM: {bridge.BIS_KM}<br>VON_KM_I: {bridge.VON_KM_I}<br>"
            f"BIS_KM_I: {bridge.BIS_KM_I}<br>RIKZ: {bridge.RIKZ}<br>RIL_100: {bridge.RIL_100}<br>"
            f"STR_MEHRFACHZUORD: {bridge.STR_MEHRFACHZUORD}<br>FLAECHE: {bridge.FLAECHE}<br>"
            f"BR_BEZ: {bridge.BR_BEZ}<br>BAUART: {bridge.BAUART}<br>BESCHREIBUNG: {bridge.BESCHREIBUNG}<br>"
            f"ZUST_KAT: {bridge.ZUST_KAT}<br>WL_SERVICEEINR: {bridge.WL_SERVICEEINR}<br>Match: {bridge.Match}"
            for bridge in all_bridges
        ]


        # Für Tunnel (df_tu_new)
        hover_text_tu = df_all_tunnel.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>VON_KM: {row['VON_KM']}<br>BIS_KM: {row['BIS_KM']}<br>LAENGE: {row['LAENGE']}<br>BAUWEISE: {row['BAUWEISE']}", axis=1)

        hover_text_strecke = df_all_strecken.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>STR_NR: {row['STR_NR']}<br>VON_KM: {row['VON_KM']}<br>BIS_KM: {row['BIS_KM']}<br>LAENGE: {row['LAENGE']}", axis=1)

        hover_text_weiche = df_all_weichen.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>LAGE_KM: {row['LAGE_KM']}", axis=1) #STR_NR



        fig = go.Figure()


        # Datainklusion Strecke
        lons_str = []
        lats_str = []
        hover_texts_str = []
        
        #Berechnung der Koordinaten
        for index, row in df_all_strecken.iterrows():
            geom_str = (row['geometry'])
            
            # Check if the geometry is a LineString
            if isinstance(geom_str, LineString):
                xs, ys = geom_str.xy
                lons_str.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                lats_str.extend(ys.tolist() + [None])
            # Check if the geometry is a MultiLineString
            elif isinstance(geom_str, MultiLineString):
                print("test")
                for line in geom_str.geoms:  # Use .geoms to iterate over each LineString
                    xs, ys = line.xy
                    lons_str.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                    lats_str.extend(ys.tolist() + [None])
                
               
            # Add hover text for each segment - this needs adjustment to prevent reference errors
            if 'xs' in locals():
                hover_texts_str.extend(hover_text_strecke)
            
        print("1")
        #Zeichnen der Strecken
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=lons_str,
            lat=lats_str,
            hovertext=hover_texts_str,
            hoverinfo="text",
            line=dict(color='#edb7ea', width=3),
            name='Strecke',
            showlegend=True,
        ))
        # Datainklusion Brücken
        print("2")
        fig.add_trace(go.Scattermapbox(
            lat=[bridge.GEOGR_BREITE for bridge in all_bridges if bridge.GEOGR_BREITE is not None],
            lon = [bridge.GEOGR_LAENGE for bridge in all_bridges if bridge.GEOGR_LAENGE is not None],
            mode='markers',
            marker=dict(size=7, color='#006587'),
            hoverinfo='text',
            hovertext=hover_text_br,
            name='Brücken',
            showlegend=True,
        ))

        print("3")
        #Bahnübergänge
        try:
            fig.add_trace(go.Scattermapbox(
                lat=df_all_bahnuebergaenge['breite'],
                lon=df_all_bahnuebergaenge['laenge'],
                mode='markers',
                marker=dict(size=7, color='#68DAFF'),
                hoverinfo='text',
                hovertext=hover_text_bu,
                name='Bahnübergänge',
                showlegend=True,
            ))
        except KeyError as e:
            print(f"KeyError: Missing expected column - {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        print("4")
        #Weichen
        fig.add_trace(go.Scattermapbox(
            lat=df_all_weichen['lat'],
            lon=df_all_weichen['lon'],
            mode='markers',
            marker=dict(size=7, color='#eb3f3f'),
            hoverinfo='text',
            hovertext=hover_text_weiche,
            name='Weiche',
            showlegend=True,
        ))
        print("5")
        #Tunnel
        lons = []
        lats = []
        hover_texts = []

        #Berechnung der Koordinaten
        for index, row in df_all_tunnel.iterrows():
            geom = row['geometry']
            # Check if the geometry is a LineString
            if isinstance(geom, LineString):
                xs, ys = geom.xy
                lons.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                lats.extend(ys.tolist() + [None])
            # Check if the geometry is a MultiLineString
            elif isinstance(geom, MultiLineString):
                for line in geom.geoms:  # Use .geoms to iterate over each LineString
                    xs, ys = line.xy
                    lons.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                    lats.extend(ys.tolist() + [None])
            # Add hover text for each segment - this needs adjustment to prevent reference errors
            if 'xs' in locals():
                hover_texts.extend(hover_text_tu)

        print("6")
        # Add a single trace for all tunnel line segments
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=lons,
            lat=lats,
            hovertext=hover_texts,
            hoverinfo="text",
            line=dict(color='#5496B8', width=7),
            name='Tunnel',  
            showlegend=True,
        ))


        print("7")
        try:
            # Calculate the mean of the latitudes and longitudes
            lats_series = pd.Series(lats)
            lons_series = pd.Series(lons)
            
            lons_series_str = pd.Series(lons_str)
            lats_series_str = pd.Series(lats_str)
            
            # Now, concatenate using pandas Series
            all_longitudes = pd.concat([lons_series_str, lons_series, df_all_bahnuebergaenge['laenge']])
            all_latitudes = pd.concat([lats_series_str, lats_series, df_all_bahnuebergaenge['breite']])

            lat1 = np.mean(all_latitudes)
            lon1 = np.mean(all_longitudes)
            # Continue with updating the layout and showing the figure as before
        
            fig.update_layout(
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    center={"lat": lat1, "lon": lon1},
                    zoom=5.5,
                    style='outdoors'
                ),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99
                ),
                title="Geoplot Strecken, Weichen, Bahnübergänge, Brücken und Tunnel",
                title_font=dict(color='#003366', size=24),
                title_x=0.5,
                margin=dict(b=40),
            )
        except:
            # Calculate the mean of the latitudes and longitudes
            

            lat1 = 51
            lon1 = 10
            # Continue with updating the layout and showing the figure as before

            fig.update_layout(
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    center={"lat": 51, "lon": 10},
                    zoom=5.5,
                    style='outdoors'
                ),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99
                ),
                title="Geoplot Strecken, Weichen, Bahnübergänge, Brücken und Tunnel",
                title_font=dict(color='#003366', size=24),
                title_x=0.5,
                margin=dict(b=40),
            )
        print("8")
        fig.update_layout(
        mapbox=dict(
        accesstoken=mapbox_access_token,
        center={"lat": lat1, "lon": lon1},
        zoom=9.0,
        style='outdoors'
        ),
        legend=dict(
        font=dict(
            size=20  
        )
        ),
  
        # Title-Bezeichnung
        
        showlegend=True,
        title_text="",
        title_font=dict(size=24, color="#003366"),
        title_pad=dict(t=20, b=20),
        
        # Dropdown für Map-Ansicht
        updatemenus=[dict(
        buttons=[
            dict(args=[{"mapbox.style": "outdoors"}],
                label="Outdoors",
                method="relayout"),
            dict(args=[{"mapbox.style": "satellite"}],
                label="Satellite",
                method="relayout"),
            dict(args=[{"mapbox.style": "light"}],
                label="Hell",
                method="relayout"),
            dict(args=[{"mapbox.style": "dark"}],
                label="Dunkel",
                method="relayout"),
            dict(args=[{"mapbox.style": "streets"}],
                label="Straße",
                method="relayout"),
            dict(args=[{"mapbox.style": "satellite-streets"}],
                label="Satellite mit Straßen",
                method="relayout"),
        ],
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=1,
        xanchor="right",
        y=1.1,
        yanchor="top",
        bgcolor="#001C4F",
        font=dict(size=15, color="white")  
        )]
        )

        fig.update_layout(height=800)
        
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
    except KeyError as error:
        print(error)
        no_data_message = "Für diese Streckennummer ist keine Geo-Visualisierung verfügbar."
        plot_html = mark_safe(f"<div style='text-align: center; padding: 20px;'>{no_data_message}</div>")



    paginator = Paginator(gsllist, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

     # Retrieve the list of columns to exclude from the request
    exclude_columns = ['geometry']



    # Filter out the excluded columns
    fields = [field for field in GSL_grouped_ISK_2022._meta.get_fields() if field.concrete and field.name not in exclude_columns]


    context = {
        'page_obj': page_obj,
        'fields': fields,
        'filters': filters,
        'plot_html': plot_html,
        'query_string': request.GET.urlencode(),
        
    }


    return render(request, 'myapp/streckeninfo.html', context)






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
    'Nordrhein-Westfalen':'NW',
    'Keine Zuordnung':'nan',
}

def anlagen_view(request, anlage_type):
    #Funktion für das Berechnen der Daten für alle Anlagentypen
    #Der Anlagentyp wird der URL entnommen

    #Checkbox um Geoplot anzuzeigen
    show_geo_plot = 'show_geo_plot' in request.POST
    
    #Model map für Anlagentyp dazugehörige Model und Filter
    model_map = {
        'weichen': (weichen_ISK_2022, WeichenFilter),
        'tunnel': (tunnel_ISK_2022, TunnelFilter),
        'bahnuebergaenge': (bahnuebergaenge_ISK_2022, BahnuebergaengeFilter),
        'bruecken': (bruecken_ISK_2022, BrueckenFilter),
        'stuetzbauwerke': (stuetzauwerke_ISK_2022, StuetzbauwerkeFilter),
        'schallschutzwaende': (schallschutzwaende_ISK_2022, SchallschutzwaendeFilter)
    }

    #Auswahl Model und Filter nach Anlagentyp
    model, filter_class = model_map.get(anlage_type.lower(), (None, None))

    #if model agiert als "Callback"
    if model:
        filter_input = request.GET
        filter = filter_class(filter_input, queryset=model.objects.all())
        #Fügt die Spalte STR_NR hinzu
        data = filter.qs.annotate(STR_NR=F('gsl_grouped_isk_2022__STR_NR'))

        paginator = Paginator(data, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        plot_html = show_plot(data, mapbox_access_token, show_geo_plot, 'anlagen', anlage_type)


        field_exclusion = {
            'tunnel': ['geometry', 'STR_MEHRFACHZUORD', 'Matching'], 
            'bahnuebergaenge': ['lat', 'lon', 'Abs_Dif_cm', 'UEB_WACH_ART', 'ANLAGEN_NR_LST'], 
            'bruecken': ['lat', 'lon', 'Match', 'STR_MEHRFACHZUORD', 'WL_SERVICEEINR', 'ANLAGEN_UNR', 'VON_KM_I', 'BIS_KM_I', 'RIKZ', 'GEOGR_BREITE','GEOGR_LAENGE'],
            'schallschutzwaende': ['VON_KM_I', 'BIS_KM_I',]
            }
        
        field_names = ['STR_NR'] + [field.name for field in model._meta.fields if not field.is_relation and not field.name.startswith('_') and field.name not in field_exclusion.get(anlage_type.lower(), []) and field.name != 'gsl_grouped_isk_2022']

        #definiert in functions.py
        #zur Erstellung der Karten 'Anzahl und Länge/Fläche' und 'Deteils pro Bundesland'
        gesamt_anzahl, gesamt_flaeche, gesamt_laenge, aggregation_per_state = calculate_sums_and_counts(anlage_type, data)

        #Downloads
        download_format = request.GET.get('format', None)

        if download_format == 'csv':
            # Create HttpResponse object for downloading text/csv content
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="{anlage_type}_data.csv"'

            # Add UTF-8 BOM to the start of the file
            response.write(u'\ufeff'.encode('utf8'))

            # Create a csv.writer object to write to the response object
            writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Writing the header
            writer.writerow(field_names)

            # Writing the data rows
            for item in data.values(*field_names):
                writer.writerow([str(item[field]) if item[field] is not None else '' for field in field_names])

            return response

        elif download_format == 'excel':
            # Set the response headers and content type
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{anlage_type}_data.xlsx"'

            # Convert the QuerySet to a DataFrame
            df = pd.DataFrame(list(data.values(*field_names)))

            # Create an Excel writer using Pandas
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')

            

            return response

        context = {
            'filter': filter,
            'page_obj': page_obj,
            'anlage_type': anlage_type,
            'field_names': field_names,
            'query_string': filter_input.urlencode(),
            'aggregation_per_state': aggregation_per_state,
            'gesamt_anzahl': gesamt_anzahl,
            'gesamt_laenge': gesamt_laenge,
            'gesamt_flaeche': gesamt_flaeche,
            'plot_html': plot_html,
            'show_geo_plot': show_geo_plot
        }

        return render(request, 'myapp/anlagen_table.html', context)




def etcs_view(request):

    data = ETCS_2022.objects.all()

    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    fields = get_fields(ETCS_2022, [], False)

    context = {
            'page_obj': page_obj,
            'fields': fields,
    }
    return render(request, 'myapp/etcs.html', context)

def elektr_view(request):
#Filter, dass nur Strecken mit Richtung == 1 ausgewählt werden
    initial_queryset = SML_ISK_2022.objects.filter(RI=1)

    #Filter auf HTML Seite
    filters = SMLFilter(request.GET, queryset=initial_queryset)
    data = filters.qs

    aggregated_data = data.aggregate(
        total_km=Coalesce(Sum('LAENGE') / 1000, 0, output_field=IntegerField()),
        total_segments=Count('gsl_grouped_isk_2022_id'),
        elektr_km=Coalesce(Sum(Case(When(ELEKTR='O', then='LAENGE'), output_field=IntegerField())) / 1000, 0, output_field=IntegerField()),
        elektr_segments=Count(Case(When(ELEKTR='O', then=1), output_field=IntegerField())),
        nicht_elektr_km=Coalesce(Sum(Case(When(ELEKTR='n.e.', then='LAENGE'), output_field=IntegerField())) / 1000, 0, output_field=IntegerField()),
        nicht_elektr_segments=Count(Case(When(ELEKTR='n.e.', then=1), output_field=IntegerField()))
    )

    #Teilt data in einzelne Seiten
    paginator = Paginator(data, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #definiert in funtions.py
    #holt alle field names von SML_ISK_2022 außer ['ID', 'RI']
    #wenn True, wird STR_NR als erste Spalte gezeigt
    fields = get_fields(SML_ISK_2022, ['ID', 'RI'], False)

    
    
    context = {
        'filters': filters,
        'page_obj': page_obj,
        'fields': fields,
        'aggregated_data': aggregated_data,
    }
    return render(request, 'myapp/elektr.html', context)


# view für Passwort Eingabe
def password_protect(request):
    if request.method == 'POST':
        if request.POST.get('password') == settings.SIMPLE_PASSWORD:
            request.session['password'] = settings.SIMPLE_PASSWORD
            return redirect('myapp:main_view')  # Weiterleitung zur Hauptseite
        else:
            return render(request, 'myapp/password.html', {'error': 'Falsches Passwort'})

    return render(request, 'myapp/password.html')

