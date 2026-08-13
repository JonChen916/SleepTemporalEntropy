import json

from sleep_temporal_entropy.cli import main


def test_cli_emits_json(capsys):
    assert main(["examples/synthetic_sleep_stages.xml"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["N3_Time_Entropy"] == 0.0
