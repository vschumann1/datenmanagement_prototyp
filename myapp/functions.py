import pandas as pd
import plotly.graph_objects as go
from shapely.geometry import LineString, MultiLineString
from shapely import wkt
from .models import GSL_grouped_ISK_2022, bruecken_ISK_2022, tunnel_ISK_2022, weichen_ISK_2022, stuetzauwerke_ISK_2022, schallschutzwaende_ISK_2022, bahnuebergaenge_ISK_2022, stationen_ISK_2022, bahnsteige_ISK_2022, df_change_vst_sts_2022, SML_ISK_2022
from django.db.models.functions import Cast
from django.db.models import IntegerField, Sum, Count, CharField
from django.http import HttpResponse
from django.db.models import Sum, Count, Case, When, IntegerField, FloatField, ExpressionWrapper, Value
import json
from django_pandas.io import read_frame

def generate_plot_html(data, anlage_type, mapbox_access_token):

    
    gsl_grouped_isk_2022_ids = data.values_list('gsl_grouped_isk_2022_id', flat=True).distinct()

    
    strecken_data = GSL_grouped_ISK_2022.objects.filter(STR_NR__in=gsl_grouped_isk_2022_ids)
   

    
    

    plotly_data = pd.DataFrame(data.values())

    if anlage_type == 'bahnuebergaenge':
        hover_text = plotly_data.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>STR_NR: {row['gsl_grouped_isk_2022_id']}<br>LAGE_KM: {row['LAGE_KM']}", axis=1) # <br>BAUFORM: {row['BAUFORM']}", axis=1)
        anlage_name = 'Bahnübergänge'
    elif anlage_type == 'weichen':
        hover_text = plotly_data.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>STR_NR: {row['gsl_grouped_isk_2022_id']}<br>LAGE_KM: {row['LAGE_KM']}", axis=1)
        anlage_name = 'Weichen'
    elif anlage_type == 'bruecken':
        hover_text = plotly_data.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>STR_NR: {row['gsl_grouped_isk_2022_id']}<br>VON_KM: {row['VON_KM']}<br>BIS_KM: {row['BIS_KM']}<br>BAUART: {row['BAUART']}<br>ZUST_KAT: {row['ZUST_KAT']}", axis=1)
        anlage_name = 'Brücken'
    

    


    # Für Brücken (df_br_new)

    # Für Tunnel (df_tu_new)


    
    

    plotly_strecken_data = pd.DataFrame(strecken_data.values())
    
    
    
    if 'geometry' in plotly_strecken_data.columns:
        # The column exists, so proceed with the operation
        valid_geometries_strecke = plotly_strecken_data['geometry'].apply(lambda x: isinstance(x, str) and x.strip().upper() not in ['', 'NONE'])
    else:
        # Column does not exist - handle gracefully
        # Option 1: Log a warning or print a message
        print("Warning: 'geometry' column not found in the DataFrame.")
        valid_geometries_strecke = pd.Series()
    plotly_strecken_data = plotly_strecken_data[valid_geometries_strecke]
    try:
        plotly_strecken_data["geometry"] = plotly_strecken_data["geometry"].apply(wkt.loads)
    except KeyError:


        plotly_strecken_data = pd.DataFrame(columns = list(plotly_strecken_data.columns))

    hover_text_strecke = plotly_strecken_data.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>STR_NR: {row['STR_NR']}<br>VON_KM: {row['VON_KM']}<br>BIS_KM: {row['BIS_KM']}<br>LAENGE: {row['LAENGE']}", axis=1)
    
    
    fig = go.Figure()
    lons_str = []
    lats_str = []
    hover_texts_str = []

    for index, row in plotly_strecken_data.iterrows():
        geom_str = (row['geometry'])
        
        # Check if the geometry is a LineString
        if isinstance(geom_str, LineString):
            xs, ys = geom_str.xy
            lons_str.extend(xs.tolist() + [None])  # Add None at the end of each linestring
            lats_str.extend(ys.tolist() + [None])
        # Check if the geometry is a MultiLineString
        elif isinstance(geom_str, MultiLineString):
            
            for line in geom_str.geoms:  # Use .geoms to iterate over each LineString
                xs, ys = line.xy
                lons_str.extend(xs.tolist() + [None])  # Add None at the end of each linestring
                lats_str.extend(ys.tolist() + [None])
                hover_texts_str.extend([hover_text_strecke[index]] * len(xs) + [None])
                
               
        # Add hover text for each segment - this needs adjustment to prevent reference errors
        
            
       
        
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
   
    if anlage_type == 'tunnel':
        if 'geometry' in plotly_data.columns:
        # The column exists, so proceed with the operation
            valid_geometries = plotly_data['geometry'].apply(lambda x: isinstance(x, str) and x.strip().upper() not in ['', 'NONE'])
        else:
            # Column does not exist - handle gracefully
            # Option 1: Log a warning or print a message
            print("Warning: 'geometry' column not found in the DataFrame.")
            valid_geometries = pd.Series()
        plotly_data = plotly_data[valid_geometries]


        try:
            plotly_data["geometry"] = plotly_data["geometry"].apply(wkt.loads)
        except Exception as e:
            print(plotly_strecken_data.columns)

            plotly_data = pd.DataFrame(columns = list(plotly_data.columns))

      

        
        hover_text_tu = plotly_data.apply(lambda row: f"REGION: {row['REGION']}<br>NETZ: {row['NETZ']}<br>STR_NR: {row['gsl_grouped_isk_2022_id']}<br>VON_KM: {row['VON_KM']}<br>BIS_KM: {row['BIS_KM']}<br>LAENGE: {row['LAENGE']}<br>BAUWEISE: {row['BAUWEISE']}", axis=1)


        

        lons = []
        lats = []
        hover_texts = []


        for index, row in plotly_data.iterrows():
            geom = row['geometry']
             
           
            if isinstance(geom, LineString):
                xs, ys = geom.xy
            
                lons.extend(xs.tolist() + [None])  
                lats.extend(ys.tolist() + [None])
            
            elif isinstance(geom, MultiLineString):
                for line in geom.geoms:  
                    xs, ys = line.xy
                    lons.extend(xs.tolist() + [None])
                    lats.extend(ys.tolist() + [None])
                    hover_texts.extend([hover_text_tu[index]] * len(xs) + [None])
            
           
        

        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=lons,
            lat=lats,
            hovertext=hover_texts,
            hoverinfo="text",
            line=dict(color='#003366', width=7),
            name='Tunnel',  
            showlegend=True,
        ))

    else:
        
        
        fig.add_trace(go.Scattermapbox(
            lat=plotly_data['lat'],
            lon=plotly_data['lon'],
            mode='markers',
            marker=dict(size=7, color='#003366'),
            hoverinfo='text',
            hovertext=hover_text,
            name= anlage_name,
            showlegend=True,
        ))
    
    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            zoom=5.0,
            style='outdoors',
            center=dict(lat=51.1657, lon=10.4515)  
        ),
        legend=dict(
            font=dict(
                size=20
            ),
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        showlegend=True,
        margin=dict(b=40),
        height=800
    )

    

    
    fig.update_layout(
        updatemenus=[dict(
            buttons=[
                dict(args=[{"mapbox.style": "outdoors"}], label="Outdoors", method="relayout"),
                dict(args=[{"mapbox.style": "satellite"}], label="Satellite", method="relayout"),
                dict(args=[{"mapbox.style": "light"}], label="Hell", method="relayout"),
                dict(args=[{"mapbox.style": "dark"}], label="Dunkel", method="relayout"),
                dict(args=[{"mapbox.style": "streets"}], label="Straße", method="relayout"),
                dict(args=[{"mapbox.style": "satellite-streets"}], label="Satellite mit Straßen", method="relayout"),
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

    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return plot_html




def calculate_sums_and_counts(anlage_type, data):

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
    # Reverse the STATE_ABBREVIATIONS dictionary for easy lookup
    STATE_NAMES = {v: k for k, v in STATE_ABBREVIATIONS.items()}

    # Conditional aggregation for LAENGE and FLAECHE
    laenge_field = 'LAENGE' if anlage_type.lower() in ['tunnel', 'schallschutzwaende', 'stuetzbauwerke'] else None
    flaeche_field = 'FLAECHE' if anlage_type.lower() == 'bruecken' else None
        
    if anlage_type != 'tunnel':
        aggregation_annotations = {
            'anzahl': Count('gsl_grouped_isk_2022_id'),
            'gesamt_laenge': Sum(laenge_field) / 1000 if laenge_field else None,  # Convert length to kilometers
            'gesamt_flaeche': Cast(Sum(flaeche_field), IntegerField()) if flaeche_field else None  # Sum up the area
        }
    else:
        aggregation_annotations = {
            'anzahl': Count('gsl_grouped_isk_2022_id'),
            'gesamt_laenge': Sum(laenge_field) if laenge_field else None,  # Convert length to kilometers
            'gesamt_flaeche': Cast(Sum(flaeche_field), IntegerField()) if flaeche_field else None  # Sum up the area
        }
        # Filter out None values from aggregation_annotations
    aggregation_annotations = {k: v for k, v in aggregation_annotations.items() if v is not None}

    aggregation_per_state = data.values('LAND').annotate(**aggregation_annotations).order_by('LAND')

    for state in aggregation_per_state:
        state['LAND'] = STATE_NAMES.get(state['LAND'], state['LAND'])  # Replace abbreviations with full names

    gesamt_anzahl = data.count()
    if anlage_type != 'tunnel':
        gesamt_laenge = int(data.aggregate(Sum(laenge_field))['LAENGE__sum'] / 1000) if laenge_field and data.aggregate(Sum(laenge_field))['LAENGE__sum'] is not None else 0
    else:
        gesamt_laenge = int(data.aggregate(Sum(laenge_field))['LAENGE__sum']) if laenge_field and data.aggregate(Sum(laenge_field))['LAENGE__sum'] is not None else 0

    
    
    gesamt_flaeche = int(data.aggregate(Sum(flaeche_field))['FLAECHE__sum']) if flaeche_field and data.aggregate(Sum(flaeche_field))['FLAECHE__sum'] is not None else 0

    return gesamt_anzahl, gesamt_flaeche, gesamt_laenge, aggregation_per_state


def safe_unpacking(func, expected_length=4):
    # Call the function
    result = func()
    # Ensure result is a tuple
    result = result if isinstance(result, tuple) else (result,)
    # Pad the result with None values if it's shorter than expected
    padded_result = result + (None,) * (expected_length - len(result))
    return padded_result

def get_fields(model, exclude_columns = [], str_first = False):
    fields = [field for field in model._meta.get_fields() if field.concrete and field.name not in exclude_columns]
    if str_first:
        
        if 'STR_NR' not in fields:
            fields.insert(0, 'STR_NR')  # Add 'STR_NR' as the first field if it's not already in the list
        else:
            fields.remove('STR_NR')  # Remove 'STR_NR' if it's already in the list
            fields.insert(0, 'STR_NR')
        
    return fields

def get_field_names(df_change_vst_sts_2022, stationen_ISK_2022, request, year_filter, include_api_fields = False):

    field_names_stationen_ISK_2022 = [field.name for field in stationen_ISK_2022._meta.fields]

    

    # Always include these default fields
    default_fields = [
        'Anzahl_Bahnsteige_x',
        'Reisende_je_Tag_und_Station_2019',
        'Land',
        'Regionalbereich',
        'Bahnhofsmanagement',
        'Ril_100',
        'ID'
    ]

    # Add fields based on the selected year
    if year_filter == '2022':
        year_specific_fields = [f.name for f in df_change_vst_sts_2022._meta.get_fields() if '2022' in f.name]
    elif year_filter == '2021':
        year_specific_fields = [f.name for f in df_change_vst_sts_2022._meta.get_fields() if '2021' in f.name]
    else:
        year_specific_fields = []

    if include_api_fields:
        field_names = default_fields + year_specific_fields + field_names_stationen_ISK_2022
    else:
        field_names = default_fields + year_specific_fields


    return field_names, year_filter

def prepare_accessability_cards(data, year_filter):
    # Define your base and year-specific columns here, possibly load from a config for flexibility
    base_columns = {
        'stufenfrei_cod_21_22': ('Stufenfreiheit'),
        'fia_cod_21_22': ('Fahrgastinformationsanlagen'),
        'akustik_cod_21_22': ('Lautsprecher_DSA_Akustikmodul'),
        'bstgtakleitsys_cod_21_22': ('Taktiles_Leitsystem_auf_dem_Bstg'),
        'takbereichbstg_cod_21_22':('Taktiler_Weg_vom_öffentlichen_Bereich_zum_Bstg'),
        'stufmark_cod_21_22':('Stufenmarkierung_an_Treppen'), 
        'takhandlauf_cod_21_22':('Taktile_Handlaufschilder_Treppen_und_Rampen'),
        'weitreichend_barrierefrei_21_22':('Weitreichend barrierefreie Bahnhöfe'), 
        #'Anzahl_Bahnsteige_21_22':'Bahnsteige',
        #'Aufzüge_21_22':'Aufzüge', 
        #'Fahrtreppen_21_22':'Fahttreppen', 
        #'Rampen_21_22':'Rampen', 
        #'Vst_21_22':'Verkehrstationen'
        # Add other columns as needed
    }

    # Year-specific columns to include based on the year filter with their specific value sets
    year_specific_columns = {
        '2022': {
            'stufenfrei_cod_2022': 'Stufenfreiheit',
            'fia_cod_2022': 'Fahrgastinformationsanlagen',
            'akustik_cod_2022': 'Lautsprecher_DSA_Akustikmodul',
            'bstgtakleitsys_cod_2022': 'Taktiles Leitsystem auf dem Bahnsteig',
            'takbereichbstg_cod_2022': 'Taktiler Weg vom öffentlichen Bereich zum Bahnsteig',
            'stufmark_cod_2022': 'Stufenmarkierung an Treppen',
            'takhandlauf_cod_2022': 'Taktile Handlaufschilder an Treppen und Rampen',
            'wls_cod_2022': 'Weitreichendes Leitsystem',
            'weitreichend_barrierefrei_2022': 'Weitreichend barrierefreie Bahnhöfe',
            # Include other 2022-specific fields as needed
        },
        '2021': {
            'Anzahl_Bahnsteige_2021': 'Anzahl der Bahnsteige',
            'Verkehrsstation_2021': 'Verkehrsstation',
            'Aufzüge_2021': 'Aufzüge',
            'Fahrtreppen_2021': 'Fahrtreppen',
            'Rampen_2021': 'Rampen',
            'stufenfrei_cod_2021': 'Stufenfreiheit',
            'fia_cod_2021': 'Fahrgastinformationsanlagen',
            'akustik_cod_2021': 'Akustik',
            'bstgtakleitsys_cod_2021': 'Taktiles Leitsystem auf dem Bahnsteig',
            'takbereichbstg_cod_2021': 'Taktiler Weg vom öffentlichen Bereich zum Bahnsteig',
            'stufmark_cod_2021': 'Stufenmarkierung an Treppen',
            'takhandlauf_cod_2021': 'Taktile Handlaufschilder an Treppen und Rampen',
            'wls_cod_2021': 'Weitreichendes Leitsystem',
            'weitreichend_barrierefrei_2021': 'Weitreichend barrierefreie Bahnhöfe',
            # Include other 2021-specific fields as needed
        }
    } # Include your dynamic handling here based on 'year_filter'

    cards = []

    # Handle base columns
    for column, title in base_columns.items():
        counts = data.aggregate(
            abgenommen=Count(Case(When(**{column: "Weniger"}, then=1), output_field=IntegerField())),
            zugenommen=Count(Case(When(**{column: "Mehr"}, then=1), output_field=IntegerField())),
            unverändert=Count(Case(When(**{column: "Unverändert"}, then=1), output_field=IntegerField())),
        )
        cards.append((title, counts))

    # Handle year-specific columns
    for column, title in year_specific_columns.get(year_filter, {}).items():
        counts = data.aggregate(
            nicht_vorhanden=Count(Case(When(**{column: 0}, then=1), output_field=IntegerField())),
            vorhanden=Count(Case(When(**{column: 1}, then=1), output_field=IntegerField())),
            teilweise_vorhanden=Count(Case(When(**{column: -98}, then=1), output_field=IntegerField())),
        )
        cards.append((title, counts))

    return cards



def get_coordinates(station_number):

    record = stationen_ISK_2022.objects.get(Bf_NR=station_number)
    coordinates = record.evaNumbers_geographicCoordinates
      # Temporarily add this to check the content of coordinates
    
    try:
        # Assuming coordinates is a flat list but might contain more than two values
        lat_lon_str = coordinates  # Replace 'your_data_source' with the actual source of your coordinates

        # Use json.loads to parse the string into an actual list
        lat_lon = json.loads(lat_lon_str)

        # Now, lat_lon is a list from which you can extract latitude and longitude as numbers
        longitude = lat_lon[0]
        latitude = lat_lon[1]  # This will unpack the first two elements, ignoring the rest
    except ValueError as e:
        # Log the error or print a message, so you can see what went wrong
        print(f"Error unpacking coordinates: {e}. Coordinates value: {coordinates}")
        raise  # Re-raise the exception to avoid silent failure

    name = record.name
    
    return latitude, longitude, name


def generate_plotly_pb_details(station_number, mapbox_access_token):
    
    lat, lon, name = get_coordinates(station_number)


    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
            lat= [lat],
            lon= [lon],
            mode='markers',
            marker=dict(size=20, color='#003366'),
            name= name,
            showlegend=True,
        ))

    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            zoom=10.0,
            style='outdoors',
            center=dict(lat=float(lat), lon=float(lon))  
        ),
        legend=dict(
            font=dict(
                size=20
            ),
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        showlegend=True,
        title=f"Geoplot: {name}",
        title_font=dict(color='#003366', size=24),
        title_x=0.5,
        margin=dict(b=40),
        height=800
    )

    

    
    fig.update_layout(
        updatemenus=[dict(
            buttons=[
                dict(args=[{"mapbox.style": "outdoors"}], label="Outdoors", method="relayout"),
                dict(args=[{"mapbox.style": "satellite"}], label="Satellite", method="relayout"),
                dict(args=[{"mapbox.style": "light"}], label="Hell", method="relayout"),
                dict(args=[{"mapbox.style": "dark"}], label="Dunkel", method="relayout"),
                dict(args=[{"mapbox.style": "streets"}], label="Straße", method="relayout"),
                dict(args=[{"mapbox.style": "satellite-streets"}], label="Satellite mit Straßen", method="relayout"),
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

    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return plot_html



def get_station_details(data_queryset):
    # Use the data_queryset to filter stationen_ISK_2022 based on related records in df_change_vst_sts_2022
    station_records = stationen_ISK_2022.objects.filter(
        Bf_NR__in=data_queryset.values('Bf_NR_id')
    ).values(
        'Bf_NR', 'name', 'evaNumbers_geographicCoordinates'
    ).distinct()

    # Convert query to DataFrame
    df_stations = pd.DataFrame.from_records(station_records)

    if 'evaNumbers_geographicCoordinates' not in df_stations.columns:
        print("No geographic coordinates available in the data.")
        return pd.DataFrame(columns=['Bf_NR', 'name', 'latitude', 'longitude'])

    # Define a function to process JSON coordinates
    def process_coordinates(row):
        coordinates = row['evaNumbers_geographicCoordinates']
        try:
            if coordinates:
                lat_lon = json.loads(coordinates)
                if len(lat_lon) == 2:
                    return pd.Series({'latitude': lat_lon[0], 'longitude': lat_lon[1]})
        except json.JSONDecodeError:
            print(f"Error decoding JSON for coordinates of Bf_NR {row['Bf_NR']}: {coordinates}")
        except Exception as e:
            print(f"Unexpected error for Bf_NR {row['Bf_NR']}: {e}")
        return pd.Series({'latitude': None, 'longitude': None})

    # Apply function to DataFrame
    df_coords = df_stations.apply(process_coordinates, axis=1)
    df_stations = pd.concat([df_stations.drop(columns=['evaNumbers_geographicCoordinates'], errors='ignore'), df_coords], axis=1)

    # Filter out rows where coordinates could not be parsed
    df_stations = df_stations.dropna(subset=['latitude', 'longitude'])

    return df_stations[['Bf_NR', 'name', 'latitude', 'longitude']]


    

'''def get_station_details(data_queryset):
    station_details = []

    for data_record in data_queryset:
        try:
            # Attempt to access the ForeignKey relationship
            station_id = data_record.Bf_NR_id  # Using _id to directly get the ForeignKey value
            #print(f"Processing station_id: {station_id}")  # Log the station_id being processed

            # Fetch the corresponding stationen_ISK_2022 record
            station_record = stationen_ISK_2022.objects.get(Bf_NR=station_id)

            # Proceed if station_record is successfully fetched
            name = station_record.name
            coordinates = station_record.evaNumbers_geographicCoordinates
            
            # Check if coordinates is non-empty and a valid JSON string
            if coordinates:
                lat_lon = json.loads(coordinates)
                if len(lat_lon) == 2:
                    latitude, longitude = lat_lon
                else:
                    print(f"Unexpected number of elements in coordinates for Bf_NR {station_id}")
                    continue
            else:
                print(f"Coordinates missing or invalid for Bf_NR {station_id}")
                continue

            station_details.append({
                'Bf_NR': station_id,
                'name': name,
                'latitude': latitude,
                'longitude': longitude,
            })

        except stationen_ISK_2022.DoesNotExist:
            print(f"No matching station found for Bf_NR {station_id}")
            continue
        except json.JSONDecodeError:
            print(f"Error decoding JSON for coordinates of Bf_NR {station_id}: {coordinates}")
            continue
        except Exception as e:
            print(f"Unexpected error for Bf_NR {station_id}: {e}")
            continue

    return station_details'''


def generate_plotly_pb_view(data_queryset, mapbox_access_token):
    station_details = pd.DataFrame(get_station_details(data_queryset))
    
    hover_text = station_details.apply(lambda row: f"Bf_NR: {row['Bf_NR']}<br>Name: {row['name']}", axis=1)

    fig = go.Figure()

    
    fig.add_trace(go.Scattermapbox(
        lon=station_details['latitude'],  # Note: 'lat' and 'lon' expect array-like objects
        lat=station_details['longitude'],
        mode='markers',
        marker=dict(size=8, color='#003366'),
        hoverinfo='text',
        hovertext=hover_text,
        name= 'Bahnhöfe/ Stationen',
        showlegend=False,
    ))

    # Assuming you want to center the map around the first station detail
    if not station_details.empty:
        center_lat = station_details.iloc[0]['latitude']
        center_lon = station_details.iloc[0]['longitude']
        map_title = "Geoplot"
    else:
        center_lat = 0  # Default latitude if list is empty
        center_lon = 0  # Default longitude if list is empty
        map_title = "Geoplot"

    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            zoom=6.0,
            style='outdoors',
            center=dict(lon=float(center_lat), lat=float(center_lon))  
        ),
        legend=dict(
            font=dict(size=20),
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        showlegend=True,
        title=map_title,
        title_font=dict(color='#003366', size=24),
        title_x=0.5,
        margin=dict(b=40),
        height=800
    )

    

    
    fig.update_layout(
        updatemenus=[dict(
            buttons=[
                dict(args=[{"mapbox.style": "outdoors"}], label="Outdoors", method="relayout"),
                dict(args=[{"mapbox.style": "satellite"}], label="Satellite", method="relayout"),
                dict(args=[{"mapbox.style": "light"}], label="Hell", method="relayout"),
                dict(args=[{"mapbox.style": "dark"}], label="Dunkel", method="relayout"),
                dict(args=[{"mapbox.style": "streets"}], label="Straße", method="relayout"),
                dict(args=[{"mapbox.style": "satellite-streets"}], label="Satellite mit Straßen", method="relayout"),
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

    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return plot_html


def show_plot(data, mapbox_access_token, show_geo_plot, view, anlage_type=''):
    if view == 'pb':
        if show_geo_plot:
            plot_html = generate_plotly_pb_view(data, mapbox_access_token)
        else:
            plot_html = ''
    else:
        if show_geo_plot:
            plot_html = generate_plot_html(data, anlage_type, mapbox_access_token)
        else:
            plot_html = ''
    return plot_html

def get_api_cards(data):
    annotations = {
        'hasParking_yes': Count(Case(When(Bf_NR__hasParking='True', then=1))),
        'hasParking_no': Count(Case(When(Bf_NR__hasParking='False', then=1))),

        'hasBicycleParking_yes': Count(Case(When(Bf_NR__hasBicycleParking=True, then=1))),
        'hasBicycleParking_no': Count(Case(When(Bf_NR__hasBicycleParking=False, then=1))),

        'hasLocalPublicTransport_yes': Count(Case(When(Bf_NR__hasLocalPublicTransport=True, then=1))),
        'hasLocalPublicTransport_no': Count(Case(When(Bf_NR__hasLocalPublicTransport=False, then=1))),

        'hasPublicFacilities_yes': Count(Case(When(Bf_NR__hasPublicFacilities=True, then=1))),
        'hasPublicFacilities_no': Count(Case(When(Bf_NR__hasPublicFacilities=False, then=1))),

        'hasLockerSystem_yes': Count(Case(When(Bf_NR__hasLockerSystem=True, then=1))),
        'hasLockerSystem_no': Count(Case(When(Bf_NR__hasLockerSystem=False, then=1))),

        'hasTaxiRank_yes': Count(Case(When(Bf_NR__hasTaxiRank=True, then=1))),
        'hasTaxiRank_no': Count(Case(When(Bf_NR__hasTaxiRank=False, then=1))),

        'hasTravelNecessities_yes': Count(Case(When(Bf_NR__hasTravelNecessities=True, then=1))),
        'hasTravelNecessities_no': Count(Case(When(Bf_NR__hasTravelNecessities=False, then=1))),

        'hasWiFi_yes': Count(Case(When(Bf_NR__hasWiFi=True, then=1))),
        'hasWiFi_no': Count(Case(When(Bf_NR__hasWiFi=False, then=1))),

        'hasTravelCenter_yes': Count(Case(When(Bf_NR__hasTravelCenter=True, then=1))),
        'hasTravelCenter_no': Count(Case(When(Bf_NR__hasTravelCenter=False, then=1))),

        'hasRailwayMission_yes': Count(Case(When(Bf_NR__hasRailwayMission=True, then=1))),
        'hasRailwayMission_no': Count(Case(When(Bf_NR__hasRailwayMission=False, then=1))),

        'hasDBLounge_yes': Count(Case(When(Bf_NR__hasDBLounge=True, then=1))),
        'hasDBLounge_no': Count(Case(When(Bf_NR__hasDBLounge=False, then=1))),

        'hasLostAndFound_yes': Count(Case(When(Bf_NR__hasLostAndFound=True, then=1))),
        'hasLostAndFound_no': Count(Case(When(Bf_NR__hasLostAndFound=False, then=1))),

        'hasCarRental_yes': Count(Case(When(Bf_NR__hasCarRental=True, then=1))),
        'hasCarRental_no': Count(Case(When(Bf_NR__hasCarRental=False, then=1))),

        'hasSteplessAccess_yes': Count(Case(When(Bf_NR__hasSteplessAccess=True, then=1))),
        'hasSteplessAccess_no': Count(Case(When(Bf_NR__hasSteplessAccess=False, then=1))),
        #'hasSteplessAccess_partial': Count(Case(When(Bf_NR__hasSteplessAccess='partial', then=1))),

        'hasMobilityService_yes': Count(Case(When(Bf_NR__hasMobilityService=True, then=0), default=1)),
        'hasMobilityService_no': Count(Case(When(Bf_NR__hasMobilityService=False, then=1))),
    }

    api_cards = data.aggregate(**annotations)
    print("API CARDS:" ,api_cards)
    return api_cards