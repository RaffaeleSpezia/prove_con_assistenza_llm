"""Simple Moon Lander game.

This script implements a text-based version of the classic Moon Lander
in which the player controls the thrust of a lunar module to attempt a
soft landing on the moon's surface.

Run the game with:
    python moonlander.py

Run an automated demo with:
    python moonlander.py --demo
"""

from __future__ import annotations

import argparse
from typing import Callable

GRAVITY = 1.6  # Acceleration due to gravity (m/s^2)
THRUST_PER_FUEL = 0.15  # Reduction in velocity per unit of fuel burned


def prompt_burn(altitude: float, velocity: float, fuel: int) -> int:
    """Ask the user how much fuel to burn this turn."""
    while True:
        try:
            value = int(input("Fuel to burn: "))
        except ValueError:
            print("Enter an integer value.")
            continue
        if value < 0:
            print("Cannot burn negative fuel.")
            continue
        if value > fuel:
            print("Not enough fuel.")
            continue
        return value


def demo_burn(altitude: float, velocity: float, fuel: int) -> int:
    """Simple autopilot used for the --demo mode.

    The strategy is intentionally naive: it tries to maintain a safe
    landing speed by burning more fuel as the craft gets close to the
    surface.
    """
    if altitude > 50:
        # Maintain a moderate speed when far from the surface
        target_velocity = 10
    else:
        # Slow down to a crawl for the final approach
        target_velocity = 2

    required = int((velocity + GRAVITY - target_velocity) / THRUST_PER_FUEL)
    if required < 0:
        required = 0
    if required > fuel:
        required = fuel
    return required


def play(burn_func: Callable[[float, float, int], int]) -> bool:
    """Run the main game loop.

    Returns True if the player lands safely, False otherwise.
    """
    altitude = 100.0  # meters
    velocity = 0.0    # m/s downward (positive is downward)
    fuel = 100        # units of fuel

    print("Welcome to Moon Lander!\n")

    while altitude > 0:
        print(f"Altitude: {altitude:.1f} m  Velocity: {velocity:.1f} m/s  Fuel: {fuel}")
        burn = burn_func(altitude, velocity, fuel)
        # Update physics
        acceleration = GRAVITY - THRUST_PER_FUEL * burn
        velocity += acceleration
        altitude -= velocity
        fuel -= burn
        if fuel <= 0 and altitude > 0:
            print("\nOut of fuel!")
            burn_func = lambda a, v, f: 0  # no more burning

    print("\nTouchdown!")
    print(f"Final velocity: {velocity:.1f} m/s")
    return velocity <= 5


def main() -> None:
    parser = argparse.ArgumentParser(description="Moon Lander game")
    parser.add_argument("--demo", action="store_true", help="run the autopilot demo")
    args = parser.parse_args()

    burn_func = demo_burn if args.demo else prompt_burn
    success = play(burn_func)
    if success:
        print("You have landed safely. Congratulations!")
    else:
        print("You crashed on the lunar surface.")


if __name__ == "__main__":
    main()
