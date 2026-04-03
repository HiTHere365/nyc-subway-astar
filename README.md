NYC SUBWAY ROUTE PLANNER
========================

OVERVIEW
--------
An interactive Python script that implements A* search to find optimal subway
routes in a simplified NYC subway network. Demonstrates informed search by
finding the fastest path between stations using f(n) = g(n) + h(n).


REQUIREMENTS
------------
- Python 3.7 or higher
- networkx library
- heapq (built-in Python module)

    pip install networkx


RUNNING THE PROGRAM
-------------------
    python NYC_Subway_planner-2.py


USAGE
-----
1. The program displays available subway stations
2. Enter a starting station (case-sensitive)
3. Enter a destination station
4. The program displays the optimal route, total travel time, and search stats
5. Enter 'quit' to exit


TESTING EXAMPLES
----------------

Test Case 1: Simple Route
  Start: Bronx → Goal: Harlem
  Expected: Direct route, 20 minutes

Test Case 2: Multi-hop Route
  Start: Bronx → Goal: NJ
  Expected: Multi-station path, A* selecting optimal route among alternatives

Test Case 3: Route with Alternatives
  Start: City College → Goal: Penn Station
  Expected: A* evaluating direct vs. indirect routes

Test Case 4: Longer Journey
  Start: Bronx → Goal: Newark
  Expected: Longer path demonstrating multi-hop exploration

Test Case 5: Adjacent Stations
  Start: Penn Station → Goal: NJ
  Expected: Direct single hop, 5 minutes


NETWORK STRUCTURE
-----------------
Stations: Bronx, Harlem, City College, West 4th St, Union Square,
          Penn Station, Newark, NJ

Connections with travel times ranging 5-40 minutes.


ALGORITHM DETAILS
-----------------
Search Method: A* (A-star)
Heuristic:     Manhattan distance scaled to time estimate (admissible)
Properties:    Complete, Optimal, Informed

f(n) = g(n) + h(n)
- g(n): actual cost from start to node n
- h(n): Manhattan distance estimate to goal, scaled so it never overestimates
- f(n): estimated total path cost through n


CODE STRUCTURE
--------------
SubwayRoutePlanner class:
- _build_network()      Build weighted graph of stations and travel times
- _set_coordinates()    Set normalized positions for heuristic calculation
- heuristic()           Manhattan distance estimate to goal
- a_star_search()       Main A* implementation with priority queue
- _reconstruct_path()   Trace came_from dict back to start
- display_route()       Print path, total time, and search statistics


MODIFICATIONS
-------------
- Add stations: edit _build_network() with new edges
- Change heuristic: modify heuristic() method
- Add real coordinates: update _set_coordinates() with actual lat/lon
- Add other algorithms: follow the same structure as a_star_search()


REFERENCES
----------
Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson.
