"""
File: heuristics.py -- Fan Yang & Dana Nau, Feb 14, 2018

This file contains five heuristic functions:
- h_edist returns the Euclidean distance from (s) to the goal, ignoring walls;
- h_esdist modifies h_edist to include an estimate of how long it will take to stop;
- h_walldist computes the approximate distance to the goal without ignoring walls. 
- h_ff1 and h_ff2 return the fast-forward distances as described in the project description.
    (h_ff1 and ff1 corresponds to state-variable representation 1; h_ff2 and ff2 correspond
    to state-variable representation 2.)
 Each heuristic function takes three arguments: state, edge, walls.
   state is the current state. It should have the form ((x,y), (u,v))
   edge is the finish line. It should have the form ((x1,y1), (x2,y2))
   walls is a list of walls, each wall having the form ((x1,y1), (x2,y2))
"""

import sys
import math
import racetrack
from itertools import product


# cached_states momerizes the visited states so that we can avoid calculating
# the same state multiple times.
cached_states = {}


def h_ff1(state, fline, walls):
    """
    :param state: the starting state
    :param fline: the finish line
    :param walls: the walls that cannot be crossed
    :return: an approximate number of steps needed to reach the finish line
    """
    global cached_states
    if state not in cached_states:
        # If the state has not been cached yet, we calculate the number of needed
        # steps and cache it.
        solution = ff1(state, fline, walls)
        if solution == False:
            cached_states[state] = math.inf
        else:
            cached_states[state] = sum([len(e) for e in solution])
    return cached_states[state]


def ff1(state, fline, walls):
    """
    :param state: the starting state
    :param fline: the finish line
    :param walls: the walls that cannot be crossed
    :return: a list of moves that when applied to the starting state r-satisfy the goal
    """

    # We first change the state to state variable representation 1. Note that I don't use
    # exactly the same representation as given in the project writeup. In the code below
    # state-variable representation 1 is represented as a list of 4 sets which consrrespond
    # to the values of x, y, u, v, respectively.
    # The goal is also converted to a list of 4 sets.
    (x0, y0), (u0, v0) = state
    (x1, y1), (x2, y2) = fline
    x_fline = range(min(x1, x2), max(x1, x2) + 1)
    y_fline = range(min(y1, y2), max(y1, y2) + 1)
    goal = [set(x_fline), set(y_fline), {0}, {0}]
    state = [{x0}, {y0}, {u0}, {v0}]
    achieved = [state[i] & goal[i] for i in range(4)]
    explored, solution = [], []

    # At each iteration of the while loop below, we select all actions that are r-applicable
    # in the current state and generate the next state accordingly. We repeat this while-loop
    # until a subset of the curent state r-satisfies the goal.
    # curr, prev store the combinations of the the values of the four state variables
    curr, prev = {(x0, y0, u0, v0)}, set()
    while not all(achieved):
        explored.append(state)
        actions = []
        # use curr - prev to avoid expanding the same value combination multiple times
        for x, y, u, v in curr - prev:
            pre = x, y, u, v
            for du, dv in ((du, dv) for du in [-1, 0, 1] for dv in [-1, 0, 1]):
                eff = _x, _y, _u, _v = x + u + du, y + v + dv, u + du, v + dv
                if eff in curr or racetrack.crash(((x, y), (_x, _y)), walls): continue
                state = [state[i] | {eff[i]} for i in range(4)]
                actions.append(((du, dv), pre, eff))
        # If the current state and the next state are the same, then there exists no solution,
        # so we return false
        if not actions: return False
        solution.append(actions)
        prev = curr
        curr = set(product(*state))
        achieved = [state[i] & goal[i] for i in range(4)]

    # On the finish line select a point that has been reached.
    # To ensure consistency, always select the point closest from the starting point.
    x_goal = min(list(achieved[0]), key=lambda x: abs(x - x0))
    y_goal = min(list(achieved[1]), key=lambda y: abs(y - y0))
    goal = [{x_goal}, {y_goal}, {0}, {0}]

    # The while-loop below backtracks from the goal to the starting state. At each iteration
    # it find a minimal set of actions that when applied to the current state will r-statisfy
    # the goal. It then updates the goal by removing the effects of the actions then adding
    # the preconditions of them. The while-loop repeats until it backtracks to the starting state.
    while explored:
        state = explored.pop()
        actions = solution.pop(len(explored))
        # target corresponds to the goal clauses that cannot be found in the current state.
        target = [goal[i] - state[i] for i in range(4)]
        pre, eff, gain = ([set() for _ in range(4)] for _ in range(3))
        # moves will store the minimal set of actions that r-satisfy the goal
        moves = []
        for i in range(len(actions)):
            move1, pre1, eff1 = actions[i]
            gain1 = [{eff1[i]} & target[i] for i in range(4)]
            # since we are interested in finding a minimal set of actions that r-ahieve the goal,
            # we can throw away all actions that either do not make progress towards the goal or make
            # no more progress than another action. The variable redundant denotes whether the action
            # can be thrown.
            redundant = gain1 <= gain
            for j in range(i + 1, len(actions)):
                if redundant: break
                move2, pre2, eff2 = actions[j]
                gain2 = [{eff2[i]} & target[i] for i in range(4)]
                redundant |= (gain1 <= gain2)
            if not redundant:
                pre = [pre[i] | {pre1[i]} for i in range(4)]
                eff = [eff[i] | {eff1[i]} for i in range(4)]
                gain = [gain[i] | gain1[i] for i in range(4)]
                moves.append(move1)
                if gain == target: break
        # update the goal and insert the filtered actions back to the solution.
        goal = [(goal[i] - eff[i]) | pre[i] for i in range(4)]
        solution.insert(len(explored), moves)
    return solution


