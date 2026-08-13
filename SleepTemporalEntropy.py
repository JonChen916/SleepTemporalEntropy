"""Backward-compatible imports for the original single-file interface.

New code should import from :mod:`sleep_temporal_entropy`.
"""

from pathlib import Path
from typing import Optional, Union
import warnings

from sleep_temporal_entropy import calculate_sleep_temporal_entropy, parse_nsrr_xml


def parse_xml_annotation(annotation_file_path):
    """Return parsed stage episodes using the maintained package implementation."""

    warnings.warn(
        "parse_xml_annotation is deprecated; use parse_nsrr_xml instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return parse_nsrr_xml(annotation_file_path)


def calculate_SleepTemporalEntropy(
    edf_file_path: Optional[Union[str, Path]],
    annotation_file_path: Optional[Union[str, Path]] = None,
):
    """Compatibility wrapper; EDF input is no longer required or read."""

    warnings.warn(
        "calculate_SleepTemporalEntropy is deprecated; use "
        "calculate_sleep_temporal_entropy(annotation_file_path).",
        DeprecationWarning,
        stacklevel=2,
    )
    annotation = annotation_file_path if annotation_file_path is not None else edf_file_path
    if annotation is None:
        raise TypeError("An annotation XML path is required.")
    return calculate_sleep_temporal_entropy(annotation)


__all__ = ["calculate_SleepTemporalEntropy", "parse_xml_annotation"]
