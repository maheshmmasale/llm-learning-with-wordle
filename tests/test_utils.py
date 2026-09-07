"""Tests for src/utils: config loading/overrides and run logging."""

import json
import logging
from pathlib import Path

import pytest
import yaml

from src.utils.config import apply_overrides, load_config, parse_value
from src.utils.logging import configure_logging, create_run_dir, write_json


def test_load_config_roundtrip_and_rejects_scalar(tmp_path):
    path = tmp_path / "c.yaml"
    path.write_text(yaml.safe_dump({"a": {"b": 1}}), encoding="utf-8")
    assert load_config(path) == {"a": {"b": 1}}
    scalar = tmp_path / "s.yaml"
    scalar.write_text("just a string\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(scalar)


def test_apply_overrides_nested_and_typed():
    config = {"train": {"lr": 0.001}}
    updated = apply_overrides(config, ["train.lr=0.01", "train.steps=100", "new.flag=true"])
    assert updated == {"train": {"lr": 0.01, "steps": 100}, "new": {"flag": True}}
    assert config == {"train": {"lr": 0.001}}  # input untouched
    with pytest.raises(ValueError):
        apply_overrides(config, ["no-equals-sign"])
    assert parse_value("[1, 2]") == [1, 2]


def test_run_dir_and_json_log(tmp_path):
    run = create_run_dir(tmp_path, "smoke", seed=0)
    assert run.is_dir()
    target = run / "metrics.json"
    write_json(target, {"wins": 3})
    assert json.loads(target.read_text(encoding="utf-8")) == {"wins": 3}
    assert not list(run.glob("*.tmp"))


def test_configure_logging_returns_logger():
    assert isinstance(configure_logging("WARNING"), logging.Logger)


def test_experiment_configs_load_and_point_at_real_data():
    root = Path(__file__).resolve().parents[1]
    for name in ("base.yaml", "sft.yaml", "inference.yaml"):
        config = load_config(root / "experiments/configs" / name)
        assert isinstance(config, dict)
    for name in ("base.yaml", "inference.yaml"):
        data = load_config(root / "experiments/configs" / name)["data"]
        assert (root / data["answers"]).is_file()
        assert (root / data["allowed_guesses"]).is_file()
