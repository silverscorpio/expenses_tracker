import argparse
from datetime import datetime, timedelta


def validate_duration(cmdline_arg: str) -> int | str:
    try:
        isinstance(int(cmdline_arg), int)
        return int(cmdline_arg)
    except ValueError:
        return cmdline_arg


def args_parser() -> int | str:
    cmd_parser = argparse.ArgumentParser(
        description="Fetch and extract transaction data from emails for budget analysis"
    )
    cmd_parser.add_argument(
        "-d",
        type=str,
        default=(datetime.today().date() - timedelta(days=1)).strftime("%Y/%m/%d"),
        help="duration for which transactions need to be fetched",
    )

    args = cmd_parser.parse_args()
    return validate_duration(cmdline_arg=args.d)


if __name__ == "__main__":
    print(args_parser())
