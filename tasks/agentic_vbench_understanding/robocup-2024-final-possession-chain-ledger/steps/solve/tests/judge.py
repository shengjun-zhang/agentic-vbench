#!/usr/bin/env python3
"""Deterministically grade an ordered RoboCup possession-chain ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


VALID_TEAMS = {"white", "black"}
VALID_ZONES = {"defensive", "middle", "attacking"}
VALID_TERMINALS = {"turnover", "stoppage", "goal"}
MAX_PREDICTIONS = 500


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", required=True, type=Path)
    parser.add_argument("--reward-json", required=True, type=Path)
    parser.add_argument("--reward-txt", required=True, type=Path)
    parser.add_argument("--details-json", type=Path)
    return parser.parse_args()


def canonical(entry: object) -> tuple[object, ...] | None:
    if not isinstance(entry, dict):
        return None
    half = entry.get("half")
    team = entry.get("team")
    kick_count = entry.get("kick_count")
    zone_path = entry.get("zone_path")
    terminal = entry.get("terminal")
    if isinstance(half, bool) or half not in (1, 2) or team not in VALID_TEAMS:
        return None
    if isinstance(kick_count, bool) or not isinstance(kick_count, int) or kick_count < 2:
        return None
    if not isinstance(zone_path, list) or not zone_path:
        return None
    if any(zone not in VALID_ZONES for zone in zone_path):
        return None
    if any(left == right for left, right in zip(zone_path, zone_path[1:])):
        return None
    if terminal not in VALID_TERMINALS:
        return None
    return half, team, kick_count, tuple(zone_path), terminal


def exact_ordered_matches(
    predicted: list[tuple[object, ...]], expected: list[tuple[object, ...]]
) -> int:
    """Order-preserving one-to-one count of exact five-field matches.

    A prediction and a ground-truth chain match only when all five canonical
    fields are identical. No partial or graded credit is awarded.
    """
    previous = [0] * (len(expected) + 1)
    for prediction in predicted:
        current = [0]
        for index, ground_truth in enumerate(expected, start=1):
            if prediction == ground_truth:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(previous[index], current[-1]))
        previous = current
    return previous[-1]


def exact_iou(matches: int, predicted: int, expected: int) -> tuple[float, float, float]:
    """Return precision, recall, and exact-match Jaccard/IoU.

    Matches are the intersection of submitted and reference chains under the
    order-preserving one-to-one alignment. The union counts every submitted
    entry, including malformed entries and duplicates, so the metric penalizes
    both false positives and missing reference chains.
    """
    precision = matches / predicted if predicted else 0.0
    recall = matches / expected if expected else 0.0
    union = predicted + expected - matches
    score = matches / union if union else 0.0
    return precision, recall, score


def main() -> None:
    args = parse_args()
    ground_truth_path = Path(__file__).with_name("ground_truth.json")
    expected_raw = json.loads(ground_truth_path.read_text(encoding="utf-8"))["chains"]
    expected = [canonical(entry) for entry in expected_raw]
    if any(item is None for item in expected):
        raise RuntimeError("invalid verifier ground truth")

    reason = "ok"
    predictions_raw: list[object] = []
    try:
        solution = json.loads(args.solution.read_text(encoding="utf-8"))
        predictions_raw = solution.get("chains", [])
        if not isinstance(predictions_raw, list):
            raise ValueError("chains is not a list")
        if len(predictions_raw) > MAX_PREDICTIONS:
            raise ValueError(f"chains exceeds {MAX_PREDICTIONS} entries")
    except Exception as exc:  # malformed output deterministically scores zero
        reason = f"unreadable solution.json: {exc}"
        predictions_raw = []

    predictions = [item for entry in predictions_raw if (item := canonical(entry)) is not None]
    exact_matches = exact_ordered_matches(predictions, expected)
    precision, recall, reward = exact_iou(
        exact_matches, len(predictions_raw), len(expected)
    )

    details = {
        "reason": reason,
        "n_ground_truth": len(expected),
        "n_predicted": len(predictions_raw),
        "n_schema_valid": len(predictions),
        "exact_matches": exact_matches,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "exact_iou": round(reward, 4),
        "matching": "exact five-field order-preserving one-to-one; no partial credit",
    }
    args.reward_json.parent.mkdir(parents=True, exist_ok=True)
    args.reward_json.write_text(
        json.dumps(
            {
                "reward": round(reward, 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "exact_iou": round(reward, 4),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    args.reward_txt.write_text(f"{round(reward, 4)}\n", encoding="utf-8")
    details_path = args.details_json or args.reward_json.with_name("verifier-details.json")
    details_path.write_text(json.dumps(details, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
