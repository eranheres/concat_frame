import subprocess
import os
import click
import re


def get_video_duration(video_file):
    """Get the duration of the video."""
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video_file}'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    duration = float(result.stdout.decode('utf-8').strip())
    return duration

def extract_last_frame(video_file, output_image, seconds=1):
    """Extract the last frame from the video."""
    duration = get_video_duration(video_file)
    # Subtract a small amount to ensure we're within the video duration
    frame_time = max(0, duration - seconds)
    cmd = f'ffmpeg -y -ss {frame_time} -i {video_file} -vframes 1 {output_image}'
    cmd = f'ffmpeg -y -sseof -{seconds} -i {video_file} -update 1 -q:v 1 {output_image}'
    subprocess.run(cmd, shell=True)

def create_frame_video(frame_image, frame_video, duration:float=1):
    """Create a video from a single frame."""
    cmd = f'ffmpeg -y -loop 1 -i {frame_image} -c:v libx264 -t {duration} -pix_fmt yuv420p {frame_video}'
    subprocess.run(cmd, shell=True)

def concatenate_videos(original_video, frame_video, output_video):
    """Concatenate the original video with the frame video."""
    with open('concat_list.txt', 'w') as file:
        file.write(f"file '{original_video}'\n")
        file.write(f"file '{frame_video}'")

    cmd = f'ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy {output_video}'
    subprocess.run(cmd, shell=True)
    os.remove('concat_list.txt')


import hashlib


def calculate_file_hash(filename, hash_algorithm='md5'):
    """
    Calculate the hash of a file using the specified hash algorithm.

    :param filename: The path to the file.
    :param hash_algorithm: The hash algorithm to use ('sha256', 'md5', etc.).
    :return: The hexadecimal hash string of the file.
    """
    hash_func = getattr(hashlib, hash_algorithm)()

    with open(filename, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)

    return hash_func.hexdigest()


@click.command()
@click.option('--count', default=1, help='Number of instances to generate.')
@click.option('--seconds', default=1.0, help='The time from end of file to sample the frame.')
@click.argument('filename')
def main(count, filename, seconds):
    """ A simple script to add frames to the end of a video."""
    # Example usage
    video_file = filename  # Your input video file
    output_image = 'last_frame.jpg'
    frame_video = 'frame_video.mp4'

    extract_last_frame(video_file, output_image, seconds)
    # check that output_image exists
    assert os.path.isfile(output_image)

    for i in range(count):
        output_video = f'output_{i}.mp4'
        create_frame_video(output_image, frame_video, duration=0.05 * i)
        concatenate_videos(video_file, frame_video, output_video)

    for i in range(count):
        output_video = f'output_{i}.mp4'
        print(f'Hash of {output_video}: {calculate_file_hash(output_video)}')

if __name__ == '__main__':
    main()