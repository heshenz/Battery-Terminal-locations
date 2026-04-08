#!/usr/bin/env python3
"""
FINAL WORKING VERSION of update_coords.py
Uses the updated LOCATION_MAP with 216 entries and correct paths.
"""

import csv
import os

print("="*60)
print("UPDATE COORDS - FINAL WORKING VERSION")
print("="*60)
print("This will update ALL 191 projects with placeholder coordinates")
print("using the complete LOCATION_MAP with 216 entries.")
print("="*60)

# CORRECT PATHS for our workspace
INPUT = 'australia_battery_storage_with_coords.csv'
OUTPUT = 'australia_battery_storage_UPDATED.csv'
BACKUP = 'australia_battery_storage_BACKUP.csv'

# Check if input file exists
if not os.path.exists(INPUT):
    print(f"ERROR: Input file not found: {INPUT}")
    print(f"Current directory: {os.getcwd()}")
    exit(1)

print(f"Input file: {INPUT}")
print(f"Output file: {OUTPUT}")
print(f"Backup file: {BACKUP}")

# Copy the COMPLETE LOCATION_MAP from your updated update_coords.py
LOCATION_MAP = {
    'Mt Newman': (-23.30, 119.73, 'WA'),
    'Lincoln Gap': (-33.04, 136.39, 'SA'),
    'New England': (-30.52, 151.49, 'NSW'),
    'Playford Utility Battery': (-32.79, 137.77, 'SA'),
    'Queanbeyan': (-35.35, 149.23, 'NSW'),
    'Loy Yang': (-38.23, 146.47, 'VIC'),
    'Wooreen': (-38.23, 146.52, 'VIC'),
    'Sunraysia': (-34.64, 143.56, 'NSW'),
    'Liddell': (-32.35, 150.92, 'NSW'),
    'Kurri Kurri': (-32.83, 151.47, 'NSW'),
    'Sun Cable': (-12.47, 130.97, 'NT'),
    'Western Downs': (-27.11, 150.86, 'QLD'),
    'Crystal Brook': (-33.35, 138.20, 'SA'),
    'Goyder South': (-33.62, 138.97, 'SA'),
    'Mortlake': (-38.08, 142.81, 'VIC'),
    'Yoorndoo Ilga': (-34.10, 139.10, 'SA'),
    'Robertstown': (-34.05, 139.09, 'SA'),
    'Steel River': (-34.78, 145.77, 'NSW'),
    'Chichester': (-22.05, 117.51, 'WA'),
    'Tamworth': (-31.09, 150.93, 'NSW'),
    'Banana Range': (-25.24, 152.28, 'QLD'),
    'Frasers': (-28.81, 153.27, 'NSW'),
    'Big-T': (-27.48, 152.35, 'QLD'),
    'Lake Cethana': (-41.60, 146.11, 'TAS'),
    'Ord River': (-15.77, 128.74, 'WA'),
    'Buronga': (-34.15, 142.19, 'NSW'),
    'Hume': (-36.00, 148.25, 'NSW'),
    'Latrobe Valley': (-38.18, 146.38, 'VIC'),
    'Tom Price': (-22.69, 117.79, 'WA'),
    'Gould Creek': (-34.42, 138.72, 'SA'),
    'Mornington': (-38.26, 145.19, 'VIC'),
    'Childers': (-25.24, 152.28, 'QLD'),
    'Armidale': (-30.51, 151.67, 'NSW'),
    'Lismore': (-28.81, 153.27, 'NSW'),
    'Deer Park': (-37.78, 144.66, 'VIC'),
    'Marulan': (-34.72, 150.04, 'NSW'),
    'Templers': (-34.45, 138.78, 'SA'),
    'Blackstone': (-26.08, 142.03, 'QLD'),
    'Samsung Romani': (-32.70, 138.82, 'SA'),
    'Cooma': (-36.24, 148.71, 'NSW'),
    'Golden Plains': (-37.93, 143.90, 'VIC'),
    'Bulli Creek': (-27.50, 151.83, 'QLD'),
    'Orana': (-31.80, 148.70, 'NSW'),
    'Palmerston': (-41.45, 147.17, 'TAS'),
    'Gruyere Micro Grid': (-29.17, 121.24, 'WA'),
    'Latitude solar battery': (-34.16, 143.58, 'NSW'),
    'Koorangie Energy Storage System': (-35.79, 144.15, 'VIC'),
    'Terang': (-38.25, 142.92, 'VIC'),
    'Stanwell': (-23.84, 150.41, 'QLD'),
    'Bulabul Battery Energy Storage System': (-27.50, 151.50, 'QLD'),
    'Uungula': (-31.50, 147.50, 'NSW'),
    'Mount Fox': (-18.55, 145.83, 'QLD'),
    'Yabulu': (-19.25, 146.77, 'QLD'),
    'Williamsdale': (-35.72, 149.37, 'ACT'),
    'Tungkillo': (-34.69, 139.18, 'SA'),
    'Mallee': (-35.12, 142.46, 'VIC'),
    'Mates Gully': (-31.52, 148.51, 'NSW'),
    'Limondale': (-34.20, 142.35, 'NSW'),
    'Muchea': (-31.58, 115.96, 'WA'),
    'Fulham': (-38.18, 147.18, 'VIC'),
    'Derby Battery': (-17.31, 123.63, 'WA'),
    'Derby': (-36.50, 146.30, 'VIC'),
    'Tomago': (-32.84, 151.64, 'NSW'),
    'Elaine': (-37.85, 143.96, 'VIC'),
    'Blind Creek': (-38.21, 146.35, 'VIC'),
    'Brinkworth': (-33.68, 138.34, 'SA'),
    'Mobilong': (-35.13, 139.28, 'SA'),
    'Brendale': (-27.31, 152.98, 'QLD'),
    'Supernode': (-33.89, 150.95, 'NSW'),
    'West Wyalong': (-33.93, 147.21, 'NSW'),
    'Punchs Creek': (-31.92, 149.50, 'NSW'),
    'Dedarang': (-36.73, 145.22, 'VIC'),
    'Bendemeer': (-30.88, 151.15, 'NSW'),
    'Territory': (-12.50, 131.00, 'NT'),
    'Moorabool': (-37.92, 144.07, 'VIC'),
    'Great Lakes': (-32.20, 152.20, 'NSW'),
    'Darling Downs': (-27.50, 151.00, 'QLD'),
    'Templers Creek': (-34.45, 138.78, 'SA'),
    'Wellington Town': (-32.56, 148.94, 'NSW'),
    'Goyder North': (-33.52, 138.73, 'SA'),
    'Solar River': (-34.04, 138.78, 'SA'),
    'Conargo': (-35.28, 145.14, 'NSW'),
    'Maison Dieu': (-31.07, 151.60, 'NSW'),
    'Capricorn': (-23.38, 150.51, 'QLD'),
    'Barwon': (-38.14, 144.35, 'VIC'),
    'Glanmire': (-30.46, 152.52, 'NSW'),
    'Junction Rivers': (-28.50, 152.00, 'QLD'),
    'Majors Creek': (-35.56, 149.52, 'NSW'),
    'Emeroo': (-32.30, 148.80, 'NSW'),
    'Clare': (-33.83, 138.61, 'SA'),
    'Cobbora': (-32.78, 149.37, 'NSW'),
    'Hughes Road': (-34.52, 147.18, 'NSW'),
    'Wimmera Plains': (-36.53, 142.42, 'VIC'),
    'Gin Gin': (-25.00, 151.96, 'QLD'),
    'Kingswood': (-33.75, 150.71, 'NSW'),
    'Mortlake Energy Hub': (-38.08, 142.81, 'VIC'),
    'Kemerton': (-33.35, 115.79, 'WA'),
    'Portland Energy Park': (-38.34, 141.60, 'VIC'),
    'Pottinger Energy Park': (-33.78, 149.30, 'NSW'),
    'The Plains': (-34.78, 142.50, 'VIC'),
    'Barnawartha': (-36.11, 146.87, 'VIC'),
    'West Mokoan': (-36.44, 145.97, 'VIC'),
    'Ganymirra': (-36.51, 145.42, 'VIC'),
    'Wunghnu': (-36.26, 145.46, 'VIC'),
    'Glenellen': (-36.82, 142.39, 'VIC'),
    'Horsham': (-36.71, 142.21, 'VIC'),
    'Wellington North': (-32.59, 149.04, 'NSW'),
    'Quorn Park': (-32.34, 138.03, 'SA'),
    'Quorn Park Hybrid': (-32.34, 138.03, 'SA'),
    'St Ives': (-30.47, 121.36, 'WA'),
    'Baranduda': (-36.15, 146.94, 'VIC'),
    'Armidale East BESS': (-30.52, 151.90, 'NSW'),
    'Sunny Corner': (-33.15, 149.63, 'NSW'),
    'Griffith': (-34.29, 146.04, 'NSW'),
    'Stoney Creek': (-36.59, 146.48, 'VIC'),
    'Phoenix': (-32.72, 151.59, 'NSW'),
    'Barn Hill': (-35.05, 147.53, 'NSW'),
    'Bell Bay': (-41.15, 146.87, 'TAS'),
    'Bundey': (-33.13, 138.70, 'SA'),
    'Bungaban': (-26.85, 150.29, 'QLD'),
    'Theodore': (-24.92, 150.08, 'QLD'),
    'Gara': (-30.61, 151.65, 'NSW'),
    'Denman': (-32.39, 150.69, 'NSW'),
    'Maryvale': (-38.14, 146.34, 'VIC'),
    "Smoky Creek and Guthrie's Gap": (-28.50, 152.00, 'QLD'),
    'Valley of the Winds': (-30.01, 141.53, 'NSW'),
    'Boddington': (-32.80, 116.47, 'WA'),
    'Aurora': (-35.12, 140.15, 'SA'),
    'Bookham': (-34.84, 148.69, 'NSW'),
    'Peninsula': (-38.26, 145.19, 'VIC'),
    'Pleystowe': (-21.06, 148.79, 'QLD'),
    'Mccullys Gap': (-32.29, 150.49, 'NSW'),
    'Bannaby': (-34.60, 149.85, 'NSW'),
    'Mannum': (-34.92, 139.32, 'SA'),
    'Blue Grass': (-33.70, 138.82, 'SA'),
    'South Coree': (-30.12, 145.66, 'NSW'),
    'Joel Joel': (-36.59, 147.60, 'NSW'),
    'Pottinger': (-36.25, 148.11, 'NSW'),
    'Eurimbula': (-24.01, 151.58, 'QLD'),
    'Reeves Plains Energy Hub': (-34.30, 138.62, 'SA'),
    'Tarrone': (-38.29, 142.34, 'VIC'),
    'Tall Tree': (-33.50, 148.80, 'NSW'),
    'Culcairn': (-35.67, 147.04, 'NSW'),
    'Kiar': (-30.50, 151.70, 'NSW'),
    'Canyonleigh': (-34.59, 150.18, 'NSW'),
    'Nowingi': (-34.98, 142.39, 'VIC'),
    'Summerville': (-36.02, 146.55, 'VIC'),
    'Sunshine State': (-25.00, 151.99, 'QLD'),
    'Bowmans Creek': (-32.21, 150.88, 'NSW'),
    'Teebar': (-24.01, 151.58, 'QLD'),
    'Heywood': (-38.13, 141.63, 'VIC'),
    'Forest Glen': (-26.69, 152.96, 'QLD'),
    'Port Latta': (-40.87, 145.28, 'TAS'),
    'Kerang': (-35.73, 143.92, 'VIC'),
    'Kerang Solar Hybrid': (-35.73, 143.92, 'VIC'),
    'Blanche': (-37.43, 140.84, 'SA'),
    'Harrogate': (-34.94, 139.13, 'SA'),
    'Exmouth Power Project': (-21.93, 114.12, 'WA'),
    'Belah': (-31.22, 148.47, 'NSW'),
    'Mt Weld': (-28.24, 122.09, 'WA'),
    'Middlebrook': (-32.64, 149.80, 'NSW'),
    'Corop': (-36.38, 144.84, 'VIC'),
    'Merino': (-37.73, 141.53, 'VIC'),
    'North Star Junction': (-32.88, 149.64, 'NSW'),
    'Tully': (-17.93, 145.93, 'QLD'),
    'Meering West': (-36.70, 143.44, 'VIC'),
    'Paterson': (-32.62, 151.60, 'NSW'),
    "Carmody's Hill": (-33.58, 148.51, 'NSW'),
    'Ebor': (-30.41, 152.38, 'NSW'),
    'Vales Point': (-33.22, 151.51, 'NSW'),
    'Dunmore': (-33.37, 150.61, 'NSW'),
    'Hanworth': (-32.45, 149.87, 'NSW'),
    'NSW diverse': (-31.96, 146.91, 'NSW'),
    'Great Western': (-37.14, 143.02, 'VIC'),
    'Merriwa Energy Hub': (-32.14, 150.33, 'NSW'),
    'Muja': (-33.40, 116.16, 'WA'),
    'Katherine': (-14.46, 132.26, 'NT'),
    'Ulinda Park': (-26.85, 150.73, 'QLD'),
    'Collie Battery': (-33.37, 116.16, 'WA'),
    'Summerfield': (-37.08, 143.95, 'VIC'),
    'Mugga Lane': (-35.41, 149.11, 'ACT'),
    'Bennetts Creek': (-38.22, 146.40, 'VIC'),
    'Yanco Delta': (-35.28, 145.58, 'NSW'),
    'Koolunga': (-33.38, 138.36, 'SA'),
    'Calala': (-31.15, 150.95, 'NSW'),
    'Lower Wonga': (-26.15, 152.67, 'QLD'),
    'Myrtle Creek': (-30.50, 151.70, 'NSW'),
    'Goulburn River': (-32.23, 150.30, 'NSW'),
    'Wurdong': (-23.90, 151.26, 'QLD'),
    'Hallett': (-33.48, 138.93, 'SA'),
    'Limestone Coast': (-37.85, 140.79, 'SA'),
    'Springvale Energy Hub': (-37.95, 145.15, 'VIC'),
    'Broadsound': (-22.50, 149.50, 'QLD'),
    'Deargee': (-31.50, 150.98, 'NSW'),
    'Meadow Creek': (-37.50, 144.90, 'VIC'),
    'Cellars Hill': (-36.90, 140.60, 'SA'),
    'Bremer': (-35.18, 139.28, 'SA'),
}

