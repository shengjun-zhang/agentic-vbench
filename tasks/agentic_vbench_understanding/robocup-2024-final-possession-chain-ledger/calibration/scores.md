# Calibration - robocup-2024-final-possession-chain-ledger

The final qualification pass must use the exact checked-in instruction, verifier,
task commit, and image built from the digest-pinned Dockerfile. The sole official
reward and difficulty gate is **exact order-preserving full-chain IoU (Jaccard)** (all five of
`half`, `team`, `kick_count`, `zone_path`, `terminal` must match). Precision and
recall are reported only as diagnostics. Do not mix results from earlier weighted or
partial-credit scorer revisions into this table.

Every row below was re-scored under the finalized judge
(`steps/solve/tests/judge.py`, SHA256
`1b2e7a5d6111d54fe33af2dd40bb2c5133a307fcc126efb31772b1580ea74cd6`) against the
submitted `solution.json` recorded in each retained job. Submitted solutions and
trajectories were not modified. Reproducible score/details bundles and manifests are
under `jobs/robocup-review-fix-rescore-20260830/`.

## End-to-end agents

Official reward is the `exact IoU` column. `precision`/`recall`/`n_pred`/`schema_valid`/
`exact` are diagnostics.

| harness | harness version | model | reasoning | exact IoU | precision | recall | n_pred | schema_valid | exact | tool-call turns | trajectory asset | whole-file SHA256 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Codex | Harbor 0.20.0 + direct Responses harness | GPT-5.6 Sol | high | 0.0000 | 0.0000 | 0.0000 | 8 | 8 | 0 | 64 | [release bundle](https://github.com/shengjun-zhang/agentic-vbench/releases/download/robocup-possession-chain-iou-20260907/codex-e2e.tar.gz) | `a426ec0c084362eb5fe6de75643d18ac151d9d1252e08e81976c97cc278d97d3` |
| Claude Code | Harbor 0.20.0 + manual wrapper | Claude Opus 4.8 | xhigh | 0.0571 | 0.1000 | 0.1176 | 20 | 20 | 2 | 416 | [release bundle](https://github.com/shengjun-zhang/agentic-vbench/releases/download/robocup-possession-chain-iou-20260907/claude-e2e.tar.gz) | `5025c388c679b6a07aced5de8a53628176f36cc7e51c5b809e16aa88d25baed1` |
| Antigravity CLI | 1.1.21 | Gemini 3.5 Flash | high | 0.0213 | 0.0253 | 0.1176 | 79 | 79 | 2 | 145 | [release bundle](https://github.com/shengjun-zhang/agentic-vbench/releases/download/robocup-possession-chain-iou-20260907/antigravity-e2e.tar.gz) | `ad1f9812032649f8a59c8a996da901e88ca9814f32e7885d44429c29f1b96350` |

The selected Claude Code row is the clean September 6 run. Its exact IoU is `0.0571`,
below the `0.10` gate, with 20 submitted chains and 2 exact matches.

## Anti-shortcut ablations

All four rows are real GPT-5.6 Sol runs under the final image and scorer, re-scored
under the finalized exact-IoU judge. Exact input conditions are fixed in
`ablations/README.md`.

| condition | exact IoU | precision | recall | n_pred | schema_valid | exact | tool-call turns | trajectory asset | whole-file SHA256 |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Prompt/schema, no media | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 0 | 2 | [release bundle](https://github.com/shengjun-zhang/agentic-vbench/releases/download/robocup-possession-chain-iou-20260907/ablation-nomedia.tar.gz) | `55dbfa7c3be082e6c3b7c523c3d93987e53cc59952204b4f33043f6323dceab1` |
| One temporal-midpoint frame | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 0 | 7 | [release bundle](https://github.com/shengjun-zhang/agentic-vbench/releases/download/robocup-possession-chain-iou-20260907/ablation-single-frame.tar.gz) | `b3eb7a96e0a5df534223c06cdeda6f66e3f5140e2615fd7fe37fd8dc70383250` |
| OCR-only timeline | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 0 | 4 | [release bundle](https://github.com/shengjun-zhang/agentic-vbench/releases/download/robocup-possession-chain-iou-20260907/ablation-ocr.tar.gz) | `6ca09d160ef1c730367f24fc269682d5ea4f83587138099a0c1d829bd9a8c2c3` |
| Every native frame pasted, no tools (independent replicate) | 0.0185 | 0.0263 | 0.0588 | 38 | 38 | 1 | 0 | [release bundle](https://github.com/shengjun-zhang/agentic-vbench/releases/download/robocup-possession-chain-iou-20260907/ablation-allframes-notools.tar.gz) | `06a8d15016e4f0688121875450c2ff363911fd42af2a129d9560d509012b25ba` |

The three degraded-input rows above produced no `solution.json`
(`n_predicted = 0`), so they score `0.0` under any metric. The all-frame row is the
pre-registered independent replicate: one exact full-chain match out of 38 submitted
entries against 17 ground-truth chains gives precision `0.0263`, recall `0.0588`, and
exact IoU `0.0185`. It used all 44,032 decoded frames in 111 chronological 20-by-20
sheets, one model turn, and no tools or subagents. The earlier all-frame run remains a
reproducibility diagnostic rather than the selected row.

The immutable bundle archives are published in the
[RoboCup exact-IoU release](https://github.com/shengjun-zhang/agentic-vbench/releases/tag/robocup-possession-chain-iou-20260907);
their whole-file SHA256 values are:

| bundle | SHA256 |
|---|---|
| `codex-e2e.tar.gz` | `73d01016602e6f57f2c8eda118530ec27498cc8a8a584fa586520b3356dbbce7` |
| `claude-e2e.tar.gz` | `b38a63503c592c43c7684c2e613ce0d404089c6d73e0241d1373a455e05df97c` |
| `antigravity-e2e.tar.gz` | `51af33c5ed420549c7303592e8e2fee1bca86512f2480dfe20bd4eed4650737b` |
| `ablation-nomedia.tar.gz` | `ac7228cd359937cb1ea81c30983f1927f3ed96cb066141a03517282ab257fd68` |
| `ablation-single-frame.tar.gz` | `8e21a31a1fcff64dfce741fa316d7602b63cfdd9b785c4d5b4a1909c645308ac` |
| `ablation-ocr.tar.gz` | `285f1cc224822a719b4bce3365a6b33a75642393d8a809d7ad32598718e0e42d` |
| `ablation-allframes-notools.tar.gz` | `32e0c7e0445c661572d8d9e4b3e0f2380a06cf052213c93abb4bda2e3a5a0002` |

Condition-specific provenance:

| condition | runtime image ID | degraded-input identity |
|---|---|---|
| No media | `sha256:24cd22f53369b31ab4b10ad6cad3e95573c96882466ae242c8bcf92a53703b5f` | both MP4 locations absent |
| Single frame | `sha256:3fe7e6d2c2933cb460f5351ae0c8eb497124e01b1cc3ce884c3c3b24541b86a3` | F22016, one 1280x720 frame; media SHA256 `75433540904e9a9d966d7dfdaf8d8e60134c2d20da5e0fd9d2ed6245a8f61ace` |
| OCR only | `sha256:f27267214f7093b3e1466d48f3aba88b2c1dba3e5a4ec860110d40969e5958fe` | 177 timestamps and 6,175 text boxes; artifact SHA256 `9a59563e7d7df2127f7b0346d269069cd0276feaa4b55d6d17a4419a4f5703c8` |
| All frames, no tools replicate | `sha256:73a4d049db3ada73882107a4e792c5e3340195224a205c7453de8bb3a4410912` | 44,032 frames; 111-sheet manifest SHA256 `011a16c3aafee19272d9eeab8321abd4110ae7b8eafd41f86c40dfec6f033325` |

## Run identity

Record these once the final image is built and do not change the task between rows:

| item | value |
|---|---|
| task commit | `7553740b95925b21a11000ec4d7256c127020577` |
| Harbor version | `0.20.0` |
| verifier judge SHA256 | `1b2e7a5d6111d54fe33af2dd40bb2c5133a307fcc126efb31772b1580ea74cd6` |
| Codex image ID | `sha256:ae98225846c1c83bb058392f1582e14b1dffea753d3a0ed2d38832a831631a39` |
| Claude image ID | `sha256:ed8de26cfd100adf229adad2e0b8d70984d4ba002ef218b6145f57885e5937dc` |
| Antigravity image ID | `sha256:b0d91055dca04597508994f693c9cc00b16bfeb5bfa2130a349fde0e66a7eeee` |
| base image digest | `python:3.12-slim@sha256:2c941e860699f878900b0edc2403613c234d4b32eda3cc9fa7036991a2a63c4a` |
| default materials URL | `https://github.com/shengjun-zhang/agentic-vbench/releases/download/robocup-possession-chain-iou-20260907/match.mp4` |
| media SHA256 | `076bcc59fc48443d24a72a87162021470b9e645b41c858c3ffa5b5b25bae36cd` |

## Counting rules

The official reward is exact full-chain IoU. For Harbor ATIF trajectories, count
tool-call turns as agent-authored steps containing at least one `tool_calls` object
across the main trajectory and any explicitly referenced subagent trajectories.
Record the raw tool-call count and any harness-native comparison count separately when
they differ. A run clears the difficulty gate only when exact full-chain IoU is below
`0.10` for every reported strong-agent and ablation row, and a genuine end-to-end
attempt exceeds 50 tool-call turns.

Antigravity records its tool progress in its native agent log rather than ATIF
`tool_calls` objects. Its 145 tool-call turns are the non-empty action records before
the final answer in that retained log.

The old desktop/local-agent measurements are superseded diagnostics, not formal
calibration: they predate the reviewer-requested scorer and did not use this pinned
isolated environment. The metadata-less schema-invalid Gemini export is dropped.

## Media acquisition validation

The ordinary no-argument Docker build was rerun after the calibration assets were
published. It fetched the public release asset at the default URL recorded above,
then verified SHA256 `076bcc59fc48443d24a72a87162021470b9e645b41c858c3ffa5b5b25bae36cd`
and ffprobe values `1280x720`, `50/1`, and `880.640000` before completing. The
resulting image manifest was
`sha256:368d5d11838495230680432ac03ccec00df418e5e0462c6803d2b148455d3d44`.
This is infrastructure validation only; the retained trajectories above remain
byte-identical and were not rerun.
