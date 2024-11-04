import argparse
import os
import sys
import zlib


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("command")
    arg_parser.add_argument("-p", dest="blob_path")
    args = arg_parser.parse_args()

    command = args.command
    if command == "init":
        init()
    elif command == "cat-file":
        cat_file(args.blob_path)
    else:
        raise RuntimeError(f"Unknown command #{command}")


def cat_file(blob_path):
    with open(rf".git/objects/{blob_path[:2]}/{blob_path[2:]}", "rb") as f:
        # f.readlines()
        print(zlib.decompress(f.read()).decode("utf-8").split("\0")[1], end="")


def init():
    os.mkdir(".git")
    os.mkdir(".git/objects")
    os.mkdir(".git/refs")
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Initialized git directory")


if __name__ == "__main__":
    main()