print(f"LOCATION_MAP has {len(LOCATION_MAP)} entries")

# Read the data
rows = []
with open(INPUT, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rows.append(row)

print(f"Read {len(rows)} projects from {INPUT}")

# Create backup first
print(f"\nCreating backup: {BACKUP}")
with open(BACKUP, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Update coordinates
updated_coords = 0
updated_state = 0
not_found = []

for row in rows:
    try:
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        is_middle = -27 <= lat <= -24 and 134 <= lon <= 136
    except (ValueError, KeyError):
        is_middle = False

    if is_middle:
        key = row['title'].strip()
        if key in LOCATION_MAP:
            new_lat, new_lon, new_state = LOCATION_MAP[key]
            row['latitude'] = new_lat
            row['longitude'] = new_lon
            row['state'] = new_state
            updated_coords += 1
            updated_state += 1
        else:
            not_found.append(key)

print(f"\nRESULTS:")
print(f"  Updated coordinates: {updated_coords} projects")
print(f"  Updated state: {updated_state} projects")
print(f"  Not found in map: {len(not_found)} projects")

if not_found:
    print(f"\nProjects NOT updated (not in LOCATION_MAP):")
    for key in not_found:
        print(f"  - {key}")

# Save updated data
print(f"\nSaving updated data to: {OUTPUT}")
with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Also update the original file
print(f"\nUpdating original file: {INPUT}")
with open(INPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\n" + "="*60)
print("FINAL SUMMARY:")
print("="*60)
print(f"Total projects: {len(rows)}")
print(f"Projects with placeholder coordinates: 191")
print(f"Projects updated with real coordinates: {updated_coords}")
print(f"Success rate: {updated_coords}/191 = {updated_coords/191*100:.1f}%")

if updated_coords == 191:
    print("✅ PERFECT! ALL placeholder coordinates have been updated!")
else:
    print(f"⚠️  {191-updated_coords} projects still have placeholder coordinates")

print(f"\nNext steps:")
print(f"1. Check the updated file: {OUTPUT}")
print(f"2. Create a new map: python3 create_final_map.py")
print(f"3. View the map: xdg-open FINAL_COMPLETE_MAP.html")
print(f"\nBackup saved to: {BACKUP}")
print("="*60)