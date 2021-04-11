#!/usr/bin/env python
# coding: utf-8

# In[155]:


import json
import drawSvg as draw
import os


# In[162]:


def draw_svg_from_geometry(geometry, name, resolution=0, dimensions=200, stroke_width=2, fill="651fff"):
    resolution = 2 ** resolution 
    geometries = []
    DISTRICT = 2
    if ("geometries" in geometry):
        #print("multi-geometry")
        for i in range(len(geometry['geometries'])):
            if (type(geometry['geometries'][i]['coordinates'][0][0][0]) != type([])):
                geometries.append(geometry['geometries'][i]['coordinates'][0])
            else:
                geometries.append(geometry['geometries'][i]['coordinates'][0][0])

    else:
        #print("single-geometry")
        if (type(geometry['coordinates'][0][0][0]) != type([])):
            geometries.append(geometry['coordinates'][0])
        else:
            geometries.append(geometry['coordinates'][0][0])


    n = len(geometries) #number of geometries
    
    cordsX = []   #store X coordinates 1d array
    cordsY = []   #store Y coordinates 1d array
    cords = []    #store all paths 2d array
    
    
    for i in range(n):
        arr = []
        for j in range(len(geometries[i])):
            cordsX.append(geometries[i][j][0])
            cordsY.append(geometries[i][j][1])
            arr.extend(geometries[i][j])
        cords.append(arr)

            
    if (cordsX == []):
        return
    #geometry bounds
    minimumX = min(cordsX)
    maximumX = max(cordsX)
    minimumY = min(cordsY)
    maximumY = max(cordsY)
    
    if (minimumX==maximumX):
        return

    if (minimumY==maximumY):
        return
    
    
    #scaling the geometry
    scaleX = dimensions/(maximumX-minimumX)
    scaleY = dimensions/(maximumY-minimumY)

    #middle of all geometries
    middleX = (maximumX+minimumX)/2
    middleY = (maximumY+minimumY)/2

    scale = min([scaleX,scaleY])

    new_cords = [] #store transformed cooridinates
    
    for i in range(len(cords)):
        rescaled_arr = []
        rescaled_arr = [0]*(len(cords[i]))
        for j in range(len(rescaled_arr)):
            if (j%2 == 0):
                rescaled_arr[j] = (cords[i][j]-middleX)*scale
            else:
                rescaled_arr[j] = (cords[i][j]-middleY)*scale
        new_cords.append(rescaled_arr)
    
    d = draw.Drawing(dimensions+1, dimensions+1, origin='center', displayInline=False)
    


    for i in range(len(new_cords)):
        p = draw.Path(stroke_width=stroke_width, stroke=fill,
                  fill=fill, fill_opacity=0.5)
        p.M(new_cords[i][0],new_cords[i][1])
        for j in range(0,len(new_cords[i])-1):
            if (j%resolution == 0):
                p.L(new_cords[i][j],new_cords[i][j+1])
        p.Z()
        d.append(p)
        
    path = "./Export"
        
    try:
        os.mkdir(path)
    except OSError:
        d.saveSvg('./Export/'+name.replace(" ", "")+'.svg')
    else:
        d.saveSvg('./Export/'+name.replace(" ", "")+'.svg')

    


# In[163]:


def GEOJSONtoSVG(file,key,resolution=1,dimensions=200,strokeWidth=2,color="#ff0000"):
    with open(file) as f:
      data = json.load(f)

    for i in range(len(data['features'])):
        draw_svg_from_geometry(data['features'][i]['geometry'],data['features'][i]['properties'][key],resolution,dimensions,strokeWidth,color)

