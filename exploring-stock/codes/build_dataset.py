# codes/build_dataset.py

from .config import (
    DEFAULT_TIKCERS,
    OUTPUT_FILE_NAME,
    DEFAULT_START,
    DEFAULT_END,
)
from .data_loader import save_universe_to_csv


def main() -> None:
    save_universe_to_csv(
        output_name=OUTPUT_FILE_NAME,
        tickers=DEFAULT_TIKCERS,
        start_date=DEFAULT_START,
        end_date=DEFAULT_END,
    )
    print(f"Saved dataset to datasets/{OUTPUT_FILE_NAME}")


if __name__ == "__main__":
    main()
