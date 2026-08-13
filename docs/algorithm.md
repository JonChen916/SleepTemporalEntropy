# Operational definition of Sleep Temporal Entropy

## Inputs

The reference implementation reads scored sleep-stage events from an NSRR-style
XML annotation. Each recognized event supplies a stage label, start time in
seconds, and positive duration in seconds. Events not representing Wake, N1,
N2, N3, or REM are ignored. Stage 4 is combined with N3.

## Episode construction

Events are sorted by start time. Adjacent events with the same normalized stage
are merged only when they overlap or are contiguous within floating-point
tolerance. Thus, each retained item represents one continuous stage episode.

## Entropy

For episode durations `d[1], ..., d[n]` in a metric's episode set, let

```text
p[j] = d[j] / sum(d)
STE  = -sum(p[j] * log2(p[j]))
```

Zero or negative durations are invalid. If the episode set is empty, the result
is missing (`None`). A single episode produces an entropy of zero.

Stage-specific metrics use episodes from one stage. NREM STE pools episodes
from N1, N2, and N3. Overall STE pools all recognized episodes, including Wake.
The logarithm base is 2, so entropy is expressed in bits.

## Scope

This definition is an entropy of normalized episode durations. It is not a
sliding-window entropy and is not the Shannon entropy of a stage-transition
matrix. Transition-based metrics described separately in the manuscript are
not implemented here.
