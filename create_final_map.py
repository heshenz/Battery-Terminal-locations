#!/usr/bin/env python3
"""
Create final map after research is complete.
NO CLUSTERING: Each battery location is a distinct small circle.
Terminal stations use red lightning in triangle icon, larger than battery markers.
WITH LIGHT/DARK MODE TOGGLE.
"""

import csv
import json
from datetime import datetime

print("="*60)
print("CREATING FINAL MAP WITH LIGHT/DARK MODE")
print("="*60)

# Read battery data
battery_file = "australia_battery_storage_with_coords.csv"
terminal_file = "all_australian_terminals.csv"

print(f"\n1. Reading {battery_file}...")
battery_data = []
with open(battery_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        battery_data.append(row)

print(f"   Loaded {len(battery_data)} battery projects")

print(f"\n2. Reading {terminal_file}...")
terminal_data = []
with open(terminal_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        terminal_data.append(row)

print(f"   Loaded {len(terminal_data)} terminal stations")

# Process battery data
battery_processed = []
valid_battery = 0
invalid_battery = 0
state_counter = {}

for row in battery_data:
    title = row.get('title', 'Unknown').strip()
    status = row.get('status', 'Unknown').strip()
    state = row.get('state', 'Unknown').strip()
    size_mw = row.get('size_mw', '').strip()
    size_mwh = row.get('size_mwh', '').strip()
    lat = row.get('latitude', '').strip()
    lon = row.get('longitude', '').strip()
    
    # Count states
    state_counter[state] = state_counter.get(state, 0) + 1
    
    if lat and lon:
        try:
            lat_val = float(lat)
            lon_val = float(lon)
            
            # Check if not placeholder
            if not (-26 < lat_val < -24 and 134 < lon_val < 136):
                # Status colors
                status_colors = {
                    'Operating': '#4CAF50',
                    'Construction': '#FF9800',
                    'Announced': '#2196F3',
                    'Proposed': '#9C27B0',
                    'Unknown': '#9E9E9E'
                }
                
                battery_processed.append({
                    'title': title,
                    'status': status,
                    'color': status_colors.get(status, '#9E9E9E'),
                    'size_mw': float(size_mw) if size_mw.replace('.', '', 1).isdigit() else None,
                    'size_mwh': float(size_mwh) if size_mwh.replace('.', '', 1).isdigit() else None,
                    'state': state,
                    'lat': lat_val,
                    'lon': lon_val
                })
                valid_battery += 1
            else:
                invalid_battery += 1
        except:
            invalid_battery += 1
    else:
        invalid_battery += 1

print(f"\n3. Battery data processed:")
print(f"   Valid projects (on map): {valid_battery}")
print(f"   Invalid/missing: {invalid_battery}")
print(f"   Coverage: {valid_battery}/{len(battery_data)} ({valid_battery/len(battery_data)*100:.1f}%)")

print(f"\n   State distribution:")
for state, count in sorted(state_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"     {state}: {count}")

# Process terminal data
terminal_processed = []
for row in terminal_data:
    name = row.get('name', 'Unknown').strip()
    state = row.get('state', 'Unknown').strip()
    voltage = row.get('voltagekv', 'Unknown').strip()
    status = row.get('operationalstatus', 'Unknown').strip()
    x = row.get('X', '').strip()
    y = row.get('Y', '').strip()
    
    if x and y:
        try:
            lon = float(x)
            lat = float(y)
            terminal_processed.append({
                'name': name,
                'state': state,
                'voltage': voltage,
                'status': status,
                'lat': lat,
                'lon': lon
            })
        except:
            pass

print(f"\n4. Terminal data processed:")
print(f"   Valid stations: {len(terminal_processed)}/{len(terminal_data)}")

# Create HTML
print(f"\n5. Creating HTML map with light/dark mode...")

html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Australian Battery Storage & Terminal Stations</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            transition: background-color 0.3s, color 0.3s;
        }}
        
        /* Light mode (default) */
        body.light-mode {{
            background-color: #f5f5f5;
            color: #333;
        }}
        
        /* Dark mode */
        body.dark-mode {{
            background-color: #121212;
            color: #e0e0e0;
        }}
        
        body.dark-mode #map {{
            filter: brightness(0.8) contrast(1.2);
        }}
        
        #map {{
            width: 100%;
            height: 100vh;
            transition: filter 0.3s;
        }}
        
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 300px;
            transition: background-color 0.3s, color 0.3s;
        }}
        
        .light-mode #info {{
            background: white;
            color: #333;
        }}
        
        .dark-mode #info {{
            background: #1e1e1e;
            color: #e0e0e0;
        }}
        
        .legend {{
            position: absolute;
            bottom: 10px;
            left: 10px;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            transition: background-color 0.3s, color 0.3s;
        }}
        
        .light-mode .legend {{
            background: white;
            color: #333;
        }}
        
        .dark-mode .legend {{
            background: #1e1e1e;
            color: #e0e0e0;
        }}
        
        .legend-item {{
            margin: 5px 0;
            display: flex;
            align-items: center;
        }}
        
        .legend-color {{
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 8px;
            display: inline-block;
        }}
        
        .stats {{
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 300px;
            transition: background-color 0.3s, color 0.3s;
        }}
        
        .light-mode .stats {{
            background: white;
            color: #333;
        }}
        
        .dark-mode .stats {{
            background: #1e1e1e;
            color: #e0e0e0;
        }}
        
        .terminal-marker-triangle {{
            background: red;
            color: white;
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-bottom: 26px solid red;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        
        .terminal-marker-triangle i {{
            position: absolute;
            top: 5px;
            color: white;
            font-size: 14px;
        }}
        
        .battery-marker {{
            border-radius: 50%;
            opacity: 0.8;
        }}
        
        /* Dark mode toggle button */
        .mode-toggle {{
            position: absolute;
            top: 10px;
            right: 320px; /* Position to the left of stats */
            background: #4CAF50;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 5px;
            cursor: pointer;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: background-color 0.3s;
        }}
        
        .mode-toggle:hover {{
            background: #45a049;
        }}
        
        .dark-mode .mode-toggle {{
            background: #333;
        }}
        
        .dark-mode .mode-toggle:hover {{
            background: #444;
        }}
        
        /* Dark mode specific styles for map controls */
        .dark-mode .leaflet-control {{
            background: #1e1e1e;
            color: #e0e0e0;
        }}
        
        .dark-mode .leaflet-control a {{
            color: #e0e0e0;
        }}
        
        .dark-mode .leaflet-control-layers {{
            background: #1e1e1e;
            color: #e0e0e0;
        }}
        
        .dark-mode .leaflet-control-layers label {{
            color: #e0e0e0;
        }}
        
        .dark-mode .leaflet-control-layers input {{
            accent-color: #4CAF50;
        }}
        
        /* Popup styling for dark mode */
        .dark-mode .leaflet-popup-content-wrapper {{
            background: #1e1e1e;
            color: #e0e0e0;
        }}
        
        .dark-mode .leaflet-popup-tip {{
            background: #1e1e1e;
        }}
        
        .dark-mode .leaflet-popup-close-button {{
            color: #e0e0e0;
        }}
    </style>
</head>
<body class="light-mode">
    <div id="map"></div>
    
    <!-- Dark mode toggle button -->
    <button class="mode-toggle" id="modeToggle">
        <i class="fas fa-moon"></i> Dark Mode
    </button>
    
    <div id="info">
        <h3>Australian Battery Storage</h3>
        <p><strong>Battery Projects:</strong> {valid_battery}</p>
        <p><strong>Terminal Stations:</strong> {len(terminal_processed)}</p>
        <p><small>Click markers for details</small></p>
        <p><small><i class="fas fa-bolt" style="color:red;"></i> Terminal stations are highlighted in red</small></p>
    </div>
    
    <div class="stats">
        <h4>Data Coverage</h4>
        <p>Battery projects: {valid_battery}/{len(battery_data)} ({valid_battery/len(battery_data)*100:.1f}%)</p>
        <p>Terminal stations: {len(terminal_processed)}/{len(terminal_data)}</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    
    <div class="legend">
        <h4>Legend</h4>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #4CAF50;"></div>
            <span>Operating Battery</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #FF9800;"></div>
            <span>Construction Battery</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #2196F3;"></div>
            <span>Announced Battery</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #9C27B0;"></div>
            <span>Proposed Battery</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #9E9E9E;"></div>
            <span>Unknown Status</span>
        </div>
        <div class="legend-item">
            <div style="width: 20px; height: 20px; margin-right: 8px; position: relative;">
                <div style="width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-bottom: 17px solid red;"></div>
                <i class="fas fa-bolt" style="position: absolute; top: 2px; left: 5px; color: white; font-size: 10px;"></i>
            </div>
            <span><strong>Terminal Station</strong> (Red Triangle)</span>
        </div>
        <div class="legend-item">
            <div style="width: 20px; height: 20px; margin-right: 8px; display: flex; align-items: center; justify-content: center;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #4CAF50;"></div>
            </div>
            <span><small>Battery markers: Small distinct circles</small></span>
        </div>
    </div>

    <script>
        // Battery data
        const batteryData = {json.dumps(battery_processed)};
        
        // Terminal data
        const terminalData = {json.dumps(terminal_processed)};
        
        // Initialize map
        const map = L.map('map').setView([-25, 135], 4);
        
        // Add tile layers for light and dark mode
        const lightTiles = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18,
            name: 'Light Map'
        }});
        
        const darkTiles = L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors, © CARTO',
            maxZoom: 18,
            name: 'Dark Map'
        }});
        
        // Start with light tiles
        lightTiles.addTo(map);
        
        // Create custom terminal icon (red triangle with lightning bolt)
        const TerminalIcon = L.DivIcon.extend({{
            options: {{
                html: `
                    <div class="terminal-marker-triangle">
                        <i class="fas fa-bolt"></i>
                    </div>
                `,
                iconSize: [30, 30],
                iconAnchor: [15, 26],
                popupAnchor: [0, -26],
                className: 'terminal-icon-marker'
            }}
        }});
        
        // Add battery projects as SMALL DISTINCT CIRCLES (no clustering)
        const batteryLayer = L.layerGroup();
        batteryData.forEach(project => {{
            const marker = L.circleMarker([project.lat, project.lon], {{
                radius: 5,  // Small distinct circles
                color: project.color,
                fillColor: project.color,
                fillOpacity: 0.7,
                weight: 1,
                className: 'battery-marker'
            }});
            
            const sizeInfo = project.size_mw ? 
                `<p><strong>Size:</strong> ${{project.size_mw}} MW${{project.size_mwh ? ' / ' + project.size_mwh + ' MWh' : ''}}</p>` : 
                '';
            
            marker.bindPopup(`
                <div style="max-width: 300px;">
                    <h4>${{project.title}}</h4>
                    <p><strong>Status:</strong> ${{project.status}}</p>
                    ${{sizeInfo}}
                    <p><strong>State:</strong> ${{project.state}}</p>
                    <p><small>Coordinates: ${{project.lat.toFixed(4)}}, ${{project.lon.toFixed(4)}}</small></p>
                </div>
            `);
            
            batteryLayer.addLayer(marker);
        }});
        
        // Add battery layer to map
        map.addLayer(batteryLayer);
        
        // Add terminal stations with custom icon (larger and more visible)
        const terminalLayer = L.layerGroup();
        terminalData.forEach(station => {{
            const icon = new TerminalIcon();
            
            const marker = L.marker([station.lat, station.lon], {{
                icon: icon,
                zIndexOffset: 1000  // Make terminals appear above batteries
            }});
            
            marker.bindPopup(`
                <div style="max-width: 300px;">
                    <h4><i class="fas fa-bolt" style="color:red;"></i> ${{station.name}}</h4>
                    <p><strong>Type:</strong> Terminal Station</p>
                    <p><strong>State:</strong> ${{station.state}}</p>
                    <p><strong>Voltage:</strong> ${{station.voltage}} kV</p>
                    <p><strong>Status:</strong> ${{station.status}}</p>
                    <p><small>Coordinates: ${{station.lat.toFixed(4)}}, ${{station.lon.toFixed(4)}}</small></p>
                </div>
            `);
            
            // Add hover effect
            marker.on('mouseover', function() {{
                this.openPopup();
            }});
            
            terminalLayer.addLayer(marker);
        }});
        
        // Add terminal layer to map
        map.addLayer(terminalLayer);
        
        // Fit bounds to show all markers
        if (batteryData.length > 0 || terminalData.length > 0) {{
            const bounds = L.latLngBounds(
                batteryData.concat(terminalData).map(item => [item.lat, item.lon])
            );
            map.fitBounds(bounds.pad(0.1));
        }}
        
        // Add layer control
        const overlayMaps = {{
            "Battery Projects (Small Circles)": batteryLayer,
            "Terminal Stations (Red Triangles)": terminalLayer
        }};
        
        const baseMaps = {{
            "Light Map": lightTiles,
            "Dark Map": darkTiles
        }};
        
        L.control.layers(baseMaps, overlayMaps, {{ collapsed: false }}).addTo(map);
        
        // Add zoom control
        L.control.zoom({{ position: 'topright' }}).addTo(map);
        
        // Add scale control
        L.control.scale({{ imperial: false, position: 'bottomleft' }}).addTo(map);
        
        // Dark mode toggle functionality
        const modeToggle = document.getElementById('modeToggle');
        const body = document.body;
        
        // Check for saved preference
        const savedMode = localStorage.getItem('mapMode');
        if (savedMode === 'dark') {{
            enableDarkMode();
        }}
        
        modeToggle.addEventListener('click', function() {{
            if (body.classList.contains('dark-mode')) {{
                disableDarkMode();
            }} else {{
                enableDarkMode();
            }}
        }});
        
        function enableDarkMode() {{
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            darkTiles.addTo(map);
            lightTiles.remove();
            modeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
            localStorage.setItem('mapMode', 'dark');
        }}
        
        function disableDarkMode() {{
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            lightTiles.addTo(map);
            darkTiles.remove();
            modeToggle.innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
            localStorage.setItem('mapMode', 'light');
        }}
        
        console.log(`Map loaded with ${{batteryData.length}} battery projects and ${{terminalData.length}} terminal stations`);
        console.log(`NO CLUSTERING: Each battery location is a distinct small circle`);
        console.log(`Light/Dark mode toggle enabled`);
    </script>
