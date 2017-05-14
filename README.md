# Evolutionary Language Games

## Dependencies

(Python Fire)[https://github.com/google/python-fire]
(numpy)[http://www.numpy.org/]

## Models

### basic\_model

This model implements a version of the evolutionary language game described in
(Nowak et al.)[basic\_model/README.md].

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
