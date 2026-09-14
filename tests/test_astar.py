"""Tests for the A* subway route planner."""

import itertools

import networkx as nx
import pytest

from nyc_subway_planner import SubwayRoutePlanner


@pytest.fixture(scope="module")
def planner():
    return SubwayRoutePlanner()


def _all_pairs():
    stations = SubwayRoutePlanner().get_available_stations()
    return list(itertools.product(stations, repeat=2))


@pytest.mark.parametrize("start,goal", _all_pairs())
def test_astar_matches_dijkstra(planner, start, goal):
    """A* must return the same cost as an exhaustive shortest-path search."""
    expected = nx.dijkstra_path_length(planner.graph, start, goal, weight="weight")
    path, cost, _stats = planner.a_star_search(start, goal)
    assert path is not None
    assert cost == expected
    # The reported path must actually be walkable and sum to the reported cost.
    assert path[0] == start and path[-1] == goal
    walked = sum(
        planner.graph[a][b]["weight"] for a, b in zip(path, path[1:])
    )
    assert walked == cost


@pytest.mark.parametrize("node,goal", _all_pairs())
def test_heuristic_is_admissible(planner, node, goal):
    """h(n) must never exceed the true shortest cost from n to goal."""
    true_cost = nx.dijkstra_path_length(planner.graph, node, goal, weight="weight")
    assert planner.heuristic(node, goal) <= true_cost


def test_same_station_query(planner):
    """Start == goal returns a single-node, zero-cost path."""
    for station in planner.get_available_stations():
        path, cost, stats = planner.a_star_search(station, station)
        assert path == [station]
        assert cost == 0
        assert stats["nodes_explored"] == 1
