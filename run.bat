@echo off
echo Australian Battery Storage & Terminal Stations Project
echo ======================================================
echo.

echo Step 1: Installing dependencies...
pip install pandas

echo.
echo Step 2: Updating coordinates...
python update_coords_FINAL.py

echo.
echo Step 3: Creating interactive map...
python create_final_map.py

echo.
echo Step 4: Opening map in browser...
if exist FINAL_COMPLETE_MAP.html (
    start FINAL_COMPLETE_MAP.html
    echo Map opened in default browser.
) else (
    echo ERROR: FINAL_COMPLETE_MAP.html not created!
)

echo.
echo Done! Check the following files:
echo   - australia_battery_storage_UPDATED.csv (updated data)
echo   - FINAL_COMPLETE_MAP.html (interactive map)
echo   - final_map_summary.json (statistics)
echo.
pause