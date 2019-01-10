"""

File: proj2a.py -- Fan Yang, May 5, 2018

This file contains an implementation of modified LAO*

LAO* is a best first search algorithm for solving SSP problems with a cyclic search
space. Updates of the states in a cyclic search space cannot be based on a bottom-up
stage-by-stage procedure. LAO∗ handle this by performing a Value-Iteration-like series
of repeated updates that are limited to the states on which the expansion of the
selected leaf state s may have an effect.

The "main" function takes three arguments: state, edge, walls.
   state is the current state. It should have the form ((x,y), (u,v))
   edge is the finish line. It should have the form ((x1,y1), (x2,y2))
   walls is a list of walls, each wall having the form ((x1,y1), (x2,y2))

"""
import os
import math
import time
import shelve
import random
from itertools import product
from heuristics import edist_grid
from racetrack import crash  # program that runs fsearch

#
# "edist" is the 2D array returned by heuristics.edist_grid(fline, walls). It contains for
# each position a rough estimate of the length of the shortest path to the finish line.
#
# "values" is a map that stores the expected cost of getting to goal from every of the
# generated states
#
# "expanded" is a map that maps each of the expanded states (i.e., the states whose children
# have been added to "values") to its applicable actions.
#
# expanded.keys() is a subset of values.keys()
#
# "crash_cost" if the cost of an action if it results in a crash. actions that don't result
# in crashes have a cost of 1.
#
s0, fline, goals, walls, prob_size, crash_cost, edist, policy, values, expanded = (None for i in range(10))

policy_changed = False


def main(s, f, w, time_limit=5):
    """
    :param s: the starting state
    :param f: the finish line
    :param w: the walls that cannot be crossed
    :param time_limit: the maximum search time
    :return: the policy computed for state s

    This function is am implementation of modified LAO* algorithm. Every time it computes
    a better policy for state s, it prints the choice, followed by a linebreak, to a
    file called choices.txt
    """

    # Calculate, or upload from the cache file, each of "edist", "policy", "values",
    # "expanded". Using cache make this algorithm run much faster.
    initialize(s, f, w)

    # values stores the expected cost of getting to goal from every generated state
    if s not in values:    # initialize the value of state s
        values[s] = h_walldist(s)

    # leaves_to_update contains every leaf of s that is neither a goal state nor a dead end
    leaves_to_update = set(filter(lambda x: values[x] != math.inf, leaves(s) - goals))

    # action is the current policy for state s.
    action = policy[s] if s in policy else s[1]
    open("choices.txt", "w").write(str(action) + "\n")
    t = time.time()
    while leaves_to_update:    # has not found a safe policy
        state = random.choice(tuple(leaves_to_update))
        if state not in expanded:
            # state not in "expanded" means LAO* has never been called on this leaf state
            # before. Since this is the first time LAO* update is called on this state, we
            # need to add it to "expanded".
            #
            # applicable(state) returns a map that maps each of the applicable actions
            # to the possible states that may result from taking that action. Therefore,
            # "expanded" is actually a map of maps.
            #
            # Below is a sketch for a key:value pair in "expanded"
            #
            #            {action1 : possible next states,
            #   state :   action2 : possible next states,
            #             action3 : possible next states}
            #
            expanded[state] = applicable(state)

            # At this points some of its children may have been generated and added to
            # "values", but some may have not. We need to make sure every one of its
            # children is added to "values" before we perform the LAO update.
            for move in expanded[state]:
                for child in expanded[state][move]:
                    if child not in values:
                        values[child] = h_walldist(child)

        # perform the LAO update. The update returns when the leaves of the state change
        # or no more progress can be made.
        LAO_update(state)

        # if the policy for state s has changed, print it to "choices.txt"
        if s in policy and action != policy[s]:
            action = policy[s]
            file = open("choices.txt", "a")
            file.write(str(action) + "\n")
            file.close()

        if time.time() - t > 0.5:  # cache the data to disk periodically
            t = time.time()
            update_cache()

        # recalculate the leaves to update
        leaves_to_update = set(filter(lambda x: values[x] != math.inf, leaves(s) - goals))

    update_cache()  # cache the data to disk when finish.
    return action


def LAO_update(s):
    """
    This function performs value updates on s and all of its policy-ancestors, until the
    policy changes or no much more progress can be make.
    """
    global policy_changed, prob_size

    # Z contains s and all policy-ancestors of s.
    Z = ancestors(s)

    # set the initial best move at s. This update may change the policy for s, so
    # reset policy_changed to false.
    Bellman_update(s)
    policy_changed = False

    while not policy_changed:
        # The loop stops if the policy changed or no much more progress can be made
        # The book says the loop should stop when the leaves of s0 changed. But since it's
        # highly likely that a change of policy will result in a change of the leaves of s0,
        # and it's significantly cheaper to verify if the policy has changed, I decided to
        # check if the policy has changed instead.
        r = max(list(map(Bellman_update, Z)))
        if r < prob_size/100: break


