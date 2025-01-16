from math import sqrt, isclose

class Receiver():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Tracker():
    def __init__(self, id, x = 0, y = 0):
        # Initialize the tracker at an impossible (physical) position 
        # that could be inside a wall or outside the building (0, 0)
        self.id = id
        self.__x = x
        self.__y = y

    def report(self, receiver):
        # This function will return the relative distance between
        # the current tracker and the pointed receiver
        return self.__measure_distance(self.__x, self.__y, receiver.x, receiver.y)
    
    def move_to(self, new_x, new_y):
        # Simulate tracker moving to another position
        self.__x = new_x
        self.__y = new_y

    def find_position(self, receivers):
        # First of all, check if there are at least 3 receivers avalable
        if len(receivers) < 3:
            raise ValueError("Not enough receibers, there should be al least 3.")        
        
        # Report to all the receivers and put the measures on a list
        loc = []
        for rec_id, rec in receivers.items():
            dist = self.report(rec)
            loc.append((dist, rec.x, rec.y))

        # Sort the measures by distance and take the 2 lowest
        loc = sorted(loc, key=lambda x: x[0])

        r0, x0, y0 = loc[0] # nearest receiver
        r1 ,x1, y1 = loc[1] # second nearest receiver

        # First we check the edge cases
        dist = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        if dist > (r0 + r1):
            # The circles do not intersects, it means something is wrong
            raise ValueError("Out of range or something wrong")
        if isclose(dist, r0 + r1, rel_tol=1e-6, abs_tol=0.01):
            # The tracker is just in the middle of two receivers (tangent circles)
            # and we can calculate its position
            x = x0 + (x1 - x0)/2
            y = y0 + (y1 - y0)/2
            self.__x , self.__y = x, y
            return (self.__x , self.__y)
        
        # Now we know the two circles intesect in two points and
        # one of them is our target. Let's calculate this points
        (x3_1, y3_1), (x3_2, y3_2) = self.__calculate_candidate_points(r0, x0, y0, r1, x1, y1, dist)
        print(f"{self.id} is at: ({x3_1},{y3_1}) or ({x3_2},{y3_2})")

        # We need the 3rd nearest receiver to decide which is the correct point
        # so we'll take the receiver on the 3rd position of the sortered list
        rt, xt, yt = loc[2]
        
        # Measure the distance from this receiber to the 2 candidates
        test_p1 = self.__measure_distance(x3_1, y3_1, xt, yt)
        test_p2 = self.__measure_distance(x3_2, y3_2, xt, yt)
        
        # The closest one is or taget (it should be 0 but we have
        # to take into account the receiver's precission)
        if isclose(rt, test_p1, rel_tol=1e-6, abs_tol=0.01):
            self.__x , self.__y = x3_1, y3_1
        elif isclose(rt, test_p2, rel_tol=1e-6, abs_tol=0.01):
            self.__x , self.__y = x3_2, y3_2
        else:
            raise ValueError("Out of range or something wrong")
        return (self.__x , self.__y)

    def __calculate_candidate_points(self, r0, x0, y0, r1, x1, y1, dist):
        # This helper calculates the two points of intersection of 2 circles
        # https://paulbourke.net/geometry/circlesphere/
        # l1 = (r0^2 - r1^2 + dist ^2) / (2*dist)
        l1 = (r0 ** 2 - r1 ** 2 + dist ** 2) / (2 * dist)

        # l2 = sqrt(r0^2 - l1^2)
        l2 = sqrt(r0 ** 2 - l1 ** 2)

        # p2 = p0 + l1 * (p1 - p0) / dist
        x2 = x0 + l1 * (x1 - x0) / dist
        y2 = y0 + l1 * (y1 - y0) / dist

        # This are the two points candidates, the intersection of the 2 circles:
        # x3_1 = x2 + l2 * (y1 - y0) / dist  ||  y3_1 = y2 - l2 * (x1 - x0) / dist
        # x3_2 = x2 - l2 * (y1 - y0) / dist  ||  y3_2 = y2 + l2 * (x1 - x0) / dist 
        return (
            (x2 + l2 * (y1 - y0) / dist, y2 - l2 * (x1 - x0) / dist),
            (x2 - l2 * (y1 - y0) / dist, y2 + l2 * (x1 - x0) / dist)
        )

    def __measure_distance(self, x, y, rx, ry):
        # This helper measures the distance between a given point (x,y)
        # and the receiver (rx, ry) 
        dist_x = x - rx
        dist_y = y - ry
        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        return dist



