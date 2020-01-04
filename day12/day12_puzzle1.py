import re


class PlanetSim:
    def __init__(self):
        self.coordinates = []
        self.velocities = []

    def add_planet(self, coordinate):
        self.coordinates.append(coordinate)
        self.velocities.append(Velocity(0, 0, 0))
        
    def calculate_total_energy(self):
        total_energy = 0
        for coordinate, velocity in zip(self.coordinates, self.velocities):
            total_energy += coordinate.energy() * velocity.energy()
        return total_energy
        
    def simulate(self, steps):
        for step in range(steps):
            self.step(step)
    
    def step(self, step):
        self.apply_gravity()
        self.apply_velocity()
        #print(step+1)
        #for coordinate, velocity in zip(self.coordinates, self.velocities):
            #print(coordinate.x, coordinate.y, coordinate.z, velocity.x, velocity.y, velocity.z)
    
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

        
def solve_day12puzzle1():
    with open("day12_data.txt", 'r') as f:
        planet_sim = PlanetSim()
        
        for line in f:
            x, y, z = tuple(map(int, re.sub('[ <>\nxyz=]', '', line).split(',')))
            planet_sim.add_planet(Coordinate(x, y, z))
            
        planet_sim.simulate(1000)
        
        return planet_sim.calculate_total_energy()
        
        
def tests_day12puzzle1():
    planet_sim = PlanetSim()
    planet_sim.add_planet(Coordinate(-1, 0, 2))
    planet_sim.add_planet(Coordinate(2, -10, -7))
    planet_sim.add_planet(Coordinate(4, -8, 8))
    planet_sim.add_planet(Coordinate(3, 5, -1))
    planet_sim.simulate(10)
    if planet_sim.calculate_total_energy() != 179:
        return False
    
    planet_sim = PlanetSim()
    planet_sim.add_planet(Coordinate(-8, -10, 0))
    planet_sim.add_planet(Coordinate(5, 5, 10))
    planet_sim.add_planet(Coordinate(2, -7, 3))
    planet_sim.add_planet(Coordinate(9, -8, -3))
    planet_sim.simulate(100)
    if planet_sim.calculate_total_energy() != 1940:
        return False

    planet_sim = PlanetSim()
    planet_sim.add_planet(Coordinate(-8, -10, 0))
    planet_sim.add_planet(Coordinate(5, 5, 10))
    planet_sim.add_planet(Coordinate(2, -7, 3))
    planet_sim.add_planet(Coordinate(9, -8, -3))
    planet_sim.simulate(4686774924)
    print(planet_sim.calculate_total_energy())
    return True


def main():
    if tests_day12puzzle1():
        print("Day 12 Puzzle 1 answer: ", solve_day12puzzle1())


if __name__ == "__main__":
    main()