def Bellman_update(s):
    """
    :param s: the state to be updated
    :return: the absolute change of the value of s due to the update.
    """
    if values[s] == math.inf: return 0   # if s is a dead end, it cannot be updated.
    policy_old = policy.get(s, None)    # the policy for s before the update
    value_old = values[s]         # the value of s before the update
    costs_to_go = {}     # will map every applicable action to the action's cost-to-go

    # retrieve the applicable actions at s
    expanded[s] = dict(filter(lambda a: not is_dead_move(s, a[0]), expanded[s].items()))

    # compute the cost-to-go for each of the applicable actions as weight sum of the
    # values of the possible child states. Crash is considered a child state with
    # a high value.
    for action in expanded[s]:
        crash_prob = 1
        costs_to_go[action] = 0
        children = expanded[s][action]
        for child in children:
            if values[child] != math.inf:
                costs_to_go[action] += (values[child] + 1) * children[child]
                crash_prob -= children[child]
        costs_to_go[action] = costs_to_go[action] + crash_cost * crash_prob

    # update the policy and the value of s
    if costs_to_go != {}:
        action = min(costs_to_go, key=costs_to_go.get)
        values[s] = costs_to_go[action]
        policy[s] = action
    else:
        values[s] = math.inf
        policy.pop(s, None)

    # check if this update changes the policy.
    if policy_old != policy.get(s, None):
        global policy_changed
        policy_changed = True

    return abs(values[s] - value_old)


def ancestors(s):
    """
    This method iterates through all of the states in "policy" and return those who have state s
    as one of their descendants.
    The returned set contains s itself.
    """
    ancestors = {s}
    for state in policy:
        if s in leaves(state):
            ancestors.add(state)
    return ancestors


def leaves(s, explored=None):
    """
    :param s: The state of which we want to collect the leaves.
    :param explored: The states whose leaves have been collected. This parameter helps the method
              to avoid checking the same state multiple times.
    :return: The leaves of s under the current policy.
    """
    if explored is None:
        explored = {s}
    else:
        explored.add(s)

    if s not in policy:
        return {s}

    leaf_states = set()
    for child in expanded[s][policy[s]]:
        if child not in explored:
            leaf_states |= leaves(child, explored)
    return leaf_states


def applicable(s):
    """
    This function finds the applicable actions at s and associates with each of them the
    possible child states. It returns a map whose keys are the applicable actions and whose
    values are the possible results by taking the actions.
    """
    actions = {(s[1][0] + u, s[1][1] + v) for u in [-1, 0, 1] for v in [-1, 0, 1]}
    if ((0, 0) in actions) and ((s[0], (0, 0)) not in goals):
        actions.remove((0, 0))
    usable = {}
    for action in actions:
        child_states = children(s, action)
        if child_states:
            usable[action] = child_states
    return usable


def children(s, action):
    """
    This function computes all of the possible child states that may be resulted from
    taking the action at state s, and it maps each of the possible child states with a
    possibility that depends on the velocity of the action.
    """
    child_states = {}
    q = ({0:1}, {-1:0.2, 0:0.6, 1:0.2})[abs(action[0]) > 1]
    r = ({0:1}, {-1:0.2, 0:0.6, 1:0.2})[abs(action[1]) > 1]
    for e in [(e1, e2) for e1 in q for e2 in r]:
        p = tuple(map(sum, zip(s[0], action, e)))
        if not crash((s[0], p), walls):
            child_states[(p, action)] = q[e[0]] * r[e[1]]
    return child_states


def is_dead_move(s, action):
    # Check if the action at s has no hope to result in a lawful state.
    for child in expanded[s][action]:
        if (child not in expanded) or (expanded[child] != {}):
            return False
    return True


def goal_states(f):
    # convert the finish line to a list of goal states.
    (x1, y1), (x2, y2) = f
    x = range(min(x1, x2), max(x1, x2) + 1)
    y = range(min(y1, y2), max(y1, y2) + 1)
    return {(p, (0, 0)) for p in set(product(x, y))}


def h_walldist(s):
    """
    This is the provided (slightly modified) heuristic function that approximates distance
    to the goal without ignoring walls. It retrieves the cached values stored in edist and
    add an estimate of how long it will take to stop.
    """
    ((x, y), (u, v)) = s
    hval = float(edist[x][y])

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
    if crash([(x, y), (sx, sy)], walls):
        penalty += math.sqrt(au ** 2 + av ** 2)
    hval = max(hval + penalty, sd)
    return hval


def initialize(s, f, w):
    """
    :param s: the state to start with
    :param f: the finish line
    :param w: the walls

    Calculate, or upload from the cache file, each of "edist", "policy", "values",
    "expanded". Using cache make this algorithm run much faster.

    Meanwhile, set the cost of crash to be 5 times the problem size
    """
    global s0, fline, goals, walls, prob_size, crash_cost, edist, policy, values, expanded
    s0, fline, walls = s, f, w
    goals = goal_states(f)
    prob_size = max({p[0][0] for p in walls})
    crash_cost = prob_size * 5

    data_cache = shelve.open("cache2a")
    if not data_cache or data_cache["fline"] != fline or data_cache["walls"] != walls:
        data_cache["fline"] = fline
        data_cache["walls"] = walls
        data_cache["edist"] = edist_grid(fline, walls)
        data_cache["policy"] = {}
        data_cache["values"] = {}
        data_cache["expanded"] = {}

    edist = data_cache["edist"]
    policy = data_cache["policy"]
    values = data_cache["values"]
    expanded = data_cache["expanded"]
    data_cache.close()


def update_cache():
    # update the cached data.
    data_cache = shelve.open("cache", 'n')
    data_cache["fline"] = fline
    data_cache["walls"] = walls
    data_cache["edist"] = edist
    data_cache["policy"] = policy
    data_cache["values"] = values
    data_cache["expanded"] = expanded
    data_cache.close()
    os.rename("cache.db", "cache2a.db")
