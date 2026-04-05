#!/usr/bin/env python3

import sys

from data_pipeline.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["all", *sys.argv[1:]]))