def h_ff2(state, fline, walls):
    """
    :param state: the starting state
    :param fline: the finish line
    :param walls: the walls that cannot be crossed
    :return: an approximate number of steps needed to reach the finish line
    """
    global cached_states
    if state not in cached_states:
        # If the state has not been cached yet, we calculate the number of needed
        # steps and cache it.
        solution = ff2(state, fline, walls)
        if solution == False:
            cached_states[state] = math.inf
        else:
            cached_states[state] = sum([len(e) for e in solution])
    return cached_states[state]


def ff2(state, fline, walls):
    """
    :param state: the starting state
    :param fline: the finish line
    :param walls: the walls that cannot be crossed
    :return: a list of moves that when applied to the starting state r-satisfy the goal
    """

    # We first change the state to state variable representation 2. Note that I don't use
    # exactly the same representation as given in the project writeup. In the code below
    # state-variable representation 2 is represented as a list of 2 sets which consrrespond
    # to the values of location p and velocity z, respectively.
    # The goal is also converted to a list of 2 sets.
    (x0, y0), (u0, v0) = state
    (x1, y1), (x2, y2) = fline
    x_fline = range(min(x1, x2), max(x1, x2) + 1)
    y_fline = range(min(y1, y2), max(y1, y2) + 1)
    goal = [set(product(x_fline, y_fline)), {(0, 0)}]
    state = [{(x0, y0)}, {(u0, v0)}]
    achieved = [state[0] & goal[0], state[1] & goal[1]]
    explored, solution = [], []

    # At each iteration of the while loop below, we select all actions that are r-applicable
    # in the current state and generate the next state accordingly. We repeat this while-loop
    # until a subset of the curent state r-satisfies the goal.
    # curr, prev store the combinations of the the values of the two state variables
    curr, prev = {((x0, y0), (u0, v0))}, set()
    while not all(achieved):
        explored.append(state)
        actions = []
        # use curr - prev to avoid expanding the same value combination multiple times
        for p, z in curr - prev:
            for m in [(du, dv) for du in [-1, 0, 1] for dv in [-1, 0, 1]]:
                _p, _z = (p[0] + z[0] + m[0], p[1] + z[1] + m[1]), (z[0] + m[0], z[1] + m[1])
                if (_p, _z) in curr or racetrack.crash((p, _p), walls): continue
                state = [state[0] | {_p}, state[1] | {_z}]
                actions.append((m, (p, z), (_p, _z)))
        # If the current state and the next state are the same, then there exists no solution,
        # so we return false
        if not actions: return False
        solution.append(actions)
        prev = curr
        curr = set(product(*state))
        achieved = [state[i] & goal[i] for i in range(2)]

    # on the finish line select a point that has been reached
    # to ensure consistency, always select the point closest from the starting point
    p_goal = min(list(achieved[0]), key=lambda p: (p[0] - x0) ** 2 + (p[1] - y0) ** 2)
    goal = [{p_goal}, {(0, 0)}]

    # The while-loop below backtracks from the goal to the starting state. At each iteration
    # it find a minimal set of actions that when applied to the current state will r-statisfy
    # the goal. It then updates the goal by removing the effects of the actions then adding
    # the preconditions of them. The while-loop repeats until it backtracks to the starting state.
    while explored:
        state = explored.pop()
        actions = solution.pop(len(explored))
        # target corresponds to the goal clauses that cannot be found in the current state.
        target = [goal[0] - state[0], goal[1] - state[1]]
        pre, eff, gain = ([set(), set()] for _ in range(3))
        moves = []  # store the minimal set of actions that r-satisfy the goal
        for i in range(len(actions)):
            move1, pre1, eff1 = actions[i]
            gain1 = [{eff1[0]} & target[0], {eff1[1]} & target[1]]
            # since we are interested in finding a minimal set of actions that r-ahieve the goal,
            # we can throw away all actions that either do not make progress towards the goal or make
            # no more progress than another action. The variable redundant denotes whether the action
            # can be thrown.
            redundant = gain1 <= gain
            for j in range(i + 1, len(actions)):
                if redundant: break
                move2, pre2, eff2 = actions[j]
                gain2 = [{eff2[0]} & target[0], {eff2[1]} & target[1]]
                redundant |= (gain1 <= gain2)
            if not redundant:
                pre = [pre[0] | {pre1[0]}, pre[1] | {pre1[1]}]
                eff = [eff[0] | {eff1[0]}, eff[1] | {eff1[1]}]
                gain = [gain[0] | gain1[0], gain[1] | gain1[1]]
                moves.append(move1)
                if gain == target: break
        # update the goal and insert the filtered actions back to the solution.
        goal = [(goal[i] - eff[i]) | pre[i] for i in range(2)]
        solution.insert(len(explored), moves)
    return solution


