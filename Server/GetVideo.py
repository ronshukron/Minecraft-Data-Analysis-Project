import argparse
import urllib.request
import os

parser = argparse.ArgumentParser(description="Download OpenAI contractor datasets")
parser.add_argument("--video-path", type=str, required=True, help="Path of the video to download")
parser.add_argument("--output-dir", type=str, required=True, help="Path to the output directory")

def main(args):
    base_url = "https://openaipublic.blob.core.windows.net/minecraft-rl/"
    video_url = base_url + args.video_path
    jsonl_url = video_url.replace(".mp4", ".jsonl")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    video_filename = os.path.basename(video_url)
    jsonl_filename = video_filename.replace(".mp4", ".jsonl")

    video_outpath = os.path.join(args.output_dir, video_filename)
    jsonl_outpath = os.path.join(args.output_dir, jsonl_filename)

    print(f"Downloading video: {video_url} to {video_outpath}")
    try:
        urllib.request.urlretrieve(video_url, video_outpath)
    except Exception as e:
        print(f"Error downloading video: {e}")
        return

    print(f"Downloading JSONL: {jsonl_url} to {jsonl_outpath}")
    try:
        urllib.request.urlretrieve(jsonl_url, jsonl_outpath)
    except Exception as e:
        print(f"Error downloading JSONL: {e}")
        os.remove(video_outpath)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
