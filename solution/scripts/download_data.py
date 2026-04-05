#!/usr/bin/env python3

import sys

from data_pipeline.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["download", *sys.argv[1:]]))
