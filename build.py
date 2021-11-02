#!/usr/bin/env python3

import os
import sys
import json
import argparse
import subprocess
from logging import basicConfig, getLogger, StreamHandler, NullHandler, DEBUG, INFO, Formatter
logger = getLogger(__name__)
logger.addHandler(NullHandler())
basicConfig(level=DEBUG, format='[{levelname:5}] {name}(L{lineno:3}): {message}', style='{')

def find_dockerfile_dirs():
    import glob
    import os
    dockerfile_paths = glob.glob("*/**/Dockerfile", recursive=True)
    dockerfile_dirs = list(map(lambda path: os.path.dirname(path), dockerfile_paths))
    return dockerfile_dirs

class CommandRunnner():
    def __init__(self, dry_run_mode=False):
        self.dry_run_mode = dry_run_mode
        if self.dry_run_mode:
            logger.info("Currently dry-run mode.")

    def run(self, command):
        logger.debug(f"RUN: {command}")
        if not self.dry_run_mode:
            subprocess.run(command, shell=True)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--dry-run", action="store_true", default=False)
    parser.add_argument("--push", action="store_true", default=False)
    parser.add_argument("contexts", nargs="*", help="contexts")
    args = parser.parse_args(args)

    contexts = args.contexts
    if not contexts:
        contexts = find_dockerfile_dirs()

    with open("versions.json", "r") as f:
        versions = json.load(f)

    command_runner = CommandRunnner(dry_run_mode=args.dry_run)

    for context in contexts:

        name, tag = context.split('/', 1)
        version = versions[context]["version"]
        tag = f"gitlab.com/docker_base_images/{name}:{tag}-{version}"
        command_runner.run(f"docker build -t {tag} {context}")

        if args.push:
            command_runner.run(f"docker push {tag}")

if __name__ == "__main__":
    main()
