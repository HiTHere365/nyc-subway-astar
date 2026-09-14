# NYC Subway Route Planner: A* Search

An interactive Python implementation of A* search applied to subway routing in a simplified NYC network. Finds the fastest path between stations using `f(n) = g(n) + h(n)`.

## Overview

Given a weighted graph of stations connected by lines with travel times, A* searches for the lowest-cost route by balancing actual cost incurred (`g(n)`) against a heuristic estimate of remaining cost (`h(n)`). The heuristic is a scaled Manhattan distance between hand-assigned station coordinates (`manhattan_distance * 0.1`).

The heuristic is admissible on this network by construction: the scale factor 0.1 is the largest value such that `h(n)` never exceeds the true shortest travel time for any of the 64 ordered station pairs. The binding pair is Penn Station to NJ, a 5 minute edge spanning 50 coordinate units. An earlier version used 0.3, which overestimated on the 10 pairs involving NJ; the test suite now checks every pair so a coordinate or scale change that breaks admissibility fails CI.

## Network

```
Stations: Bronx, Harlem, City College, West 4th St,
          Union Square, Penn Station, Newark, NJ
```

Travel times range from 5 to 40 minutes. The network includes an express edge (Harlem to Penn Station) and multi-hop alternatives for A* to evaluate.

## Requirements

```bash
pip install -r requirements.txt
```

Requires Python 3.7+.

## Running

```bash
python nyc_subway_planner.py
```

The program prompts for a starting station and a destination, prints the route, then prompts again. Enter `quit` (or send end-of-file) to exit.

## Sample Output

Interactive session, entering `Bronx` and then `NJ`:

```
============================================================
NYC SUBWAY ROUTE PLANNER
Using A* Search Algorithm
============================================================

Available Stations:
  1. Bronx
  2. City College
  3. Harlem
  4. NJ
  5. Newark
  6. Penn Station
  7. Union Square
  8. West 4th St

------------------------------------------------------------

Enter starting station (or 'quit' to exit): Bronx
Enter destination station: NJ

Searching for route from 'Bronx' to 'NJ'...
Using A* search with Manhattan distance heuristic...


============================================================
ROUTE FOUND!
============================================================

Path: Bronx → Harlem → City College → Penn Station → NJ

Total Travel Time: 50.0 minutes

Detailed Route:
  1. Bronx → Harlem (20 min)
  2. Harlem → City College (10 min)
  3. City College → Penn Station (15 min)
  4. Penn Station → NJ (5 min)

Search Statistics:
  Nodes explored: 5
  Max frontier size: 5
============================================================
```

## Algorithm Details

| Property | Value |
|---|---|
| Search method | A* with a min-heap frontier; nodes are re-pushed when a cheaper `g(n)` is found |
| Heuristic | Manhattan distance between station coordinates, scaled by 0.1 (largest admissible scale on this network) |
| Complete | Yes (finite graph) |
| Optimal | Matches Dijkstra on every pair in this network (tested), but the heuristic does not guarantee it |
| Time complexity | O(b^d) where b = branching factor, d = depth |

## Tests

```bash
pip install -r requirements.txt pytest
pytest -q
```

The suite checks three things for every ordered station pair: A* returns the same cost as `networkx` Dijkstra, the heuristic never exceeds the true cost, and a same-station query returns a zero-cost single-node path.

## Extension Points

- Replace normalized coordinates with real lat/lon for geographic accuracy
- Add time-of-day edge weights for peak vs. off-peak modeling
- Extend to multi-modal routing (subway + bus + walking)

## License

GNU Affero General Public License v3.0 (AGPL v3)

For commercial licensing: volts-beret0t@icloud.com
