from Grid import Grid
import math
import geopandas as gpd

class GridMatrix(object):
    def __init__(self, linkShpFile, IDIndex, geoIndex, widthCoe, encoding):
        parseResult = self.parse_shp(linkShpFile, encoding = encoding)
        self.gridWidth = parseResult['gridWidth']/widthCoe
        self.grids = []
        self.minX, self.maxX = parseResult['minX'], parseResult['maxX']
        self.minY, self.maxY = parseResult['minY'], parseResult['maxY']
        self.nCols = math.ceil((self.maxX - self.minX)/self.gridWidth)
        self.nRows = math.ceil((self.maxY - self.minY)/self.gridWidth)
        print('Init GridMatrix with {}*{} grids with width of {}...'.format(self.nCols, self.nRows, self.gridWidth))
        self.init_grids()
        self.add_grid_neighbours()
        print('Forming point-link relation...')
        self.form_point_link_relation(IDIndex, geoIndex)
        print('Forming grid-link relation...')
        self.form_grid_link_relation()
        print('Init success.')

    def init_grids(self):
        for colIndex in range(self.nCols):
            col = []
            X = self.minX + colIndex * self.gridWidth
            for rowIndex in range(self.nRows):
                Y = self.minY + rowIndex * self.gridWidth
                col.append(Grid((X, Y), self.gridWidth))
            self.grids.append(col)

    def add_grid_neighbours(self):
        for colIndex in range(self.nCols):
            for rowIndex in range(self.nRows):
                neighbours = []
                # left
                if colIndex > 0:
                    neighbours.append(self.grids[colIndex - 1][rowIndex])
                # top
                if rowIndex < self.nRows - 1:
                    neighbours.append(self.grids[colIndex][rowIndex + 1])
                # right
                if colIndex < self.nCols - 1:
                    neighbours.append(self.grids[colIndex + 1][rowIndex])
                # down 
                if rowIndex > 0:
                    neighbours.append(self.grids[colIndex][rowIndex - 1])
                # top left diag:
                if colIndex > 0 and rowIndex < self.nRows - 1:
                    neighbours.append(self.grids[colIndex - 1][rowIndex + 1])
                # top right diag:
                if colIndex < self.nCols - 1 and rowIndex < self.nRows - 1:
                    neighbours.append(self.grids[colIndex + 1][rowIndex + 1])
                # down right diag:
                if colIndex < self.nCols - 1 and rowIndex > 0:
                    neighbours.append(self.grids[colIndex - 1][rowIndex - 1])
                # down left diag:
                if colIndex > 0 and rowIndex > 0:
                    neighbours.append(self.grids[colIndex - 1][rowIndex - 1])
                self.grids[colIndex][rowIndex].add_neighbours(neighbours)

    def show(self):
        for col in self.grids:
            for grid in reversed(col):
                print(grid)

    def parse_shp(self, linkShpFile, encoding):
        print('Reading link shp file...')
        self.links = gpd.read_file(linkShpFile, encoding = encoding)
        print('Parsing shp file...')
        # find minX, maxX, minY, maxY, maxLineLength
        minX, minY = float('Inf'), float('Inf')
        maxX, maxY, maxLineLength = float('-Inf'), float('-Inf'), float('-Inf')
        for link in self.links.values.tolist():
            linkGeo = link[-1]
            if linkGeo.length > maxLineLength:
                maxLineLength = linkGeo.length
            coords = linkGeo.coords
            corsX = [x[0] for x in coords]
            corsY = [x[1] for x in coords]
            for i in range(len(coords)):
                if corsX[i] > maxX:
                    maxX = corsX[i]
                if corsX[i] < minX:
                    minX = corsX[i]
                if corsY[i] > maxY:
                    maxY = corsY[i]
                if corsY[i] < minY:
                    minY = corsY[i]
        #print({'gridWidth':maxLineLength, 'minX':minX, 'maxX':maxX, 'minY':minY, 'maxY':maxY})
        return {'gridWidth':maxLineLength, 'minX':minX, 'maxX':maxX, 'minY':minY, 'maxY':maxY}
    
    def form_point_link_relation(self, IDIndex, geoIndex):
        self.pointLinkRelation = {}
        for link in self.links.values.tolist():
            linkID, linkGeo = link[IDIndex], link[geoIndex]
            points = linkGeo.coords
            points = [str(point) for point in points]
            # add this link to all its points' connected links
            for point in points:
                try:
                    self.pointLinkRelation[point].append((linkID, linkGeo))
                except KeyError:
                    self.pointLinkRelation[point] = [(linkID, linkGeo)]
    
    def form_grid_link_relation(self):
        for point, connectedLinks in self.pointLinkRelation.items():
            # find the grid it belongs to
            x, y = point.split(',')
            x, y = float(x[1:]), float(y[:-1])
            indexX, indexY = math.floor((x - self.minX)/self.gridWidth), math.floor((y - self.minY)/self.gridWidth)
            belongGrid = self.grids[indexX][indexY]
            # add all its connected links to this grid
            belongGrid.add_links(connectedLinks)


if __name__ == '__main__':
    GM = GridMatrix('link/shenzhen_mars.shp', 0, -1, 4, 'gbk')
    