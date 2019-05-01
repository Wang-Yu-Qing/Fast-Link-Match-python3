import geopandas as gpd
import pandas as pd

data = gpd.read_file('link/shenzhen_mars.shp')
result = []
for row in data.values.tolist():
    points = str(row[-1])
    i, j = points.index('('), points.index(')')
    points = points[i+1:j]
    points = [result.append(point.split(' ')) for point in points.split(', ')]
result = pd.DataFrame(result, columns = ['lon', 'lat'])
result.to_csv('test.csv', index = False, header = True)
