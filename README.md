# Evolutionary Language Games

## Introduction

The evolutionary language game formulates the origin of language as a game-theoretic
problem. It was first described in ["The Evolutionary Language Game" (Nowak, Plotkin, Krakauer)]
(https://www.sciencedirect.com/science/article/abs/pii/S0022519399909815).

The game models a communicative event as an attempt by one agent A to convey accurately
a world-state W to a second agent B. Agent A encodes W as a message, M, which is then
received by B. B's interpretation of M results in an internal representation of a world-state,
W'. M may be received in degenerate form, i.e. transmission errors can
occur. The success of a communicative act is measured as the proximity of W to W'.
The game assumes altruism, i.e. that a successful communicative act benefits both
agents, so both agents are rewarded for successful communication.

## Dependencies

[Python Fire](https://github.com/google/python-fire)

[numpy](http://www.numpy.org/)

## Models

### basic\_model

This model implements a version of the evolutionary language game described in
[Nowak et al.](basic\_model/README.md).

#### Example Usage

```shell
python generate_fire.py basic_model \
  --individuals 10 --signals 6 --meanings 5 --k 5 --terminal "iterations(100)"
```

The population size will be ten. The languages engendered will apply a "lexicon"
of six signals to a semantic space of five discrete meanings. Association
matrices will be inferred with k=5; this means that, for each meaning, a new
member of the population will sample its parent's responses to ech object in the
semantic space five times. Learning will terminate after one hundred iterations.

### iterated\_learning\_model

TODO
