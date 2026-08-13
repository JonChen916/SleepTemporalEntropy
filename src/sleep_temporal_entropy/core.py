"""Core calculations for Sleep Temporal Entropy (STE)."""

from dataclasses import dataclass
from math import fsum, isclose, log2
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Union
import xml.etree.ElementTree as ET


STAGES = ("Wake", "N1", "N2", "N3", "REM")

_STAGE_MAPPING = {
    "Wake": "Wake",
    "Stage 1 sleep": "N1",
    "Stage 2 sleep": "N2",
    "Stage 3 sleep": "N3",
    "Stage 4 sleep": "N3",
    "REM sleep": "REM",
}


@dataclass(frozen=True)
class StageEpisode:
    """A scored sleep-stage interval measured in seconds."""

    stage: str
    start: float
    duration: float

    def __post_init__(self) -> None:
        if self.stage not in STAGES:
            raise ValueError("Unrecognized normalized sleep stage: %s" % self.stage)
        if self.start < 0:
            raise ValueError("Episode start time must be non-negative.")
        if self.duration <= 0:
            raise ValueError("Episode duration must be positive.")

    @property
    def end(self) -> float:
        return self.start + self.duration


def parse_nsrr_xml(path: Union[str, Path]) -> List[StageEpisode]:
    """Parse recognized scored-stage events from an NSRR-style XML file."""

    root = ET.parse(path).getroot()
    events: List[StageEpisode] = []

    for event in root.findall(".//ScoredEvent"):
        concept_node = event.find("EventConcept")
        start_node = event.find("Start")
        duration_node = event.find("Duration")
        if concept_node is None or start_node is None or duration_node is None:
            continue
        if concept_node.text is None or start_node.text is None or duration_node.text is None:
            continue

        concept = concept_node.text.split("|", 1)[0].strip()
        stage = _STAGE_MAPPING.get(concept)
        if stage is None:
            continue

        try:
            events.append(
                StageEpisode(
                    stage=stage,
                    start=float(start_node.text),
                    duration=float(duration_node.text),
                )
            )
        except ValueError as exc:
            raise ValueError("Invalid scored-stage event in %s: %s" % (path, exc)) from exc

    return sorted(events, key=lambda item: (item.start, item.end))


def merge_consecutive_events(events: Iterable[StageEpisode]) -> List[StageEpisode]:
    """Merge overlapping or contiguous adjacent events of the same stage."""

    ordered = sorted(events, key=lambda item: (item.start, item.end))
    merged: List[StageEpisode] = []

    for event in ordered:
        if not merged:
            merged.append(event)
            continue

        previous = merged[-1]
        contiguous = event.start <= previous.end or isclose(
            event.start, previous.end, rel_tol=0.0, abs_tol=1e-9
        )
        if event.stage == previous.stage and contiguous:
            merged[-1] = StageEpisode(
                stage=previous.stage,
                start=previous.start,
                duration=max(previous.end, event.end) - previous.start,
            )
        else:
            merged.append(event)

    return merged


def shannon_entropy(durations: Sequence[float]) -> Optional[float]:
    """Return base-2 entropy of positive durations normalized by their sum."""

    if not durations:
        return None
    if any(duration <= 0 for duration in durations):
        raise ValueError("All episode durations must be positive.")
    if len(durations) == 1:
        return 0.0

    total = fsum(durations)
    return -fsum((duration / total) * log2(duration / total) for duration in durations)


def calculate_entropies(events: Iterable[StageEpisode]) -> Dict[str, Optional[float]]:
    """Calculate stage-specific, overall, and NREM temporal entropies."""

    episodes = merge_consecutive_events(events)
    durations = {
        stage: [episode.duration for episode in episodes if episode.stage == stage]
        for stage in STAGES
    }

    result: Dict[str, Optional[float]] = {
        "%s_Time_Entropy" % stage: shannon_entropy(durations[stage])
        for stage in STAGES
    }
    result["Overall_Time_Entropy"] = shannon_entropy(
        [episode.duration for episode in episodes]
    )
    result["NREM_Time_Entropy"] = shannon_entropy(
        durations["N1"] + durations["N2"] + durations["N3"]
    )
    return result


def calculate_sleep_temporal_entropy(
    annotation_file_path: Union[str, Path]
) -> Dict[str, Optional[float]]:
    """Calculate STE metrics from an NSRR-style XML annotation file."""

    return calculate_entropies(parse_nsrr_xml(annotation_file_path))
