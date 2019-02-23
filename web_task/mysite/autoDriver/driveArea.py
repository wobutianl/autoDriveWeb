from shapely.geometry import Polygon, Point
areaA = Polygon([(0, 0), (1, 1), (1, 0)])
areaB = Polygon([(0, 0), (1, 1), (1, 0)])

# the two parts of dock much match one to one
dock1 = Point(0,0)
dock2 = Point(2,2)

dock21 = Point(0,0)
dock22 = Point(2,2)

dockPoint =[[dock1, dock2],[dock21, dock22]]


