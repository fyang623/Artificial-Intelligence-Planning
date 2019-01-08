"""

File: proj2b.py -- Fan Yang, May 5, 2018

This file contains an implementation of modified UCT algorithm.

UCT is a Monte Carlo Tree Search algorithm that explores promising actions more frequently
and prune out rapidly inferior options, with no action left untried.
The trade-off between the number of times an action a has been sampled in s and the
value Q(s, a), i.e., the cost-to-go, can be tuned by adjusting the hyperparameter "C"
in the following equation.

        Q(s, a) - C * sqrt(log(n(s))/n(s, a)

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
from numpy import random as rand
from itertools import product
from heuristics import edist_grid
from racetrack import crash

#
# "edist" is the 2D array returned by heuristics.edist_grid(fline, walls). It contains for
# each position a rough estimate of the length of the shortest path to the finish line.
#
# "envelope" is a map that maps each of the visited states to the applicable actions at that
# state. A value in "envelop" is itself a map that associates each of the applicable actions
# with its information. Therefore, a key:value pair in "envelope" in the following form:
#
#            {action1 : information of action1,
#   state :   action2 : information of action2,
#             action3 : information of action3}
#
# There can be more or fewer than 3 actions for each of the states.
#
# The information of each action is a 4-tuple with the form of
#
#       (times tried, cost-to-go, priority, possible child states)
#
# Within the above tuple, "possible child states" is again a map. It maps each of the child
# states to the probability of getting to that state by taking the action.
#
# The data structure of "envelope" might be a bit overly complex, but it stores most of the
# information we need to calculate the cost of roll-out of any visited state. With the help
# of the information cached in "envelope" the program runs roughly 10~20 times faster.
#
# "crash_cost" if the cost of an action if it results in a crash. actions that don't result
# in crashes have a cost of 1.
#
# "h_max" is the maximum depth that UCT algorithm explores
#

fline, goals, walls, edist, h_max, crash_cost, envelope = (None for i in range(7))


def main(s, f, w, time_limit=5):
    """
    :param s: the starting state
    :param f: the finish line
    :param w: the walls that cannot be crossed
    :param time_limit: the maximum search time
    :return: the policy computed for state s

    This function is am implementation of modified UCT algorithm. Every time it computes a
    better move for state s, it prints the choice, followed by a linebreak, to a
    file called choices.txt
    """
    t = time.time()

    # Calculate, or upload from the cache file, each of "edist", "policy", "values",
    # "expanded". Using cache make this algorithm run significantly faster.
    initialize(s, f, w)

    # action: the policy for state s, initialized to be the current velocity
    # count: the times that "action" has been tried
    # mark: the times that "action" has been tried when it is set to be the policy for s
    if s in envelope and envelope[s]:
        action = min(envelope[s], key=lambda a: envelope[s][a][1])
        count = mark = envelope[s][action][0]
    else:
        action = s[1]
        count = mark = 0

    open("choices.txt", "w").write(str(action) + "\n")

    # count - mark is the number of runs over which the policy at s has stayed the same.
    # If the policy for state s has stayed the same over the last 5000 runs, then it is
    # safe to say that the policy has become stable, thus we can terminate the loop.
    while count - mark < 5000:
        UCT(s, h_max)

        # "candidates" is a map that maps the applicable actions to their information
        candidates = envelope[s]

        # if the state is a dead end, just return the current velocity
        if not candidates: break

        # if the policy for state s has changed, print it to "choices.txt"
        action_new = min(candidates, key=lambda a: candidates[a][1])
        if action != action_new:
            action = action_new
            count = mark = envelope[s][action][0]
            file = open("choices.txt", "a")
            file.write(str(action) + "\n")
            file.close()

        # cache the data to disk periodically
        if time.time() - t > 0.9 * time_limit:
            t = time.time()
            update_cache()

        count += 1
    update_cache()  # cache the data to disk when finish.
    return action


def UCT(s, h):
    """
    :param s: the state to roll out
    :param h: the depth bound of the rollout
    :return:  a tuple (cost, risk).

    In the returned tuple, "cost" is the cost of rollout without considering the risk of crashing
    into walls, and "risk" is the correction to "cost" that takes the walls into consideration.
    Cost of rollout can be computing by simply taking the sum of "cost" and "risk".
    The purpose of having these two separate values is to decrease the weight of the crashing cost
    as the rollout goes deeper. The intuition is simple: a crash that will happen next step should
    weigh more than a crash that will happen 10 steps later.
    """
    if s in goals:
        return 0, 0

    if h == 0:
        return h_walldist(s), 0

    if s not in envelope:      # s has not been explored before
        # the information for each action is (times tried, cost-to-go, priority, child states)
        actions = {action:(0, 0, -math.inf, results) for (action, results) in applicable(s).items()}
        envelope[s] = actions

    if not envelope[s]:      # s has no applicable actions, thus is a dead end
        return h_walldist(s), crash_cost

    # find the action that has the highest (numerically smallest) priority
    action = choose_move(s)
    if action is None:
        return h_walldist(s), crash_cost

    # Randomly sample a child state. The sampled state can be "None", which represents a
    # crash resulted from taking the action.
    child = sample_child(s, action)

    if child is None:
        # "None" represents a crash
        cost, risk = h_walldist(s), crash_cost
    else:
        # recursively call UCT with a decremented depth bound
        cost_child = UCT(child, h - 1)
        cost, risk = 1 + cost_child[0], cost_child[1]/5

    cost_rollout = cost + risk
    n_all = sum([info[0] for info in envelope[s].values()])

    # update the information of the action
    # n, q, p, c = times tried, cost-to-go, priority, child states
    n, q, p, c = envelope[s][action]
    # q = (n * q + cost_rollout) / (n + 1)
    q = (n + 1) * q / (n + q / cost_rollout) if q > 0 else cost_rollout
    p = priority(q, n + 1, n_all + 1)
    envelope[s][action] = (n + 1, q, p, c)

    return cost, risk


def choose_move(s):
    if not envelope[s]: return None

    # if there is an action that has been tried fewer than 100 times, then choose that
    # action; else, choose the action that has the highest (smallest numerically) priority
    actions = envelope[s]
    under_tried = list(filter(lambda a: actions[a][0] < 100, actions))

    if under_tried:
        action = random.choice(under_tried)
    else:
        action = min(actions, key=lambda a: actions[a][2])

    if is_dead_move(s, action):
        envelope[s].pop(action)
        action = choose_move(s)

    return action


def sample_child(s, action):
    """
    Sample a state from the child states that can be achieved by taking the action at
    state s. The probability of a child state getting sampled depends on the probabilities
    of steering errors.
    The sampled child state can be "None", in which case it's considered that a crash
    occurs when taking the action
    """
    if s in envelope:
        child_states = envelope[s][action][3]
    else:
        child_states = children(s, action)

    states, probs = [], []
    for (state, prob) in child_states.items():
        states.append(state)
        probs.append(prob)
    states.append(None)
    probs.append(1 - sum(probs))
    return states[rand.choice(len(states), p=probs)]


def applicable(s):
    """
    This function finds the applicable actions at s and associates with each of them the
    possible child states. It returns a map whose keys are the applicable actions and whose
    values are the possible results by taking the actions.
    """
    actions = {(s[1][0] + u, s[1][1] + v) for u in [-1, 0, 1] for v in [-1, 0, 1]}
    if (0, 0) in actions:
        if (s[0], (0, 0)) in goals:
            actions = {(0, 0)}
        else:
            actions.remove((0, 0))

    usable = {}
    for action in actions:
        child_states = children(s, action)
        if child_states:
            usable[action] = child_states
    return usable


def is_dead_move(s, action):
    # Check if the action at s has no hope to result in a lawful state.
    if s in envelope:
        child_states = envelope[s][action][3]
    else:
        child_states = children(s, action)

    for child in child_states:
        if (child not in envelope) or (envelope[child] != {}):
            return False
    return True


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


def goal_states(f):
    # convert the finish line to a list of goal states.
    (x1, y1), (x2, y2) = f
    x = range(min(x1, x2), max(x1, x2) + 1)
    y = range(min(y1, y2), max(y1, y2) + 1)
    return {(p, (0, 0)) for p in set(product(x, y))}


def priority(cost_to_go, n_this, n_all):
    # In the slides the priority is calculated using the following formula
    #       Q(s, a) - C * sqrt(log(n(s))/n(s, a)
    #
    # "C" is a constant that can be changed to control the expectation-exploration trade-off
    #
    # For reason of computational efficiency, it's approximated by
    #       Q(s, a) - C * n(s)/n(s, a)
    return cost_to_go - n_all / (5 * n_this)   # "5" may be changed to other numbers
    # return cost_to_go - 100*math.sqrt(math.log(n_all)/n_this)


def h_walldist(s):
    """
    This is a lightly modified version of the provided heuristic function that approximates
    distance to the goal. It retrieves the cached values stored in edist and add an estimate
    of how long it will take to stop.
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

    Calculate, or upload from the cache file, "edist" and "envelop".
    Using cache make this algorithm run much faster.

    Meanwhile, set the cost of crash to be 5 times the problem size,
    and the maximum depth bound to be one fourth of the problem size.
    """
    global fline, goals, walls, edist, h_max, crash_cost, envelope
    fline, walls,  = f, w
    goals = goal_states(f)
    crash_cost, h_max = 100, 5

    data_cache = shelve.open("cache2b")
    if not data_cache or data_cache["fline"] != fline or data_cache["walls"] != walls:
        data_cache["fline"] = fline
        data_cache["walls"] = walls
        data_cache["edist"] = edist_grid(fline, walls)
        data_cache["envelope"] = {}

    edist = data_cache["edist"]
    envelope = data_cache["envelope"]
    data_cache.close()


def update_cache():
    # update the cached data.
    data_cache = shelve.open("cache", 'n')
    data_cache["fline"] = fline
    data_cache["walls"] = walls
    data_cache["edist"] = edist
    data_cache["envelope"] = envelope
    data_cache.close()
    os.rename("cache.db", "cache2b.db")
