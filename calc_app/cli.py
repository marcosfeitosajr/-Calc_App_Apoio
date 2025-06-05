import argparse
from .calculator import PotCalculator


def main() -> None:
    parser = argparse.ArgumentParser(description="Run POT UNI calculation")
    parser.add_argument("maxNsd", type=float, help="Maximum vertical load (kN)")
    parser.add_argument("Vxd", type=float, help="Non-seismic longitudinal movement (mm)")
    args = parser.parse_args()

    calc = PotCalculator(args.maxNsd * 1000, args.Vxd)
    results = calc.calculate()
    for key, value in results.to_dict().items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
