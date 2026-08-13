from math import isclose

import pytest

from sleep_temporal_entropy import (
    StageEpisode,
    calculate_entropies,
    calculate_sleep_temporal_entropy,
    merge_consecutive_events,
    parse_nsrr_xml,
    shannon_entropy,
)


def test_shannon_entropy_known_values():
    assert shannon_entropy([]) is None
    assert shannon_entropy([30.0]) == 0.0
    assert shannon_entropy([30.0, 30.0]) == 1.0
    assert isclose(shannon_entropy([60.0, 30.0]), 0.9182958340544896)


def test_shannon_entropy_rejects_nonpositive_duration():
    with pytest.raises(ValueError, match="positive"):
        shannon_entropy([30.0, 0.0])


def test_merge_only_contiguous_same_stage_events():
    events = [
        StageEpisode("N2", 0.0, 30.0),
        StageEpisode("N2", 30.0, 30.0),
        StageEpisode("N2", 90.0, 30.0),
    ]
    assert merge_consecutive_events(events) == [
        StageEpisode("N2", 0.0, 60.0),
        StageEpisode("N2", 90.0, 30.0),
    ]


def test_stage4_is_normalized_to_n3(tmp_path):
    xml = tmp_path / "stage4.xml"
    xml.write_text(
        "<PSGAnnotation><ScoredEvents><ScoredEvent>"
        "<EventConcept>Stage 4 sleep|4</EventConcept>"
        "<Start>0</Start><Duration>30</Duration>"
        "</ScoredEvent></ScoredEvents></PSGAnnotation>",
        encoding="utf-8",
    )
    assert parse_nsrr_xml(xml) == [StageEpisode("N3", 0.0, 30.0)]


def test_calculate_entropies_has_manuscript_output_fields():
    result = calculate_entropies(
        [
            StageEpisode("Wake", 0.0, 30.0),
            StageEpisode("N1", 30.0, 30.0),
            StageEpisode("N2", 60.0, 60.0),
            StageEpisode("N1", 120.0, 30.0),
            StageEpisode("REM", 150.0, 60.0),
        ]
    )
    assert set(result) == {
        "Wake_Time_Entropy",
        "N1_Time_Entropy",
        "N2_Time_Entropy",
        "N3_Time_Entropy",
        "REM_Time_Entropy",
        "Overall_Time_Entropy",
        "NREM_Time_Entropy",
    }
    assert result["N3_Time_Entropy"] is None
    assert result["N1_Time_Entropy"] == 1.0


def test_synthetic_xml_end_to_end():
    result = calculate_sleep_temporal_entropy("examples/synthetic_sleep_stages.xml")
    assert isclose(result["Wake_Time_Entropy"], 0.9182958340544896)
    assert result["N1_Time_Entropy"] == 1.0
    assert isclose(result["N2_Time_Entropy"], 0.9709505944546686)
    assert result["N3_Time_Entropy"] == 0.0
    assert isclose(result["REM_Time_Entropy"], 0.9709505944546686)
    assert result["Overall_Time_Entropy"] is not None
    assert result["NREM_Time_Entropy"] is not None
