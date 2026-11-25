"""
AUTOMATED MUNICIPAL PROPERTY CLIP
For ArcGIS Pro / ArcPy

What it does:
1. Reads the municipal boundaries shapefile.
2. Selects one municipality using the MUNICNAME field.
3. Clips the property shapefile to that municipality.
4. Saves a separate output shapefile.

HOW TO USE:
- Open this file in ArcGIS Pro's Python environment or run it from the ArcGIS Pro Python
  Command Prompt.
- Edit DATA_FOLDER, OUTPUT_FOLDER, and MUNICIPALITY_NAME below.
- Run the script again whenever you need another municipality.

The paths below are examples based on the folder structure in your screenshot.
Replace the example root path with the actual full Windows path on your computer.
"""

import os
import re
import arcpy

# ---------------------------------------------------------------------
# 1. USER SETTINGS - EDIT THESE THREE SETTINGS
# ---------------------------------------------------------------------

# Example only: replace with the full path to your ITIS\\DATA folder.
DATA_FOLDER = r"C:\Users\OneDrive\ITIS\DATA"

# Where the clipped municipality shapefiles will be saved.
OUTPUT_FOLDER = os.path.join(DATA_FOLDER, "Clipped_Properties")

# Type the municipality exactly as it appears in the MUNICNAME field.
# Examples: "Buffalo City", "Nelson Mandela Bay", "Makana"
MUNICIPALITY_NAME = "Buffalo City"

# ---------------------------------------------------------------------
# 2. INPUT DATA
# ---------------------------------------------------------------------

MUNICIPALITIES_SHP = os.path.join(
    DATA_FOLDER, "MDB_Local_Municipalities_2026.shp"
)

PROPERTIES_SHP = os.path.join(
    DATA_FOLDER, "VW_LIS_PM_PROPERTIES_GEOM.shp"
)

MUNICIPALITY_FIELD = "MUNICNAME"

# ---------------------------------------------------------------------
# 3. PROCESSING
# ---------------------------------------------------------------------

def safe_filename(value):
    """Convert a municipality name into a Windows-safe output filename."""
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return value.strip("_")


def main():
    arcpy.env.overwriteOutput = True

    print("\n" + "=" * 65)
    print("MUNICIPAL PROPERTY CLIP")
    print("=" * 65)

    # Check that the input data exists.
    if not arcpy.Exists(MUNICIPALITIES_SHP):
        raise FileNotFoundError(
            "Municipalities shapefile not found:\n" + MUNICIPALITIES_SHP
        )

    if not arcpy.Exists(PROPERTIES_SHP):
        raise FileNotFoundError(
            "Properties shapefile not found:\n" + PROPERTIES_SHP
        )

    # Check that the municipality field exists.
    municipality_fields = [f.name for f in arcpy.ListFields(MUNICIPALITIES_SHP)]
    if MUNICIPALITY_FIELD not in municipality_fields:
        raise ValueError(
            f"Field '{MUNICIPALITY_FIELD}' was not found. "
            f"Available fields: {municipality_fields}"
        )

    # Create the output folder if it does not already exist.
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Build a safely quoted SQL expression.
    field_sql = arcpy.AddFieldDelimiters(
        MUNICIPALITIES_SHP, MUNICIPALITY_FIELD
    )
    municipality_sql_value = MUNICIPALITY_NAME.replace("'", "''")
    where_clause = f"{field_sql} = '{municipality_sql_value}'"

    print(f"\nMunicipality requested: {MUNICIPALITY_NAME}")
    print("Selecting municipality boundary...")

    # Create a temporary layer and select the requested municipality.
    municipality_layer = "municipality_selection_lyr"
    arcpy.management.MakeFeatureLayer(
        MUNICIPALITIES_SHP, municipality_layer
    )
    arcpy.management.SelectLayerByAttribute(
        municipality_layer, "NEW_SELECTION", where_clause
    )

    selected_count = int(arcpy.management.GetCount(municipality_layer)[0])

    if selected_count == 0:
        available_names = sorted({
            row[0] for row in arcpy.da.SearchCursor(
                MUNICIPALITIES_SHP, [MUNICIPALITY_FIELD]
            ) if row[0] is not None
        })
        raise ValueError(
            f"No municipality matched '{MUNICIPALITY_NAME}'.\n"
            "Check the spelling and spacing. Some available names are:\n"
            + ", ".join(available_names[:30])
        )

    if selected_count > 1:
        raise ValueError(
            f"The selection returned {selected_count} features. "
            "Please check whether MUNICNAME uniquely identifies the municipality."
        )

    print(f"Selected municipality boundary: {selected_count} feature")

    # Prepare output name and path.
    output_name = safe_filename(MUNICIPALITY_NAME) + "_Properties_Clip.shp"
    output_shapefile = os.path.join(OUTPUT_FOLDER, output_name)

    print("\nClipping property data...")
    print("This may take some time if the property dataset is large.")

    # Clip the properties using the selected municipality boundary.
    arcpy.analysis.Clip(
        in_features=PROPERTIES_SHP,
        clip_features=municipality_layer,
        out_feature_class=output_shapefile
    )

    output_count = int(arcpy.management.GetCount(output_shapefile)[0])

    print("\n" + "=" * 65)
    print("PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f"Municipality: {MUNICIPALITY_NAME}")
    print(f"Properties clipped: {output_count:,}")
    print(f"Output saved to:\n{output_shapefile}")
    print("=" * 65)

    # Clean up the temporary layer.
    arcpy.management.Delete(municipality_layer)

    # Add the output to the current ArcGIS Pro map, if run inside a Pro project.
    try:
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        current_map = aprx.activeMap
        if current_map is not None:
            current_map.addDataFromPath(output_shapefile)
            print("The clipped shapefile has also been added to the active map.")
    except Exception:
        # Running outside an open ArcGIS Pro project is fine.
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("\nPROCESS FAILED:")
        print(error)
        print("\nArcPy details:")
        print(arcpy.GetMessages(2))
        raise
