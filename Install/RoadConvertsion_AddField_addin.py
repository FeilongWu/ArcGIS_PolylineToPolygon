import arcpy
import pythonaddins

class ButtonClass1(object):
    """Implementation for RoadConvertsion_AddField_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        def getCoor(WKT):
            return WKT[18:len(WKT)-2]
        
        def IsEnclosed(WKT):
            coordinates=WKT.split(" ")
            if (coordinates[0].strip(",")==coordinates[-2].strip(","))&(coordinates[1].strip(",")==coordinates[-1].strip(",")):
                return True
            else:
                return False
            
        def PolylintToPolygon(WKT):
            return arcpy.FromWKT("MULTIPOLYGON ((("+WKT+")))")

        input_fc=arcpy.env.workspace
        fc1=input_fc.split('\\')
        name1=fc1[-1]
        name=name1+'.shp'
        path=''
        for i in range(len(fc1[0:-1])):
            path+=fc1[i]
            if i != len(fc1[0:-1])-1:
                path+='\\'
        arcpy.env.workspace=path
        target=name1+"_Polygon"
        arcpy.CreateFeatureclass_management(arcpy.env.workspace,target,"POLYGON")
        fNamTyp={}
        for field in arcpy.ListFields(name1):
            if field.baseName in ["FID","Shape"]:
                continue
            else:
                fNamTyp[field.baseName]=field.type
        for key in fNamTyp:
            arcpy.AddField_management(target,key,fNamTyp[key])
            
        fc=arcpy.env.workspace+'\\'+name
        cursor=None
        cursor=arcpy.SearchCursor(fc)
        fValues=[]
        for road in cursor:
            row={}
            for key in fNamTyp:
                row[key]=road.getValue(key)
            fValues.append(row)

        cursorT=arcpy.da.InsertCursor(target,["SHAPE@"])
        cursor=None
        cursor=arcpy.SearchCursor(fc)
        NonLineRing=[]
        index=-1
        for road in cursor:
            index+=1
            record=road.getValue("Shape")
            WKT=getCoor(record.WKT)
            if IsEnclosed(WKT):
                try:
                    cursorT.insertRow([PolylintToPolygon(WKT)])
                except:
                    continue
            else:
                NonLineRing.append(index)
                continue
        cursor=None
        cursorT=None
        cursorT=arcpy.UpdateCursor(target)
        for key in fNamTyp:
            index=-1
            with arcpy.da.UpdateCursor(target,key) as cursor:
                for row in cursor:
                    index+=1
                    if index in NonLineRing:
                        continue
                    else:
                        row[0]=fValues[index][key]
                        cursor.updateRow(row)
        cusorT=None

class ComboBoxClass1(object):
    """Implementation for RoadConvertsion_AddField_addin.combobox (ComboBox)"""
    def __init__(self):
        self.items = ["item1", "item2"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
    def onSelChange(self, selection):
        layer = arcpy.mapping.ListLayers(self.mxd, selection)[0]
        arcpy.env.workspace=layer.workspacePath+'\\'+layer.name
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        self.mxd = arcpy.mapping.MapDocument('current')
        layers = arcpy.mapping.ListLayers(self.mxd)
        self.items = []
        for layer in layers:
            self.items.append(layer.name)
    def onEnter(self):
        pass
    def refresh(self):
        pass
