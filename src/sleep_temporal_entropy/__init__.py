"""Reference implementation of Sleep Temporal Entropy."""

from .core import (
    STAGES,
    StageEpisode,
    calculate_entropies,
    calculate_sleep_temporal_entropy,
    merge_consecutive_events,
    parse_nsrr_xml,
    shannon_entropy,
)

__all__ = [
    "STAGES",
    "StageEpisode",
    "calculate_entropies",
    "calculate_sleep_temporal_entropy",
    "merge_consecutive_events",
    "parse_nsrr_xml",
    "shannon_entropy",
]

__version__ = "1.0.0"
