# Concat frames

This project is a simple script that generates multiple variants of a video by concatenating frames from a video. It is done by adding the last frame of the video to the original.

## Installation
You should have ffmpeg installed and set in the $PATH variable.
```bash
pip install -r requirements.txt
```

## Usage

```bash
python concat_frames.py --input <input_video> --output <output_video> --frames <number_of_frames>
```

