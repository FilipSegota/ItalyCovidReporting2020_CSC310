# ItalyCovidReporting2020_CSC310
## Info
**Author:**
Filip Segota  
**Class:**
CSC 320 (Advanced CS Topics-Big Data), Spring 2021  
**Assignment:**
Italy Covid Assignment

## Overview
Create a GUI application that will report data on COVID-19 infection by regions in Italy. The application will have two sections for selecting a region: dropdown menu and map. 
 - For the dropdown menu, we can select what region we want to see data on and click "Check Region". The pop-up window will appear with the total Italy population, region name, population, total covid cases, likelihood of increasing or decreasing, and percentage infected.
 - For a map, we can click on one of the regions and it will display data (region population, total covid cases, likelihood of increasing or decreasing, and percentage infected)
There is also an option to see the window in different languages (English, Italian, Spanish, and Chinese). There is a dropdown menu to select the language. This will change the text of the window not counting the map (The map won't be translated).  

**KNOWN ISSUE:** normal googletrans package 3.0.0 doesn't work and to get the translation to work, googletrans 3.1.0a0 or 4.0.0rc1 needs to be installed. GitHub discussion here: https://github.com/ssut/py-googletrans/issues/234#issuecomment-742460612.
