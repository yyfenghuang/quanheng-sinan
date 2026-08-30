#!/usr/bin/env python3
"""Print published entry directories, one per line.

The Makefile reads this to decide which entries to build. One job: list.
"""
from __future__ import annotations

from entries import load_published


def main():
    for meta in load_published():
        print(f"entries/{meta['_slug']}")


if __name__ == "__main__":
    main()
