from django.shortcuts import render

# generic base view
from django.views.generic import TemplateView 




#folium
import folium
from folium import plugins



#gee
import ee
from geemap import geojson_to_ee, ee_to_geojson
from ipyleaflet import GeoJSON, Marker, MarkerCluster

ee.Initialize()


#forntend
#home
class home(TemplateView):
    template_name = 'index.html'
    # Define a method for displaying Earth Engine image tiles on a folium map.
    

    def get_context_data(self, **kwargs):

        figure = folium.Figure()

        m = folium.Map(
            location=[9.0, 2.4],
            zoom_start=7,
        )
        m.add_to(figure)

        plugins.Fullscreen(position='topright', title='Full Screen', title_cancel='Exit Full Screen', force_separate_button=False).add_to(m)
        
        alldept = ee.Image('users/ashamba/allDepartments_v0')

        benin_adm1 = ee.FeatureCollection("users/ashamba/BEN_adm1")
        benin_adm1_json = ee_to_geojson(benin_adm1)
        
        benin_adm2 = ee.FeatureCollection("users/ashamba/BEN_adm2")
        benin_adm2_json = ee_to_geojson(benin_adm2)

        



        # dataset = ee.ImageCollection('MODIS/006/MOD13Q1').filter(ee.Filter.date('2019-07-01', '2019-11-30')).first()
        # modisndvi = dataset.select('NDVI')
        # visParams = {'min':0, 'max':3000, 'palette':['225ea8','41b6c4','a1dab4','034B48']}
        # vis_paramsNDVI = {
        #     'min': 0,
        #     'max': 9000,
        #     'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}

        # map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
        # folium.raster_layers.TileLayer(
        #             tiles = map_id_dict['tile_fetcher'].url_format,
        #             attr = 'Google Earth Engine',
        #             name = 'NDVI',
        #             overlay = True,
        #             control = True
        #             ).add_to(m)
        def add_ee_layer(self, ee_image_object, vis_params, name):
            map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
                name=name,
                overlay=True,
                control=True
            ).add_to(self)

        folium.Map.add_ee_layer = add_ee_layer   
        m.add_ee_layer(alldept, {'min':0, 'max': 4, 'palette': "black, green, white, gray"}, 'Benin Cashew Predict')

        # json_layer_ben = folium.GeoJson(data=benin_adm1_json, name='Benin States JSON')

        def highlight_function(feature):
            return {"fillColor": "#ffaf00", "color": "green", "weight": 3, "dashArray": "1, 1"}

        g = folium.GeoJson(data=benin_adm1_json,
           name='Benin Dept JSON',
           highlight_function = highlight_function)

        g1 = folium.GeoJson(data=benin_adm2_json,
           name='Benin Communes JSON',
           highlight_function = highlight_function)

    
        
        # m.add_child(json_layer_ben)

        folium.GeoJsonTooltip(fields=["NAME_1"],
            aliases = ["Dep't name:"],
            labels = False,
            sticky = False,
            style=("background-color: white; color: black; font-family: sans-serif; font-size: 12px; padding: 4px;")
            ).add_to(g)

        folium.GeoJsonTooltip(fields=["NAME_2"],
            aliases = ["Commune name:"],
            labels = False,
            sticky = False,
            style=("background-color: white; color: black; font-family: sans-serif; font-size: 12px; padding: 4px;")
            ).add_to(g1)

        g.add_to(m)

        g1.add_to(m)

        m.add_child(folium.LayerControl())


        figure.render()

        # print('test')
        return {"map": figure}