from timeit import timeit
import heuristics

heur = ["heuristics.h_walldist", "heuristics.h_esdist", "heuristics.h_ff1", "heuristics.h_ff2"]

for i in range(len(heur)):
    t = 0
    for j in range(100):
        if (j + 1) % 20 == 0:
            print("Time test of {} on problem size {}: {} seconds on average\n".format(heur[i], 4*(j+21)//20, t/20))
            t = 0
        s = "racetrack.main(random_probs.problem{}, 'gbf', {}, verbose=1, draw=0)".format(j, heur[i])
        r = "import racetrack, heuristics, random_probs"
        t += timeit(stmt=s, number=1, setup=r)
        heuristics.tear_down()
