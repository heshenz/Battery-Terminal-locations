#!/bin/bash

echo "Australian Battery Storage & Terminal Stations Project"
echo "======================================================"
echo ""

echo "Step 1: Installing dependencies..."
pip3 install pandas

echo ""
echo "Step 2: Updating coordinates..."
python3 update_coords_FINAL.py

echo ""
echo "Step 3: Creating interactive map..."
python3 create_final_map.py

echo ""
echo "Step 4: Opening map in browser..."
if [ -f "FINAL_COMPLETE_MAP.html" ]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open FINAL_COMPLETE_MAP.html &
    elif command -v open &> /dev/null; then
        open FINAL_COMPLETE_MAP.html &
    else
        echo "Please open FINAL_COMPLETE_MAP.html in your web browser."
    fi
else
    echo "ERROR: FINAL_COMPLETE_MAP.html not created!"
fi

echo ""
echo "Done! Check the following files:"
echo "  - australia_battery_storage_UPDATED.csv (updated data)"
echo "  - FINAL_COMPLETE_MAP.html (interactive map)"
echo "  - final_map_summary.json (statistics)"