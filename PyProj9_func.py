"""
This is the function script for the PyProj9_main script. The purpose of this script
was to practice object-oriented programming, reading in a JSON file and attributing/
creating geopackages from the JSON data.

Any folder paths have been change to empty quotes for privacy and flexibility.

@author: dknight2
"""
import qgis
import qgis.core

# abstract class Waterbody is the root class of our hierarchy 
class Waterbody():
    
    # constructor (can be derived by subclasses)
    def __init__(self, name, geometry):
        self.name = name            # instance variable for storing the name of the watebrbody
        self.geometry = geometry    # instance variable for storing the a QgsGeometry object with the geometry for this waterbody

    # abstract static class function for creating a waterbody object if the given way satisfies
    # the required conditions; needs to be overridden by instantiable subclasses 
    def fromOSMWay(way, allNodes):     
        pass
    
    # abstract method for creating QgsFeature object for this waterbody;
    # needs to be overridden by instantiable subclasses 
    def toQgsFeature(self):
        pass
    

# abstract class LinearWaterBody is derived from class Waterbody
class LinearWaterbody(Waterbody):
    
    # constructor (can be invoked by derived classes and takes care of the length computation)
    def __init__(self, name, geometry):
        super(LinearWaterbody, self).__init__(name, geometry)
        
        # calculate length of this linear waterbody
        qda = qgis.core.QgsDistanceArea() 
        qda.setEllipsoid('WGS84')
        length = qda.measureLength(geometry)

        # instance variable for storing the length of this linear waterbody
        self.length = qda.convertLengthMeasurement(length, qgis.core.QgsUnitTypes.DistanceMeters)
        
        

    def toGeoPackage(item, output):
        layer = qgis.core.QgsVectorLayer('LineString?crs=EPSG:4326&field=NAME:string(255)&field=TYPE:string(255)&field=LENGTH:string(255)', 'Linear Features', 'memory')
        prov = layer.dataProvider()
        
        prov.addFeatures(item)
        qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer, output, "utf-8", layer.crs(), "GPKG")
        
    
    # ... you may want to add additional auxiliary methods or class functions to this class definition


# abstract class ArealWaterbody is derived from class Waterbody
class ArealWaterbody(Waterbody):

    # constructor (can be invoked by derived classes and takes care of the area computation)
    def __init__(self, name, geometry):
        super(ArealWaterbody, self).__init__(name, geometry)

        # calculate area of this areal waterbody
        qda = qgis.core.QgsDistanceArea() 
        qda.setEllipsoid('WGS84')
        area = qda.measureArea(geometry)

        # instance variable for storing the length of this areal waterbody
        self.area = qda.convertAreaMeasurement(area, qgis.core.QgsUnitTypes.AreaSquareMeters)

    def toGeoPackage(item, output):
        layer = qgis.core.QgsVectorLayer('Polygon?crs=EPSG:4326&field=NAME:string(255)&field=TYPE:string(255)&field=AREA:string(255)', 'Areal Features', 'memory')
        prov = layer.dataProvider()
        
        prov.addFeatures(item)
        qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer, output, "utf-8", layer.crs(), "GPKG")
    # ... you may want to add additional auxiliary methods or class functions to this class definition


