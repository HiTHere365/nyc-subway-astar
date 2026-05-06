# NYC Subway Route Planner: A* Search

An interactive Python implementation of A* search applied to optimal subway routing in a simplified NYC network. Finds the fastest path between stations using `f(n) = g(n) + h(n)`.

## Overview

Given a weighted graph of stations connected by lines with travel times, A* finds the optimal route by balancing actual cost incurred (`g(n)`) against a heuristic estimate of remaining cost (`h(n)`). The heuristic is a scaled Manhattan distance between station coordinates, calibrated to be admissible (never overestimates), which guarantees the returned path is optimal.

## Network

```
Stations: Bronx, Harlem, City College, West 4th St,
          Union Square, Penn Station, Newark, NJ
```

Travel times range from 5 to 40 minutes. The network includes express routes and multi-hop alternatives for A* to evaluate.

## Requirements

```bash
pip install -r requirements.txt
```

Requires Python 3.7+.

## Running

```bash
python nyc_subway_planner.py
```

## Sample Output

```
NYC SUBWAY ROUTE PLANNER
Using A* Search Algorithm

Available Stations:
  1. Bronx
  2. City College
  3. Harlem
  4. NJ
  5. Newark
  6. Penn Station
  7. Union Square
  8. West 4th St

Enter starting station: Bronx
Enter destination station: NJ

ROUTE FOUND!
Path: Bronx -> Harlem -> City College -> Penn Station -> NJ
Total Travel Time: 50.0 minutes

Detailed Route:
  1. Bronx -> Harlem (20 min)
  2. Harlem -> City College (10 min)
  3. City College -> Penn Station (15 min)
  4. Penn Station -> NJ (5 min)

Search Statistics:
  Nodes explored: 5
  Max frontier size: 3
```

## Algorithm Details

| Property | Value |
|---|---|
| Search method | A* |
| Heuristic | Scaled Manhattan distance (admissible) |
| Complete | Yes |
| Optimal | Yes |
| Time complexity | O(b^d) where b = branching factor, d = depth |

## Extension Points

- Replace normalized coordinates with real lat/lon for geographic accuracy
- Add time-of-day edge weights for peak vs. off-peak modeling
- Extend to multi-modal routing (subway + bus + walking)

## License

GNU Affero General Public License v3.0 (AGPL v3)

For commercial licensing: volts-beret0t@icloud.com