</body>
</html>'''

# Save HTML
output_file = "FINAL_COMPLETE_MAP.html"
with open(output_file, "w") as f:
    f.write(html)

print(f"   ✓ Created {output_file}")

# Create summary
summary = {
    "generated": datetime.now().isoformat(),
    "battery_projects": {
        "total": len(battery_data),
        "with_valid_coordinates": valid_battery,
        "coverage_percentage": round(valid_battery/len(battery_data)*100, 1),
        "state_distribution": state_counter
    },
    "terminal_stations": {
        "total": len(terminal_data),
        "with_coordinates": len(terminal_processed)
    },
    "map_features": {
        "battery_marker_size": "5px radius (small distinct circles)",
        "terminal_marker": "red triangle with lightning bolt (30px)",
        "clustering": "DISABLED - each battery is a distinct marker",
        "layer_control": "enabled with light/dark base maps",
        "dark_mode": "enabled with toggle button",
        "visualization": "Terminal stations are larger and more visible than battery markers"
    }
}

summary_file = "final_map_summary.json"
with open(summary_file, "w") as f:
    json.dump(summary, f, indent=2)

print(f"   ✓ Created {summary_file}")

print("\n" + "="*60)
print("FINAL MAP WITH LIGHT/DARK MODE CREATED!")
print("="*60)
print(f"""
To view the map:
  xdg-open {output_file}

KEY FEATURES:
  • Terminal stations use RED TRIANGLE with lightning bolt icon
  • Terminal markers are LARGER (30px) than battery markers
  • Battery markers are SMALL DISTINCT CIRCLES (5px radius)
  • NO CLUSTERING - each battery location is individually visible
  • LIGHT/DARK MODE TOGGLE - switch between light and dark themes
  • Dark mode uses CartoDB dark tiles
  • Mode preference saved in localStorage
  • Terminal markers have Z-INDEX priority (appear above batteries)
  • Layer control added to toggle battery/terminal visibility
  • Hover effects on terminal markers

Summary:
  Battery projects: {valid_battery}/{len(battery_data)} ({valid_battery/len(battery_data)*100:.1f}%)
  Terminal stations: {len(terminal_processed)}/{len(terminal_data)}
  Total markers: {valid_battery + len(terminal_processed)}

Files created:
  - {output_file}
  - {summary_file}

The map shows all projects with valid coordinates.
Projects with placeholder coordinates are excluded.
Terminal stations are HIGHLY VISIBLE with red triangle markers.
Battery locations are SMALL DISTINCT CIRCLES (no clustering).
""")