from Grid import Grid
from GridMatrix import GridMatrix
import math
from shapely.geometry import Point

class LinkMatch(object):
    def __init__(self, shpFile, IDIndex, GeoIndex, widthCoe, encoding):
        self.GM = GridMatrix(shpFile, IDIndex, GeoIndex, widthCoe, encoding = encoding)
    
    def find_point_belongGrid(self, point):
        x, y = point[0], point[1]
        xIndex = math.floor((x - self.GM.minX)/self.GM.gridWidth)
        yIndex = math.floor((y - self.GM.minY)/self.GM.gridWidth)
        if xIndex < 0 or yIndex < 0:
            return 'point not in grid matrix area.'
        try:
            belongGrid = self.GM.grids[xIndex][yIndex]
            # return belong grid and its neighbours
            return [belongGrid] + belongGrid.neighbours
        except IndexError:
            return 'point not in grid matrix area.'

    @staticmethod
    def find_nearest_link(links, point):
        point = Point(point)
        # {linkID:distance}
        nearestLink = {'ID':None, 'distance':float('Inf')}
        for linkID, linkGeo in links:
            distance = point.distance(linkGeo)
            if distance < nearestLink['distance']:
                nearestLink['ID'] = linkID
                nearestLink['distance'] = distance
        return nearestLink

    @staticmethod
    def extract_links(grids):
        links = []
        for grid in grids:
            for link in grid.containedLinks:
                if link not in links:
                    links.append(link)
        if not links:
            return 'point\'s belonging grid and neighbours contains no link.'
        return links
    
    def match(self, point, unmatchedPoints = None):
        grids = self.find_point_belongGrid(point)
        potentialLinks = self.extract_links(grids)
        if isinstance(potentialLinks, list):
            nearestLink = self.find_nearest_link(potentialLinks, point)
            return nearestLink['ID']
        else:
            if unmatchedPoints is not None:
                unmatchedPoints.append(point)
            return -1

if __name__ == '__main__':
    LM = LinkMatch('link/shenzhen_mars.shp', 0, -1, 5, 'gbk')
    import pandas as pd
    testData = pd.read_csv('test.csv')
    total = len(testData)
    testData = testData.values.tolist()
    import time
    before = time.time()
    num = 0
    for row in testData:
        LM.match((row[0], row[1]))
        num += 1
        print(num, end = '\r')
    cost = time.time() - before
    print('{} points cost {} sec'.format(total, cost))