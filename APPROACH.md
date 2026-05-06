# Design Approach

## The Problem

Given a weighted graph of NYC subway stations connected by edges with travel times, find the optimal route between two stations that minimizes total travel time. This is a shortest path problem on a finite weighted graph where:

- **Initial state**: starting station
- **Goal state**: destination station
- **Actions**: move along an edge to a neighboring station
- **Path cost**: accumulated travel time

## Why A* Over the Alternatives

Three search strategies apply to this problem:

| Strategy | How it works | Problem |
|---|---|---|
| Uniform Cost Search | Expands cheapest g(n) first | Explores in all directions, ignores goal location |
| Greedy Best-First | Expands smallest h(n) first | Ignores cost already incurred, gets misled by detours |
| A* | Expands smallest f(n) = g(n) + h(n) first | Balances both, optimal and complete |

UCS is optimal but blind: it expands nodes in every direction with no sense of where the goal is. Greedy search is fast but not optimal: it can be misled by a locally attractive route that costs more overall. A* combines both signals. The heuristic focuses the search toward the goal; the accumulated cost prevents it from chasing cheap-looking shortcuts that add up to a longer path.

For a routing problem where both correctness and efficiency matter, A* is the right choice.

## Admissibility of the Heuristic

The heuristic h(n) is a scaled Manhattan distance between station coordinates:

```
h(n) = manhattan_distance(n, goal) * 0.3
```

A heuristic is **admissible** if it never overestimates the true cost to reach the goal. The scaling factor (0.3) is calibrated so that the distance estimate is always less than or equal to actual travel time along any real path through the graph. Because A* with an admissible heuristic is guaranteed to return an optimal path, admissibility is a hard requirement here.

For a real deployment with actual geographic coordinates, the scaling factor would be derived from the ratio of physical distance to average travel time across the network.

## Optimality and Completeness

A* on a finite graph with an admissible heuristic is:
- **Complete**: guaranteed to find a path if one exists
- **Optimal**: guaranteed to return the minimum-cost path

The implementation uses a min-heap priority queue ordered by f(n) = g(n) + h(n), a `came_from` dictionary for path reconstruction, and a `g_cost` dictionary that updates when a shorter path to a node is found. A tie-breaking counter ensures stable ordering when f-costs are equal.

## Memory Tradeoff

A* keeps both explored nodes and the frontier in memory, which grows with the search space. For the small subway network modeled here this is not a concern, but on very large graphs (city-scale road networks, for example) memory becomes the binding constraint. In those cases, variants like IDA* (iterative deepening A*) trade memory for time by recomputing paths rather than storing them.

## Extension Points

- Replace normalized coordinates with real lat/lon for a geographically accurate heuristic
- Swap Manhattan distance for Euclidean or Haversine distance depending on network geometry
- Add time-of-day weighting to edges to model peak vs. off-peak travel times
- Extend to multi-modal routing (subway + bus + walking) by adding edge types
