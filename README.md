# gis-property-automation
Automated spatial property extraction and municipal analysis using Python, ArcPy and ArcGIS Pro.
# Municipal Property GIS Automation System

**Python | ArcPy | SQL | ArcGIS Pro | OpenPyXL**

## Project Overview

An automated geospatial data processing and quality assurance system designed to streamline municipal property extraction, spatial clipping, data cleaning, property identification and management reporting.

The project was developed to address repetitive GIS workflows by transforming manual spatial processing tasks into a reusable ArcGIS Pro Python Toolbox.

## Business Problem

Manual municipal property extraction involves several repetitive processes, including selecting municipal boundaries, clipping property datasets, removing unapproved and unregistered properties, identifying duplicate property references and preparing statistical reports.

These processes can be time-consuming and susceptible to human error.

This project provides an automated, scalable and repeatable solution.

## Project Objectives

- Automate municipal property extraction.
- Enable single and batch municipality processing.
- Implement automated property data cleaning.
- Identify duplicate and missing property identifiers.
- Calculate unique property counts.
- Generate automated CSV and Excel reports.
- Improve data quality and operational efficiency.
- Reduce manual GIS processing.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Automation and business logic |
| ArcPy | Geospatial processing |
| ArcGIS Pro | GIS environment and custom toolbox |
| SQL | Attribute filtering |
| OpenPyXL | Excel reporting and visualisation |
| GitHub | Version control and documentation |

## Key Features

- Custom ArcGIS Pro Python Toolbox.
- Dynamic municipality selection.
- Multiple municipality batch processing.
- Automated spatial clipping.
- Case-insensitive attribute cleaning.
- Unique property identification using RDS numbers.
- Duplicate and missing identifier detection.
- Automated numerical reconciliation.
- CSV quality assurance reports.
- Excel management dashboard with charts.
- Existing output protection.
- Preservation of original source datasets.

## System Workflow

1. Load municipal boundaries and property datasets.
2. Dynamically retrieve municipality names.
3. Select one or multiple municipalities.
4. Clip property features to municipal boundaries.
5. Apply property data cleaning rules.
6. Calculate unique property identifiers.
7. Identify duplicate and missing identifiers.
8. Perform quality assurance checks.
9. Export cleaned spatial datasets.
10. Generate CSV and Excel management reports.

## Data Cleaning and Quality Assurance

The system applies configurable processing logic based on property descriptions and reference identifiers.

Unapproved and unregistered property records are excluded from the cleaned dataset.

Duplicate identifiers are reported without automatically deleting their associated geometries.

Missing identifiers are retained and flagged for further investigation.

The system verifies the following relationships:

- Original records = Cleaned records + Excluded records
- Cleaned records = Unique identifiers + Additional duplicate records + Missing identifiers

## Automated Reporting

The Excel reporting module generates six worksheets:

- Dashboard
- Municipal Summary
- Cleaning Statistics
- Duplicate RDS
- Missing RDS
- QA Checks

The management dashboard provides property statistics, retention rates, processing statuses and comparative charts.

## Installation and Usage

### Requirements

- ArcGIS Pro
- Python with ArcPy
- OpenPyXL
- Municipal boundary dataset
- Property polygon dataset

### Instructions

1. Clone or download this repository.
2. Open ArcGIS Pro.
3. Navigate to the Catalog pane.
4. Right-click Toolboxes and select Add Toolbox.
5. Select Municipal_Property_Tools_V4.pyt.
6. Open the Extract Clean and Count Properties tool.
7. Specify the input datasets, municipalities and output folder.
8. Run the tool.
9. Review the generated spatial datasets and management reports.

## Development History

| Version | Development milestone |
|---|---|
| V1.0 | Single municipality spatial clipping |
| V2.0 | Batch municipality processing |
| V2.1 | Dynamic parameter improvements |
| V2.2 | Multivalue parameter validation fix |
| V3.0 | Automated cleaning and property quality assurance |
| V4.0 | Excel reporting and management dashboard |

## Skills Demonstrated

- Geospatial data engineering
- Spatial ETL development
- Python programming
- GIS process automation
- SQL attribute queries
- Object-oriented programming
- Software debugging
- Data cleaning and transformation
- Data quality assurance
- Automated business intelligence reporting

## Future Enhancements

- Flexible existing output management.
- Advanced geometry validation.
- Spatial topology checks.
- SQL database integration.
- PostGIS integration.
- Interactive geospatial dashboards.
- Performance optimisation.
- Advanced spatial analytics.

## Data Privacy

This repository is intended to demonstrate geospatial automation and software development capabilities. Public or synthetic datasets should be used for demonstrations. Confidential organisational data is not included.

## Project Status

Version 4.0 — Successfully tested for single-municipality extraction, data cleaning, property counting and automated Excel reporting in ArcGIS Pro. Further multi-municipality testing is planned.

## Author

GIS Specialist | Aspiring Geospatial Data Scientist

Passionate about combining GIS, Python, SQL, spatial analytics and automation to develop practical, data-driven solutions.<img width="935" height="916" alt="image" src="https://github.com/user-attachments/assets/d74e9988-999e-40be-a997-0f7157c329be" />
