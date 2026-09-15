# Keypoint schema

`data/motion-keypoints.json` uses schema
`rnskill.human-motion.landmarks.v1`.

## Coordinates

- `x`, `y`: normalized image coordinates. `(0, 0)` is the top-left corner.
- `z`: MediaPipe relative depth; it is not a metric camera-space distance.
- `visibility`: model confidence when supplied by the landmark model.
- `time_seconds`: time relative to the extracted segment.
- `source_time_seconds`: time in the original source.

Each frame contains `pose`, `left_hand`, `right_hand`, and `detected`. Landmark
rows are `[x, y, z, visibility]`; missing values are JSON `null`.

## Handedness

`left_hand` and `right_hand` follow MediaPipe Holistic's subject-relative
handedness. Mirrored source footage can make visual left/right appear reversed.
Check the overlay whenever handedness matters downstream.

## Raw and smoothed arrays

The compressed NPZ keeps both raw and smoothed arrays:

- `pose_raw`, `left_hand_raw`, `right_hand_raw`
- `pose_smooth`, `left_hand_smooth`, `right_hand_smooth`

Use smoothed coordinates for preview or soft guidance. Use raw coordinates and
confidence evidence when auditing jumps, swaps, or occlusions.

