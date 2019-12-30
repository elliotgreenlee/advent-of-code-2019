class Planet:
    def __init__(self, name):
        self.name = name
        self.orbits = None  # thing this node orbits


class Graph:
    def __init__(self):
        self.planets = {}
    
    def add_orbit_relationship(self, left_name, right_name):
        if left_name not in self.planets:
            left_planet = Planet(left_name)
            self.planets[left_name] = left_planet
        
        if right_name not in self.planets:
            right_planet = Planet(right_name)
            self.planets[right_name] = right_planet
        
        self.planets[right_name].orbits = self.planets[left_name]


def solve_day6puzzle1():
    with open("day6_data.txt", 'r') as f:
        
        graph = Graph()
        
        for line in f:
            names = line.strip().split(')')
            left_name = names[0]
            right_name = names[1]
            
            graph.add_orbit_relationship(left_name, right_name)
        
        planet = graph.planets['YOU']
        you_common = []
        while planet.orbits is not None:
            planet = planet.orbits
            you_common.append(planet.name)
        
        planet = graph.planets['SAN']
        san_common = []
        while planet.orbits is not None:
            planet = planet.orbits
            san_common.append(planet.name)

        difference = list(set(you_common).difference(set(san_common))) + list(set(san_common).difference(set(you_common)))
        return len(difference)


def tests_day6puzzle1():
    return True


def main():
    if tests_day6puzzle1():
        print("Day 6 Puzzle 1 answer: ", solve_day6puzzle1())


if __name__ == "__main__":
    main()
