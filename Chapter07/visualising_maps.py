import matplotlib.pyplot as plt
import matplotlib.cm as cm
import fiona

# STEP 2
COUNTRIES_POPULATION = {
    'Spain': 47.2,
    'Portugal': 10.6,
    'United Kingdom': 63.8,
    'Ireland': 4.7,
    'France': 64.9,
    'Italy': 61.1,
    'Germany': 82.6,
    'Netherlands': 16.8,
    'Belgium': 11.1,
    'Denmark': 5.6,
    'Slovenia': 2,
    'Austria': 8.5,
    'Luxembourg': 0.5,
    'Andorra': 0.077,
    'Switzerland': 8.2,
    'Liechtenstein': 0.038,
}
MAX_POPULATION = max(COUNTRIES_POPULATION.values())
MIN_POPULATION = min(COUNTRIES_POPULATION.values())

# STEP 3
colormap = cm.get_cmap('Greens')
COUNTRY_COLOUR = {
    country_name: colormap(
        (population - MIN_POPULATION) / (MAX_POPULATION - MIN_POPULATION)
    )
    for country_name, population in COUNTRIES_POPULATION.items()
}

# STEP 4
with fiona.open('europe.geojson') as fd:
    full_data = [data for data in fd]

# STEP 5
full_data = [data for data in full_data
             if data['properties']['NAME'] in COUNTRIES_POPULATION]

for data in full_data:
    country_name = data['properties']['NAME']
    colour = COUNTRY_COLOUR[country_name]

    # Draw the ISO3 code of each country
    long, lat = data['properties']['LON'], data['properties']['LAT']
    iso3 = data['properties']['ISO3']
    plt.text(long, lat, iso3, horizontalalignment='center')

    geo_type = data['geometry']['type']
    if geo_type == 'Polygon':
        data_x = [x for x, y in data['geometry']['coordinates'][0]]
        data_y = [y for x, y in data['geometry']['coordinates'][0]]
        plt.fill(data_x, data_y, c=colour)
        # Draw a line surrounding the area
        plt.plot(data_x, data_y, c='black', linewidth=0.2)
    elif geo_type == 'MultiPolygon':
        for coordinates in data['geometry']['coordinates']:
            data_x = [x for x, y in coordinates[0]]
            data_y = [y for x, y in coordinates[0]]
            plt.fill(data_x, data_y, c=colour)
            # Draw a line surrounding the area
            plt.plot(data_x, data_y, c='black', linewidth=0.2)

# Set the background to light blue
axes = plt.gca()
axes.set_facecolor('xkcd:light blue')
# Set the proper aspect to avoid distorsions
axes.set_aspect('equal', adjustable='box')
# Remove labels from axes
plt.xticks([])
plt.yticks([])

# STEP 6
plt.show()