# class Stream is derived from class LinearWaterBody and can be instantiated
class Stream(LinearWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Stream,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        # ... write code that tests whether the way element in parameter 'way' satisfies the tag conditions for Streams;
        streams = []
        points = []
        name = ''
        for stream in way:
            if way['type'] == 'way':
                if 'waterway' in way['tags']:
                    if way['tags']['waterway'] == 'stream':
                        streams.append(way)
        for way in streams:
            # getting the name information
            if 'name' in way['tags']:
                # getting the name information
                name = way['tags']['name']
            else:
                name = 'unknown'
            # Use the node's lat/lon info to create a list of QgsPointXY objects
            for nid in way['nodes']:
                node = allNodes[nid]
                p = qgis.core.QgsPointXY(node['lon'],node['lat'])
                points.append(p)
                
            geometry = qgis.core.QgsGeometry.fromPolylineXY(points)
            stream = Stream(name, geometry)
            return stream
     
    # override the toQgsFeature(...) method
    def toQgsFeature(self):

        feature = qgis.core.QgsFeature()
        feature.setAttributes([self.name, "Stream", self.length])
        feature.setGeometry(self.geometry)        
        return feature
       
    def __str__(self):
        return 'Name: {}, Type: {} (length: {}m)'.format(self.name, 'Stream', self.length)
   
class River(LinearWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(River,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        # ... write code that tests whether the way element in parameter 'way' satisfies the tag conditions for Streams;
        rivers = []
        points = []
        name = ''
        for river in way:
            if way['type'] == 'way':
                if 'waterway' in way['tags']:
                    if way['tags']['waterway'] == 'river':
                        rivers.append(way)
        for way in rivers:
            # getting the name information
            if 'name' in way['tags']:
                # getting the name information
                name = way['tags']['name']
            else:
                name = 'unknown'
            # Use the node's lat/lon info to create a list of QgsPointXY objects
            for nid in way['nodes']:
                node = allNodes[nid]
                p = qgis.core.QgsPointXY(node['lon'],node['lat'])
                points.append(p)
                
            geometry = qgis.core.QgsGeometry.fromPolylineXY(points)            
            river = River(name, geometry)        
            return river

    # override the toQgsFeature(...) method
    def toQgsFeature(self):

        feature = qgis.core.QgsFeature()
        feature.setAttributes([self.name, 'River', self.length])
        feature.setGeometry(self.geometry)
        
        return feature
       
    def __str__(self):
        return 'Name: {}, Type: {} (length: {}m)'.format(self.name, 'River', self.length)

class Canal(LinearWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Canal,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        # ... write code that tests whether the way element in parameter 'way' satisfies the tag conditions for Streams;
        canals = []
        points = []
        name = ''
        for canal in way:
            if way['type'] == 'way':
                if 'waterway' in way['tags']:
                    if way['tags']['waterway'] == 'canal':
                        canals.append(way)
        for way in canals:
            # getting the name information
            if 'name' in way['tags']:
                # getting the name information
                name = way['tags']['name']
            else:
                name = 'unknown'
            # Use the node's lat/lon info to create a list of QgsPointXY objects
            for nid in way['nodes']:
                node = allNodes[nid]
                p = qgis.core.QgsPointXY(node['lon'],node['lat'])
                points.append(p)
                
            geometry = qgis.core.QgsGeometry.fromPolylineXY(points)           
            canal = Canal(name, geometry)            
            return canal
     
    # override the toQgsFeature(...) method
    def toQgsFeature(self):

        feature = qgis.core.QgsFeature()
        feature.setAttributes([self.name, 'Canal', self.length])
        feature.setGeometry(self.geometry)        
        return feature
       
    def __str__(self):
        return 'Name: {}, Type: {} (length: {}m)'.format(self.name, 'Canal', self.length)

class Lake(ArealWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Lake,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        # ... write code that tests whether the way element in parameter 'way' satisfies the tag conditions for Streams;
        lakes = []
        points = []
        name = ''
        for lake in way:
            if way['type'] == 'way':
                if 'natural' in way['tags']:
                    if 'water' in way['tags']:
                        if way['tags']['water'] == 'lake':
                            lakes.append(way)

        for item in lakes:
            if 'name' in item['tags']:
                name = item['tags']['name']
            else:
                name = 'unknown'
        
        # Use the node's lat/lon info to create a list of QgsPointXY objects
            for nid in way['nodes']:
                node = allNodes[nid]
                p = qgis.core.QgsPointXY(node['lon'],node['lat'])
                points.append(p)
                   
            geometry = qgis.core.QgsGeometry.fromPolygonXY([points])
            lake = Lake(name, geometry)
            return lake
     
    # override the toQgsFeature(...) method
    def toQgsFeature(self):

        feature = qgis.core.QgsFeature()
        feature.setAttributes([self.name, "Lake", self.area])
        feature.setGeometry(self.geometry)        
        return feature
       
    def __str__(self):
        return 'Name: {}, Type: {} (area: {} square m)'.format(self.name, 'Lake', self.area)

class Pond(ArealWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Pond,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        # ... write code that tests whether the way element in parameter 'way' satisfies the tag conditions for Streams;
        ponds = []
        points = []
        name = ''
        for pond in way:
            if way['type'] == 'way':
                if 'natural' in way['tags']:
                    if 'water' in way['tags']:
                        if way['tags']['water'] == 'pond':
                            ponds.append(way)

        for item in ponds:
            if 'name' in item['tags']:
                name = item['tags']['name']
            else:
                name = 'unknown'
        
        # Use the node's lat/lon info to create a list of QgsPointXY objects
            for nid in way['nodes']:
                node = allNodes[nid]
                p = qgis.core.QgsPointXY(node['lon'],node['lat'])
                points.append(p)
                   
            geometry = qgis.core.QgsGeometry.fromPolygonXY([points])
            pond = Pond(name, geometry)
            return pond
     
    # override the toQgsFeature(...) method
    def toQgsFeature(self):

        feature = qgis.core.QgsFeature()
        feature.setAttributes([self.name, "Pond", self.area])
        feature.setGeometry(self.geometry)        
        return feature
       
    def __str__(self):
        return 'Name: {}, Type: {} (area: {} square m)'.format(self.name, 'Pond', self.area)

class Reservoir(ArealWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Reservoir,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        # ... write code that tests whether the way element in parameter 'way' satisfies the tag conditions for Streams;
        reservoirs = []
        points = []
        name = ''
        for reservoir in way:
            if way['type'] == 'way':
                if 'natural' in way['tags']:
                    if 'water' in way['tags']:
                        if way['tags']['water'] == 'reservoir':
                            reservoirs.append(way)

        for item in reservoirs:
            if 'name' in item['tags']:
                name = item['tags']['name']
            else:
                name = 'unknown'
        
        # Use the node's lat/lon info to create a list of QgsPointXY objects
            for nid in way['nodes']:
                node = allNodes[nid]
                p = qgis.core.QgsPointXY(node['lon'],node['lat'])
                points.append(p)
                   
            geometry = qgis.core.QgsGeometry.fromPolygonXY([points])
            reservoir = Reservoir(name, geometry)
            return reservoir
     
    # override the toQgsFeature(...) method
    def toQgsFeature(self):

        feature = qgis.core.QgsFeature()
        feature.setAttributes([self.name, "Reservoir", self.area])
        feature.setGeometry(self.geometry)        
        return feature
       
    def __str__(self):
        return 'Name: {}, Type: {} (area: {} square m)'.format(self.name, 'Reservoir', self.area)