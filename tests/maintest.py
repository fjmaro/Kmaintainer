"""rawarranger test"""
from pathlib import Path
import shutil

from kjmarotools.basics import logtools

from kmaintainer import FileMaintainer


def filemaintainer():
    """raw test"""
    here = Path(__file__).parent.resolve()
    base_path = here.joinpath("datasets/totest")

    if base_path.exists():
        shutil.rmtree(base_path)
    shutil.copytree(here.joinpath("datasets/originals"), base_path)

    logger = logtools.get_fast_logger("maintest", base_path)
    mnt = FileMaintainer(base_path, logger, ("1*", "2*", "3*", "4*", "5*"))
    mnt.run()


if __name__ == "__main__":
    filemaintainer()
