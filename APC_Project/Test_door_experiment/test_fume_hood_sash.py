#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys

from ochra_apc_devices.devices.fume_hood_sash.driver import FumeHoodSashDriver

from _common import add_connection_arguments
from _common import add_runtime_arguments
from _common import run_cli
from _common import run_step


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manual test script for the fume hood sash device."
    )
    add_connection_arguments(
        parser,
        default_address=FumeHoodSashDriver.DEFAULT_ADDRESS,
        default_port=FumeHoodSashDriver.DEFAULT_PORT,
        default_timeout=FumeHoodSashDriver.DEFAULT_TIMEOUT_SECONDS,
    )
    add_runtime_arguments(parser)
    parser.add_argument(
        "--action",
        choices=("up", "down", "cycle"),
        default="cycle",
        help="Action to perform. Default: cycle",
    )
    return parser


def build_driver(args: argparse.Namespace) -> FumeHoodSashDriver:
    driver = FumeHoodSashDriver(
        device_name="fume_hood_sash",
        connection_mode="tcp",
        address=args.address,
        port=args.port,
        simulation=False,
        timeout_seconds=args.timeout,
        movement_delay_seconds=args.observe_seconds if not args.prompt else 0,
    )
    driver.connect()
    return driver


def run_actions(driver: FumeHoodSashDriver, args: argparse.Namespace) -> None:
    if args.action in {"up", "cycle"}:
        run_step(label="move sash up", action=driver.move_up, observe_seconds=args.observe_seconds, prompt=args.prompt)
    if args.action in {"down", "cycle"}:
        run_step(
            label="move sash down",
            action=driver.move_down,
            observe_seconds=args.observe_seconds,
            prompt=args.prompt,
        )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run_cli(
        device_name="fume_hood_sash",
        address=args.address,
        port=args.port,
        driver_factory=lambda: build_driver(args),
        args=args,
        action_runner=run_actions,
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