def h_edist(state, edge, walls):
    """Euclidean distance from state to edge, ignoring walls."""
    (x, y) = state[0]
    ((x1, y1), (x2, y2)) = edge

    # find the smallest and largest coordinates
    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)

    return min([math.sqrt((xx - x) ** 2 + (yy - y) ** 2)
                for xx in range(xmin, xmax + 1) for yy in range(ymin, ymax + 1)])


def h_esdist(state, fline, walls):
    """
    h_edist modified to include an estimate of how long it will take to stop.
    """
    ((x, y), (u, v)) = state
    m = math.sqrt(u ** 2 + v ** 2)
    stop_dist = m * (m - 1) / 2.0
    return max(h_edist(state, fline, walls) + stop_dist / 10.0, stop_dist)


# Global variables for h_walldist

# in Python 3 we can just use math.inf, but that doesn't work in Python 2
infinity = float('inf')

g_fline, g_walls, grid = False, False, []


def h_walldist(state, fline, walls):
    """
    The first time this function is called, for each gridpoint that's not inside a wall
    it will cache a rough estimate of the length of the shortest path to the finish line.
    The computation is done by a breadth-first search going backwards from the finish 
    line, one gridpoint at a time.
    
    On all subsequent calls, this function will retrieve the cached value and add an
    estimate of how long it will take to stop. 
    """
    global g_fline, g_walls
    if fline != g_fline or walls != g_walls or grid == []:
        edist_grid(fline, walls)
    ((x, y), (u, v)) = state
    hval = float(grid[x][y])

    # add a small penalty to favor short stopping distances
    au = abs(u)
    av = abs(v)
    sdu = au * (au - 1) / 2.0
    sdv = av * (av - 1) / 2.0
    sd = max(sdu, sdv)
    penalty = sd / 10.0

    # compute location after fastest stop, and add a penalty if it goes through a wall
    if u < 0: sdu = -sdu
    if v < 0: sdv = -sdv
    sx = x + sdu
    sy = y + sdv
    if racetrack.crash([(x, y), (sx, sy)], walls):
        penalty += math.sqrt(au ** 2 + av ** 2)
    hval = max(hval + penalty, sd)
    return hval


def edist_grid(fline, walls):
    global grid, g_fline, g_walls, xmax, ymax
    xmax = max([max(x, x1) for ((x, y), (x1, y1)) in walls])
    ymax = max([max(y, y1) for ((x, y), (x1, y1)) in walls])
    grid = [[edistw_to_line((x, y), fline, walls) for y in range(ymax + 1)] for x in range(xmax + 1)]
    flag = True
    print('computing edist grid', end=' ')
    sys.stdout.flush()
    while flag:
        print('.', end='')
        sys.stdout.flush()
        flag = False
        for x in range(xmax + 1):
            for y in range(ymax + 1):
                for y1 in range(max(0, y - 1), min(ymax + 1, y + 2)):
                    for x1 in range(max(0, x - 1), min(xmax + 1, x + 2)):
                        if grid[x1][y1] != infinity and not racetrack.crash(((x, y), (x1, y1)), walls):
                            if x == x1 or y == y1:
                                d = grid[x1][y1] + 1
                            else:
                                d = grid[x1][y1] + 1.4142135623730951
                            if d < grid[x][y]:
                                grid[x][y] = d
                                flag = True
    print('done')
    g_fline = fline
    g_walls = walls
    return grid


def edistw_to_line(point, edge, walls):
    """
    straight-line distance from (x,y) to the line ((x1,y1),(x2,y2)).
    Return infinity if there's no way to do it without intersecting a wall
    """
    #   if min(x1,x2) <= x <= max(x1,x2) and  min(y1,y2) <= y <= max(y1,y2):
    #       return 0
    (x, y) = point
    ((x1, y1), (x2, y2)) = edge
    if x1 == x2:
        ds = [math.sqrt((x1 - x) ** 2 + (y3 - y) ** 2) \
              for y3 in range(min(y1, y2), max(y1, y2) + 1) \
              if not racetrack.crash(((x, y), (x1, y3)), walls)]
    else:
        ds = [math.sqrt((x3 - x) ** 2 + (y1 - y) ** 2) \
              for x3 in range(min(x1, x2), max(x1, x2) + 1) \
              if not racetrack.crash(((x, y), (x3, y1)), walls)]
    ds.append(infinity)
    return min(ds)


def distance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def tear_down():
    global g_fline, g_walls
    g_fline, g_walls = False, False
    grid.clear()
    cached_states.clear()
