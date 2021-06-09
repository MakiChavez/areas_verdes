#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
import folium as fl
from folium import plugins
import folium.plugins as plugins
df_av = pd.read_csv("https://raw.githubusercontent.com/MakiChavez/areas_verdes/main/areasLimpioUltimo.csv")
df_servicios = pd.read_csv("https://raw.githubusercontent.com/MakiChavez/areas_verdes/main/DENUE_2020.csv")
df_av


# In[79]:


AreaF = df_av['SHAPE_AREA'].map('{:,.0f}'.format)


# In[110]:


fig = px.sunburst(df_av,
                  path=["SECTOR", "TIPOLOGIA", "NOMBRE_PARQUE"],
                  values='SHAPE_AREA',
                  width=750, height=700,
                  color_discrete_sequence =['#D81159','#FFBC42','#07B77E','#0496FF','#006BA6'],
                  color='TIPOLOGIA',
                  hover_name='Area: '+AreaF+' m2',
                  hover_data={'SHAPE_AREA':False,'TIPOLOGIA':False},
                  title="Parques en San Pedro (K1)",
                  template="seaborn"
                  )
fig.update_traces(textinfo='label+percent parent')
fig.show()


# In[119]:


# Loading the background map
mapa_parques = fl.Map(location=[25.679520,-100.417480], zoom_start=15, tiles="OpenStreetMap")

         
for i in range(0,len(df_servicios)):
    fl.Circle(
       location=[df_servicios.iloc[i]['latitud'], df_servicios.iloc[i]['longitud']],opacity = 0.8,
        popup= df_servicios.iloc[i]['nom_estab'],radius=3,tooltip= df_servicios.iloc[i]['nom_estab']
              ).add_to(mapa_parques) 

for i in range(0,len(df_av)):
  fl.Circle(
       location=[df_av.iloc[i]['LAT'], df_av.iloc[i]['LONG']],fill= False, color = "#688C4F", opacity = 0.5,
        popup = df_av.iloc[i]['NOMBRE_PARQUE'], radius = 400
              ).add_to(mapa_parques)

 
for idx, parque in df_av.iterrows():
    if parque['TIPOLOGIA'] == 'Parque de barrio':
        fl.Marker(location=(parque['LAT'],parque['LONG']),icon= fl.Icon(color='black',icon_color="#FFBC42"),popup= parque['NOMBRE_PARQUE'],tooltip= parque['NOMBRE_PARQUE']).add_to(mapa_parques)
    elif parque['TIPOLOGIA'] == 'Parque urbano':
        fl.Marker(location=(parque['LAT'],parque['LONG']), icon= fl.Icon(color='blue',icon_color= "#006BA6"), popup= parque['NOMBRE_PARQUE'],tooltip= parque['NOMBRE_PARQUE']).add_to(mapa_parques)
    elif parque['TIPOLOGIA'] == 'Parque lineal':
        fl.Marker(location=(parque['LAT'],parque['LONG']),icon= fl.Icon(color="pink", icon_color="#D81159"),popup= parque['NOMBRE_PARQUE'],tooltip= parque['NOMBRE_PARQUE']).add_to(mapa_parques)
    else:
        fl.Marker(location=(parque['LAT'],parque['LONG']),icon= fl.Icon(color="lightgreen",icon_color = '#70B77E'), popup= parque['NOMBRE_PARQUE'],tooltip= parque['NOMBRE_PARQUE']).add_to(mapa_parques)



# Display
mini_map = plugins.MiniMap(toggle_display= True, width=200, height=200, collapsed_width=25)
mapa_parques.add_child(mini_map)


mapa_parques


# In[120]:


### GUARDARLO COMO HTML
mapa_parques.save(outfile= "MAPA_OVERVIEW.html")


# In[83]:


df_urbano = pd.read_csv('https://raw.githubusercontent.com/MakiChavez/areas_verdes/main/Urbano.csv')
df_barrio = pd.read_csv('https://raw.githubusercontent.com/MakiChavez/areas_verdes/main/Barrio.csv')
df_lineal = pd.read_csv('https://raw.githubusercontent.com/MakiChavez/areas_verdes/main/Lineal.csv')
df_bolsillo = pd.read_csv('https://raw.githubusercontent.com/MakiChavez/areas_verdes/main/Bolsillo.csv')
df_urbano


# In[102]:


azul='#006BA6' #urbano
rosa='#D81159' #lineal
amarillo='#FFBC42' #barrio
verde='#70B77E' #bolsillo
colors = ['#D81159','#FFBC42','#70B77E','#006BA6','#0496FF']


