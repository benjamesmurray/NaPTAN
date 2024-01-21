1. **count.py**:
   - **Analysis**: Counts the total number of stops in the NaPTAN dataset.
   - **Naming Convention**: No file generated; results are printed. e.g. Total number of stops in the dataset: 437779

2. **count_FLX.py**:
   - **Analysis**: Counts the number of flexible (FLX) stops in the dataset.
   - **Naming Convention**: Two files generated to list and supply XML for all FLX stops:
     - Exported ATCO codes to bct_flx_atco_codes_20240121143455.csv
     - Exported matching stops to bct_flx_stops_20240121143455.xml

3. **deleted_common_name.py**:
   - **Analysis**: Identifies stops with deleted common names.
   - **Naming Convention**: Results are printed and CSV listing the ATCO codes generated.
     - Number of ATCO codes with 'DELETE' or variations in Descriptor's CommonName: 62
     - Exported data to atco_with_delete_20240121143724.csv

4. **duplicates.py**:
   - **Analysis**: Detects duplicate stop entries.
   - **Naming Convention**: Two CSV's for exported for NaPTAN and ATCO results.
     - Exported ATCO duplicates to atco_duplicates_20240121143842.csv
     - Exported NaPTAN duplicates to naptan_duplicates_20240121143842.csv

5. **flexiblezone_stoptype.py**:
   - **Analysis**: Analyzes stops by type, focusing on flexible zones to see if any stops other than FLX have a flexiblezone element.
   - **Naming Convention**: 'CSV for exported data.
     - Exported data to bus_stop_type_with_flexible_zone_20240121144043.csv

6. **FLX_LL_vs_NE.py**:
   - **Analysis**: Reviews whether the locations within FLX stops are presented as Easting Northing, Lat Long or both.
   - **Naming Convention**: CSV exported:
     - Exported data to flexible_zone_positions_20240121144204.csv

7. **FLX_zone_count.py**:
   - **Analysis**: Counts stops within each flexible zone.
   - **Naming Convention**: Exports counts and the codes in two CSV's:
     - Exported counts data to flexible_zones_counts_20240121144410.csv
     - Exported ATCO codes data to flexible_zones_atco_codes_20240121144410.csv

8. **inactive.py**:
   - **Analysis**: Identifies inactive stops in the dataset.
   - **Naming Convention**: No file generated; results are printed. e.g. Number of inactive stops: 51165

9. **missing_naptan_code.py**:
    - **Analysis**: Searches for stops missing a NaPTAN code.
    - **Naming Convention**: Two CSV's generated:
      - Exported counts to atco_with_no_naptan_by_type_20240121144646.csv
      - Exported details to atco_with_no_naptan_details_20240121144646.csv

10. **single_stop.py**:
   - **Analysis**: Analyzes data for a single stop based on its ATCO code.
   - **Naming Convention**: A single .txt file generated for that stop.

11. **zero_coords.py**:
   - **Analysis**: Identifies stops in the dataset with coordinates set to zero.
   - **Naming Convention**: Two files created to list and supply details of each stop with zero coords.
     - invalid_stops_20240121144855.csv
     - invalid_stops_20240121144855.xml

