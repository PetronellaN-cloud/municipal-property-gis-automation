"""ArcGIS Pro toolbox for municipal property clipping."""
import os
import re
import uuid
import arcpy

FIELD = 'MUNICNAME'

class Toolbox:
    def __init__(self):
        self.label = 'Municipal Property Tools'
        self.alias = 'municipalproperty'
        self.tools = [ClipProperties]

class ClipProperties:
    def __init__(self):
        self.label = 'Clip Properties by Municipality'
        self.description = 'Select a municipality by name and clip property features.'
        self.canRunInBackground = False
        self._source = None
        self._names = []
        self._error = None

    def getParameterInfo(self):
        def param(label, name, datatype, kind='Required', direction='Input'):
            return arcpy.Parameter(displayName=label, name=name, datatype=datatype,
                                   parameterType=kind, direction=direction)
        boundaries = param('Municipal boundaries', 'boundaries', 'DEFeatureClass')
        properties = param('Property features', 'properties', 'DEFeatureClass')
        municipality = param('Select municipality', 'municipality', 'GPString')
        municipality.filter.type = 'ValueList'
        municipality.filter.list = []
        folder = param('Output folder', 'output_folder', 'DEFolder')
        output = param('Clipped properties', 'clipped_properties', 'DEFeatureClass', 'Derived', 'Output')
        return [boundaries, properties, municipality, folder, output]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        source = parameters[0].valueAsText
        if source != self._source:
            self._source = source
            self._names = []
            self._error = None
            if source and arcpy.Exists(source):
                try:
                    field = next((f.name for f in arcpy.ListFields(source)
                                  if f.name.upper() == FIELD), None)
                    if not field:
                        raise ValueError('MUNICNAME field not found.')
                    with arcpy.da.SearchCursor(source, [field]) as rows:
                        self._names = sorted({r[0] for r in rows if r[0] and str(r[0]).strip()}, key=str.casefold)
                    if not self._names:
                        self._error = 'No municipality names found.'
                except Exception as exc:
                    self._error = str(exc)
            parameters[2].filter.list = self._names
            if parameters[2].valueAsText not in self._names:
                parameters[2].value = None
        return

    def updateMessages(self, parameters):
        if self._error:
            parameters[0].setErrorMessage(self._error)
        for p in parameters[:2]:
            if p.valueAsText and arcpy.Exists(p.valueAsText):
                if arcpy.Describe(p.valueAsText).shapeType != 'Polygon':
                    p.setErrorMessage('A polygon feature class is required.')
        return

    def execute(self, parameters, messages):
        boundaries, properties, name, folder = [p.valueAsText for p in parameters[:4]]
        field = next((f.name for f in arcpy.ListFields(boundaries) if f.name.upper() == FIELD), None)
        if not field:
            raise arcpy.ExecuteError('MUNICNAME field not found.')
        sql = arcpy.AddFieldDelimiters(boundaries, field) + " = '" + name.replace("'", "''") + "'"
        stem = re.sub(r'[^\w-]+', '_', name, flags=re.UNICODE).strip('_') or 'Municipality'
        output = os.path.join(folder, stem + '_Properties_Clip.shp')
        if arcpy.Exists(output) or os.path.exists(output):
            arcpy.AddError('Output already exists. Choose another folder or rename the existing output: ' + output)
            raise arcpy.ExecuteError
        layer = 'municipality_' + uuid.uuid4().hex
        try:
            arcpy.management.MakeFeatureLayer(boundaries, layer, sql)
            count = int(arcpy.management.GetCount(layer)[0])
            if not count:
                arcpy.AddError('No matching municipality boundary found.')
                raise arcpy.ExecuteError
            if count > 1:
                arcpy.AddWarning(f'{count} boundary records match this name; all will be used for clipping. Verify that they represent the intended municipality.')
            arcpy.AddMessage('Clipping properties for ' + name)
            with arcpy.EnvManager(overwriteOutput=False, extent=None):
                arcpy.analysis.Clip(properties, layer, output)
            total = int(arcpy.management.GetCount(output)[0])
            arcpy.AddMessage(f'Output property features: {total:,}')
            arcpy.AddMessage('Saved to: ' + output)
            arcpy.SetParameterAsText(4, output)
        finally:
            if arcpy.Exists(layer):
                arcpy.management.Delete(layer)
