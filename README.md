# MotionBench Studio — research prototype

Evidence-first motion-design inspection. **Not** a validated aesthetic benchmark or a guarantee of 10/10 creative quality.

## Run

Requires Python 3.10+, FFmpeg and FFprobe:

```bash
python motionbench.py output.mp4 --out review --reference inspiration.mp4
```

Emits `review/report.json`: media identity (SHA-256), dimensions, timestamps, possible cuts, audio presence, and explicit coverage. Does not pretend that scene detection proves a transition is good. `aesthetic_score=null` until human-calibrated evaluation exists.

## Planned quality architecture

1. **Brief and reference intake**: genre, audience, creative intent, resolution, duration, sound, explicit constraints; licensed reference metadata.
2. **Reference grammar**: shot segmentation, composition, typographic hierarchy, material, easing, spatial continuity, story, audio rhythm. Annotate confidence and source timestamps.
3. **Production**: separate director, technical renderer, and blind critic; preserve reproducible project source and timeline.
4. **Objective QA**: native-resolution frame decode, black/white flashes, unintended freezes, discontinuities, unsafe crop, text legibility, asset continuity, audio clipping and sync; whitelist intentional holds/cuts.
5. **Transition QA**: full-fps inspection around every boundary and object handoff, not just sparse contact sheets.
6. **Independent evaluation**: blinded panel scores narrative clarity, visual craft, motion, sound, originality, consistency, and reference adherence, with evidence timestamps. Never give the producer's self-rating authority.
7. **Calibration**: genre-specific labeled reference pairs, multiple independent human raters, held-out validation, inter-rater agreement, error bounds. Do not claim a universal 100-point objective aesthetic scale.
8. **Repair loop**: produce → measure → critique → local repair → re-render → recheck; stop only on verified gates or explicit resource budget, not a self-reported score.

## Scoring proposal (not yet calibrated)

Narrative/intent 15; composition/typography 15; animation/timing 20; transitions/continuity 15; materials/lighting/render 10; sound 10; originality 10; technical compliance 5. Genre-specific weights are required; 2D and 3D cannot share all tests. Severe technical violations are hard gates, not merely average-score deductions.

## Limits

- Current prototype measures timestamps and candidate cuts; no exhaustive raster or perceptual QA yet.
- A single pixel is detectable only by lossless, aligned frame comparison or known geometry/source manifests; subjective visual analysis alone cannot promise that.
- No auto-scraping copyrighted award films or asserting their ratings without human annotations.
- No Opus 5.5 API calls, independent judges, Blender/Remotion hooks, or real benchmark calibration implemented yet.
