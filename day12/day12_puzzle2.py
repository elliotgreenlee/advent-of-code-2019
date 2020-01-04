import re


class PlanetSim:
    def __init__(self):
        self.coordinatesx = []
        self.coordinatesy = []
        self.coordinatesz = []
        self.velocitiesx = []
        self.velocitiesy = []
        self.velocitiesz = []
    
    def add_planet(self, coordinate):
        self.coordinatesx.append(coordinate.x)
        self.coordinatesy.append(coordinate.y)
        self.coordinatesz.append(coordinate.z)
        self.velocitiesx.append(0)
        self.velocitiesy.append(0)
        self.velocitiesz.append(0)
        
    # TODO: redo calculation
    def calculate_total_energy(self):
        total_energy = 0
        for coordinate, velocity in zip(self.coordinates, self.velocities):
            total_energy += coordinate.energy() * velocity.energy()
        return total_energy
    
    def find_repeats_x(self):
        past_statsx = set()
        past_statsx.add(tuple(self.coordinatesx) + tuple(self.velocitiesx))

        step = 1
        repeat = False
        while not repeat:
            # apply gravity to velocities
            for i, x1 in enumerate(self.coordinatesx):
                for x2 in self.coordinatesx:
                    if x1 < x2:
                        self.velocitiesx[i] += 1
                    elif x1 > x2:
                        self.velocitiesx[i] -= 1
            # apply velocity to coordinates
            for i, velocity in enumerate(self.velocitiesx):
                self.coordinatesx[i] += velocity
            
            # check if already been here
            if (tuple(self.coordinatesx) + tuple(self.velocitiesx)) in past_statsx:
                return step
                repeat = True
                
            past_statsx.add(tuple(self.coordinatesx) + tuple(self.velocitiesx))
            
            step += 1

    def find_repeats_y(self):
        past_statsy = set()
        past_statsy.add(tuple(self.coordinatesy) + tuple(self.velocitiesy))
        
        step = 1
        repeat = False
        while not repeat:
            # apply gravity to velocities
            for i, y1 in enumerate(self.coordinatesy):
                for y2 in self.coordinatesy:
                    if y1 < y2:
                        self.velocitiesy[i] += 1
                    elif y1 > y2:
                        self.velocitiesy[i] -= 1
            # apply velocity to coordinates
            for i, velocity in enumerate(self.velocitiesy):
                self.coordinatesy[i] += velocity
        
            # check if already been here
            if (tuple(self.coordinatesy) + tuple(self.velocitiesy)) in past_statsy:
                return step
                repeat = True
        
            past_statsy.add(tuple(self.coordinatesy) + tuple(self.velocitiesy))
        
            step += 1

    def find_repeats_z(self):
        past_statsz = {}
        past_statsz[tuple(self.coordinatesz) + tuple(self.velocitiesz)] = 0

        step = 1
        repeat = False
        while not repeat:
            # apply gravity to velocities
            for i, z1 in enumerate(self.coordinatesz):
                for z2 in self.coordinatesz:
                    if z1 < z2:
                        self.velocitiesz[i] += 1
                    elif z1 > z2:
                        self.velocitiesz[i] -= 1
            # apply velocity to coordinates
            for i, velocity in enumerate(self.velocitiesz):
                self.coordinatesz[i] += velocity

            # check if already been here
            if (tuple(self.coordinatesz) + tuple(self.velocitiesz)) in past_statsz:
                return step
                repeat = True
        
            past_statsz[tuple(self.coordinatesz) + tuple(self.velocitiesz)] = step
        
            step += 1
    
    def simulate(self, steps):
        for step in range(steps):
            self.step(step)
    
    def step(self, step):
        self.apply_gravity()
        self.apply_velocity()
        # print(step+1)
        # for coordinate, velocity in zip(self.coordinates, self.velocities):
        # print(coordinate.x, coordinate.y, coordinate.z, velocity.x, velocity.y, velocity.z)
    
    def apply_gravity(self):
        for i, coordinate1 in enumerate(self.coordinates):
            for coordinate2 in self.coordinates:
                if coordinate1.x < coordinate2.x:
                    self.velocities[i].x += 1
                elif coordinate1.x > coordinate2.x:
                    self.velocities[i].x -= 1
                
                if coordinate1.y < coordinate2.y:
                    self.velocities[i].y += 1
                elif coordinate1.y > coordinate2.y:
                    self.velocities[i].y -= 1
                
                if coordinate1.z < coordinate2.z:
                    self.velocities[i].z += 1
                elif coordinate1.z > coordinate2.z:
                    self.velocities[i].z -= 1
    
    def apply_velocity(self):
        for i, velocity in enumerate(self.velocities):
            self.coordinates[i] += velocity


class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, velocity):
        return Coordinate(self.x + velocity.x, self.y + velocity.y, self.z + velocity.z)
    
    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


class Velocity:
    def __init__(self, velx, vely, velz):
        self.x = velx
        self.y = vely
        self.z = velz
    
    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def solve_day12puzzle2():
    with open("day12_data.txt", 'r') as f:
        planet_sim = PlanetSim()
        
        for line in f:
            x, y, z = tuple(map(int, re.sub('[ <>\nxyz=]', '', line).split(',')))
            planet_sim.add_planet(Coordinate(x, y, z))
        
        stepsx = planet_sim.find_repeats_x()
        stepsy = planet_sim.find_repeats_y()
        stepsz = planet_sim.find_repeats_z()
        return lcm(stepsx, lcm(stepsy, stepsz))


def tests_day12puzzle2():
    planet_sim = PlanetSim()
    planet_sim.add_planet(Coordinate(-1, 0, 2))
    planet_sim.add_planet(Coordinate(2, -10, -7))
    planet_sim.add_planet(Coordinate(4, -8, 8))
    planet_sim.add_planet(Coordinate(3, 5, -1))
    stepsx = planet_sim.find_repeats_x()
    stepsy = planet_sim.find_repeats_y()
    stepsz = planet_sim.find_repeats_z()
    if lcm(stepsx, lcm(stepsy, stepsz)) != 2772:
        return False
    
    planet_sim = PlanetSim()
    planet_sim.add_planet(Coordinate(-8, -10, 0))
    planet_sim.add_planet(Coordinate(5, 5, 10))
    planet_sim.add_planet(Coordinate(2, -7, 3))
    planet_sim.add_planet(Coordinate(9, -8, -3))
    stepsx = planet_sim.find_repeats_x()
    stepsy = planet_sim.find_repeats_y()
    stepsz = planet_sim.find_repeats_z()
    if lcm(stepsx, lcm(stepsy, stepsz)) != 4686774924:
        return False
    
    return True


def main():
    if tests_day12puzzle2():
        print("Day 12 Puzzle 2 answer: ", solve_day12puzzle2())


if __name__ == "__main__":
    main()