# In[103]:


xU = df_urbano["NOMBRE_PARQUE"]
yU = df_urbano["SHAPE_AREA"]

figRankUrbano = go.Figure(data=[go.Bar(x=xU, y=yU,
            hovertext=['Area del #1: 50,322 m2', 'Area del #2: 43,372 m2', 'Area del #3: 7,825 m2', 'Area del #4: 2,790 m2', 'Area del #5: 1,398 m2'])])
# Customize aspect
figRankUrbano.update_traces(marker_color=azul, marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
figRankUrbano.update_layout(title_text="TOP 5: Parque Urbano", yaxis_title="m2 de parque")
figRankUrbano.show()


# In[104]:


xBA = df_barrio["NOMBRE_PARQUE"]
yBA = df_barrio["SHAPE_AREA"]

figRankBarrio = go.Figure(data=[go.Bar(x=xBA, y=yBA,
            hovertext=['Area del #1: 15,204 m2', 'Area del #2: 14,897 m2', 'Area del #3: 14,415 m2', 'Area del #4: 11,679 m2', 'Area del #5: 10,024 m2'])])
# Customize aspect
figRankBarrio.update_traces(marker_color=amarillo, marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
figRankBarrio.update_layout(title_text="TOP 5: Parque Barrio", yaxis_title="m2 de parque")
figRankBarrio.show()


# In[105]:


xL = df_lineal["NOMBRE_PARQUE"]
yL = df_lineal["SHAPE_AREA"]

figRankLineal = go.Figure(data=[go.Bar(x=xL, y=yL,
            hovertext=['Area del #1: 7,859 m2', 'Area del #2: 3,021 m2', 'Area del #3: 2,786 m2', 'Area del #4: 2,114 m2', 'Area del #5: 981 m2'])])
# Customize aspect
figRankLineal.update_traces(marker_color=rosa, marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
figRankLineal.update_layout(title_text="TOP 5: Parque Lineal", yaxis_title="m2 de parque")
figRankLineal.show()


# In[106]:


xBO = df_bolsillo["NOMBRE_PARQUE"]
yBO = df_bolsillo["SHAPE_AREA"]

figRankBolsillo = go.Figure(data=[go.Bar(x=xBO, y=yBO,
            hovertext=['Area del #1: 1,494 m2', 'Area del #2: 1,328 m2', 'Area del #3: 1,152 m2', 'Area del #4: 1,107 m2', 'Area del #5: 924 m2'])])
# Customize aspect
figRankBolsillo.update_traces(marker_color=verde, marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
figRankBolsillo.update_layout(title_text="TOP 5: Parque Bolsillo", yaxis_title="m2 de parque")
figRankBolsillo.show()


# In[121]:


#URBANO
latitude= 25.679520
longitude= -100.417480
map1 = fl.Map(location=[latitude,longitude],tiles="openstreetmap", zoom_start=15)

for i in range(0,len(df_urbano)):
   fl.Circle(
       location=[df_urbano.iloc[i]['LAT'], df_urbano.iloc[i]['LONG']],fill= True, color = "#888581",opacity= 0.3,
        popup= df_urbano.iloc[i]['NOMBRE_PARQUE'],tooltip= df_urbano.iloc[i]['NOMBRE_PARQUE'], radius = 400
              ).add_to(map1)

   fl.Marker(
       location=[df_urbano.iloc[i]['LAT'], df_urbano.iloc[i]['LONG']],
        popup= df_urbano.iloc[i]['NOMBRE_PARQUE'],icon= fl.Icon(color='blue',icon_color= "#006BA6"), tooltip= df_urbano.iloc[i]['NOMBRE_PARQUE'],
              ).add_to(map1) 

         
for i in range(0,len(df_servicios)):
    fl.Circle(
       location=[df_servicios.iloc[i]['latitud'], df_servicios.iloc[i]['longitud']],opacity=0.83,
        popup= df_servicios.iloc[i]['nom_estab'],radius=4,tooltip= df_servicios.iloc[i]['nom_estab']
              ).add_to(map1) 


mini_map = plugins.MiniMap(toggle_display=True, width=180, height=180, collapsed_width=25)
map1.add_child(mini_map)
map1


# In[122]:


map1.save(outfile= "MAPA_URBANO.html")


# In[123]:


#lineal
latitude= 25.679520
longitude= -100.417480
map2 = fl.Map(location=[latitude,longitude],tiles="openstreetmap", zoom_start=15)
fl.LayerControl().add_to(map2)


for i in range(0,len(df_lineal)):
   fl.Circle(
       location=[df_lineal.iloc[i]['LAT'], df_lineal.iloc[i]['LONG']],fill= True, color = "#888581", opacity= 0.3,
        popup= df_lineal.iloc[i]['NOMBRE_PARQUE'],tooltip= df_lineal.iloc[i]['NOMBRE_PARQUE'], radius = 400
              ).add_to(map2)

   fl.Marker(
       location=[df_lineal.iloc[i]['LAT'], df_lineal.iloc[i]['LONG']],
        popup= df_lineal.iloc[i]['NOMBRE_PARQUE'],icon= fl.Icon(color="pink", icon_color="#D81159" ), tooltip= df_lineal.iloc[i]['NOMBRE_PARQUE'],
              ).add_to(map2) 

         
for i in range(0,len(df_servicios)):
    fl.Circle(
       location=[df_servicios.iloc[i]['latitud'], df_servicios.iloc[i]['longitud']],
        popup= df_servicios.iloc[i]['nom_estab'],radius=4,tooltip= df_servicios.iloc[i]['nom_estab']
              ).add_to(map2) 



mini_map = plugins.MiniMap(toggle_display=True, width=180, height=180, collapsed_width=25)
map2.add_child(mini_map)
map2


# In[124]:


map2.save(outfile= "MAPA_LINEAL.html")


# In[129]:


#bolsillo
latitude= 25.66644464
longitude= -100.4086041
map3 = fl.Map(location=[latitude,longitude],tiles="openstreetmap", zoom_start=15)



for i in range(0,len(df_bolsillo)):
   fl.Circle(
       location=[df_bolsillo.iloc[i]['LAT'], df_bolsillo.iloc[i]['LONG']],fill= True, color = "#888581", opacity= 0.3,
        popup= df_bolsillo.iloc[i]['NOMBRE_PARQUE'],tooltip= df_bolsillo.iloc[i]['NOMBRE_PARQUE'], radius = 400
              ).add_to(map3)

   fl.Marker(
       location=[df_bolsillo.iloc[i]['LAT'], df_bolsillo.iloc[i]['LONG']],
        popup= df_bolsillo.iloc[i]['NOMBRE_PARQUE'],icon= fl.Icon(color="lightgreen",icon_color = '#70B77E' ), tooltip= df_bolsillo.iloc[i]['NOMBRE_PARQUE'],
              ).add_to(map3) 
  
         
for i in range(0,len(df_servicios)):
    fl.Circle(
       location=[df_servicios.iloc[i]['latitud'], df_servicios.iloc[i]['longitud']],
        popup= df_servicios.iloc[i]['nom_estab'],radius=4,tooltip= df_servicios.iloc[i]['nom_estab']
              ).add_to(map3) 



mini_map = plugins.MiniMap(toggle_display=True, width=180, height=180, collapsed_width=25)
map3.add_child(mini_map)
map3


# In[131]:


map3.save(outfile= "MAPA_BOLSILLO.html")


# In[127]:


#barrio
latitude= 25.679520
longitude= -100.417480
map4 = fl.Map(location=[latitude,longitude],tiles="openstreetmap", zoom_start=15)


for i in range(0,len(df_barrio)):
   fl.Circle(
       location=[df_barrio.iloc[i]['LAT'], df_barrio.iloc[i]['LONG']],fill= True, color = "#888581",opacity= 0.3,
        popup= df_barrio.iloc[i]['NOMBRE_PARQUE'],tooltip= df_barrio.iloc[i]['NOMBRE_PARQUE'], radius = 400
              ).add_to(map4)

   fl.Marker(
       location=[df_barrio.iloc[i]['LAT'], df_barrio.iloc[i]['LONG']],
        popup= df_barrio.iloc[i]['NOMBRE_PARQUE'],icon= fl.Icon(color='black',icon_color="#FFBC42"), tooltip= df_barrio.iloc[i]['NOMBRE_PARQUE'],
              ).add_to(map4) 

         
for i in range(0,len(df_servicios)):
    fl.Circle(
       location=[df_servicios.iloc[i]['latitud'], df_servicios.iloc[i]['longitud']],opacity=0.83,
        popup= df_servicios.iloc[i]['nom_estab'],radius=4,tooltip= df_servicios.iloc[i]['nom_estab']
              ).add_to(map4) 



mini_map = plugins.MiniMap(toggle_display=True, width=180, height=180, collapsed_width=25)
map4.add_child(mini_map)
map4


# In[128]:


map4.save(outfile= "MAPA_BARRIO.html")

