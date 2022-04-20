"""running raw arranger by default - example"""
from pathlib import Path

from kmarotools.basics import logtools

from kmaintainer import FileMaintainer


if __name__ == "__main__":
    this_file_path = Path(__file__).parent.resolve()
    logger = logtools.get_fast_logger("FileMaintainer", this_file_path)
    folder_patterns = ("1.*", "2.*", "3.*", "4.*", "5.*", )
    year_bounds = (1800, 2300)
    newest_only = True
    FileMaintainer(this_file_path, logger, folder_patterns, year_bounds,
                   newest_only).run()
