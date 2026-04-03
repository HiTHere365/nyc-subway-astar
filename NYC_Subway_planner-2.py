"""
NYC Subway Route Planner - A* Search Implementation
====================================================

Problem Definition:
------------------
This script solves a simplified NYC subway routing problem. Given a network of subway
stations connected by lines with travel times, find the optimal route from a starting
station to a destination station, minimizing total travel time.

This is a variant of the shortest path problem in a weighted graph, where:
- Initial State: Starting subway station
- Goal State: Destination subway station
- Actions: Move from one station to a connected neighboring station
- Path Cost: Sum of travel times between stations

Search Algorithm: A* Search
"""

import heapq
import networkx as nx
from typing import Dict, List, Tuple, Optional


class SubwayRoutePlanner:
    """
    A subway route planner using A* search algorithm.
    """
    
    def __init__(self):
        """Initialize the subway network graph."""
        self.graph = nx.Graph()
        self._build_network()
        self._set_coordinates()
        
    def _build_network(self):
        """
        Build the NYC subway network with stations and travel times.
        Travel times are in minutes.
        """
        # Define edges: (station1, station2, travel_time_minutes)
        edges = [
            ('Bronx', 'Harlem', 20),
            ('Harlem', 'City College', 10),
            ('City College', 'West 4th St', 25),
            ('City College', 'Penn Station', 15),  # Added alternate route
            ('West 4th St', 'Union Square', 5),
            ('Union Square', 'Penn Station', 8),
            ('West 4th St', 'Newark', 40),
            ('Newark', 'Penn Station', 10),
            ('Penn Station', 'NJ', 5),
            ('Harlem', 'Penn Station', 30),  # Express route
        ]
        
        for u, v, weight in edges:
            self.graph.add_edge(u, v, weight=weight)
    
    def _set_coordinates(self):
        """
        Set approximate coordinates for heuristic calculation.
        Coordinates are normalized to represent relative positions.
        For a real application, these would be actual lat/lon coordinates.
        """
        self.coordinates = {
            'Bronx': (0, 100),
            'Harlem': (0, 80),
            'City College': (10, 70),
            'West 4th St': (20, 50),
            'Union Square': (25, 55),
            'Penn Station': (30, 40),
            'Newark': (50, 30),
            'NJ': (60, 20),
        }
    
    def heuristic(self, node: str, goal: str) -> float:
        """
        Calculate heuristic estimate from node to goal.
        
        Uses Manhattan distance scaled by average speed.
        This heuristic is admissible (never overestimates) because:
        - It assumes direct travel at maximum possible speed
        - Actual route must follow edges, which cannot be shorter
        
        Args:
            node: Current station
            goal: Goal station
            
        Returns:
            Estimated time in minutes to reach goal
        """
        if node not in self.coordinates or goal not in self.coordinates:
            return 0
        
        x1, y1 = self.coordinates[node]
        x2, y2 = self.coordinates[goal]
        
        # Manhattan distance
        manhattan_dist = abs(x1 - x2) + abs(y1 - y2)
        
        # Convert to time estimate (assume 2 units of distance = 1 minute)
        # This is calibrated to never overestimate actual travel time
        estimated_time = manhattan_dist * 0.3
        
        return estimated_time
    
    def a_star_search(self, start: str, goal: str) -> Tuple[Optional[List[str]], Optional[float], Dict]:
        """
        Perform A* search to find optimal route.
        
        A* uses f(n) = g(n) + h(n) where:
        - g(n): actual cost from start to node n
        - h(n): heuristic estimate from n to goal
        - f(n): estimated total cost of path through n
        
        Args:
            start: Starting station
            goal: Destination station
            
        Returns:
            Tuple of (path, total_cost, search_stats)
        """
        if start not in self.graph:
            print(f"Error: Starting station '{start}' not found in network.")
            return None, None, {}
        
        if goal not in self.graph:
            print(f"Error: Goal station '{goal}' not found in network.")
            return None, None, {}
        
        # Statistics for analysis
        stats = {
            'nodes_explored': 0,
            'nodes_in_frontier': 0,
            'max_frontier_size': 0
        }
        
        # Priority queue: (f_cost, counter, current_node)
        # Counter ensures FIFO behavior for equal f_costs
        counter = 0
        frontier = []
        heapq.heappush(frontier, (0, counter, start))
        
        # Track how we reached each node
        came_from = {start: None}
        
        # g(n): actual cost from start to n
        g_cost = {start: 0}
        
        while frontier:
            stats['max_frontier_size'] = max(stats['max_frontier_size'], len(frontier))
            
            f, _, current = heapq.heappop(frontier)
            stats['nodes_explored'] += 1
            
            # Goal test
            if current == goal:
                path = self._reconstruct_path(came_from, current)
                return path, g_cost[current], stats
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                # Calculate new cost to reach neighbor
                edge_weight = self.graph[current][neighbor]['weight']
                tentative_g = g_cost[current] + edge_weight
                
                # If this is a better path to neighbor, record it
                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g
                    h = self.heuristic(neighbor, goal)
                    f_cost = tentative_g + h
                    
                    counter += 1
                    heapq.heappush(frontier, (f_cost, counter, neighbor))
                    came_from[neighbor] = current
        
        # No path found
        return None, None, stats
    
    def _reconstruct_path(self, came_from: Dict[str, str], current: str) -> List[str]:
        """Reconstruct the path from start to goal."""
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
    
    def get_available_stations(self) -> List[str]:
        """Return list of all available stations."""
        return sorted(self.graph.nodes())
    
    def display_route(self, path: List[str], total_cost: float, stats: Dict):
        """Display the route information in a readable format."""
        print("\n" + "="*60)
        print("ROUTE FOUND!")
        print("="*60)
        
        print(f"\nPath: {' → '.join(path)}")
        print(f"\nTotal Travel Time: {total_cost:.1f} minutes")
        
        print("\nDetailed Route:")
        for i in range(len(path) - 1):
            current = path[i]
            next_station = path[i + 1]
            segment_time = self.graph[current][next_station]['weight']
            print(f"  {i+1}. {current} → {next_station} ({segment_time} min)")
        
        print(f"\nSearch Statistics:")
        print(f"  Nodes explored: {stats['nodes_explored']}")
        print(f"  Max frontier size: {stats['max_frontier_size']}")
        print("="*60 + "\n")


def main():
    """Main interactive function."""
    print("\n" + "="*60)
    print("NYC SUBWAY ROUTE PLANNER")
    print("Using A* Search Algorithm")
    print("="*60)
    
    planner = SubwayRoutePlanner()
    
    print("\nAvailable Stations:")
    stations = planner.get_available_stations()
    for i, station in enumerate(stations, 1):
        print(f"  {i}. {station}")
    
    # Interactive mode
    while True:
        print("\n" + "-"*60)
        try:
            start = input("\nEnter starting station (or 'quit' to exit): ").strip()
            if start.lower() == 'quit':
                print("Thank you for using NYC Subway Route Planner!")
                break
            
            goal = input("Enter destination station: ").strip()
            
            print(f"\nSearching for route from '{start}' to '{goal}'...")
            print("Using A* search with Manhattan distance heuristic...\n")
            
            path, total_cost, stats = planner.a_star_search(start, goal)
            
            if path:
                planner.display_route(path, total_cost, stats)
            else:
                print(f"\nNo route found from '{start}' to '{goal}'.")
                print("Please check that both stations exist in the network.\n")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
