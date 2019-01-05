# Artificial-Intelligence-Planning
CMSC722 at UMCP Spring 2018
      
This repo contains two projects that were requirements for the graduate level "AI Planning" course offered at University of Maryland College Park, spring 2018. Both projects were implemented in Python 3.

## Contents
* [`Part 1`](part1):  Comparing the **F**ast **F**orward (FF) heuristic with a domain-specific heuristic on racetrack.
* [`Part 2`](part2):  Planning and Acting on racetrack with unreliable steering.

## Introduction
The project deals with 2D racetrack problems, for which there are three possible state-variable representations. See the detailed explanation below.

### 1. Problem domain
- 2-D polygonal region
  - Inside are a starting point, finish line, maybe obstacles
- All walls are straight lines
- All coordinates are nonnegative integers
- Robot vehicle begins at starting point, can make certain kinds of moves
- Control system introduces small random errors
- Want to move it to the finish line as quickly as possible
  - Without crashing into any walls
  - Need to come to a complete stop on the finish line
  
See figure 1 for an example of the problem domain.

### 2. State-variable representations
- `Representation 1`: state variables x, y for location, and u, v for velocity
  - Each state variable’s value is an integer
- `Representation 2`: state variables p and z: current location, current velocity
  - Each state variable’s value is a pair of integers
- `Representation 3`: one state variable s: current state
  - Value is a 4-tuple of integers

In each representation, the locations of the walls are rigid properties.

## Part 1: Comparing the FF heuristic with a domain-specific heuristic 

### Author
[Fan Yang](mailto:fyang3@cs.umd.edu)

### Licence
Refer to `Licence` for more details.
