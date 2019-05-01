from shapely.geometry import Polygon

class Grid(object):
    def __init__(self, bottomLeft, w):
        self.x0, self.y0 = bottomLeft
        self.width = w
        self.points = [(self.x0, self.y0), (self.x0, self.y0 + w), 
                       (self.x0 + w, self.y0 + w), (self.x0 + w, self.y0)]
        self.geometry = Polygon(self.points)
        self.neighbours = []
        self.containedLinks = []

    def __repr__(self):
        return 'Grid:' + str(self.points[1]) + ', ' + str(self.points[2]) + '\n' + \
               '     ' + str(self.points[0]) + ', ' + str(self.points[3])

    def add_neighbours(self, neighbours):
        self.neighbours = neighbours

    def add_links(self, links):
        self.containedLinks += links




if __name__ == '__main__':
    g = Grid((0, 0), 2)
    print(g)
    
        