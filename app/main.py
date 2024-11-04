import argparse
import hashlib
import os
import sys
import zlib


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("command")
    arg_parser.add_argument("-p", dest="blob_path")
    arg_parser.add_argument("-w", dest="file_path")
    args = arg_parser.parse_args()

    command = args.command
    if command == "init":
        init()
    elif command == "cat-file":
        cat_file(args.blob_path)
    elif command == "hash-object":
        hash_object(args.file_path)
    else:
        raise RuntimeError(f"Unknown command #{command}")


def cat_file(blob_path):
    with open(rf".git/objects/{blob_path[:2]}/{blob_path[2:]}", "rb") as f:
        # f.readlines()
        print(zlib.decompress(f.read()).decode("utf-8").split("\0")[1], end="")


def hash_object(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
        blob = zlib.compress(
            b"blob" + f" {len(content)}".encode("utf-8") + b"\0" + content
        )
        blob_path = hashlib.sha1(
            b"blob" + f" {len(content)}".encode("utf-8") + b"\0" + content
        ).hexdigest()

    os.mkdir(f".git/objects/{blob_path[:2]}")

    with open(rf".git/objects/{blob_path[:2]}/{blob_path[2:]}", "+wb") as f:
        f.write(blob)

    print(blob_path)


def init():
    os.mkdir(".git")
    os.mkdir(".git/objects")
    os.mkdir(".git/refs")
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Initialized git directory")


if __name__ == "__main__":
    main()
