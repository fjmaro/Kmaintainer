"""rawarranger test"""
from pathlib import Path
import shutil

from kjmarotools.basics import logtools, filetools

from kmaintainer import FileMaintainer


def test_filemaintainer():
    """raw test"""
    here = Path(__file__).parent.resolve()
    base_path = here.joinpath("datasets/totest")

    if base_path.exists():
        shutil.rmtree(base_path)
    shutil.copytree(here.joinpath("datasets/_originals_"), base_path)

    pattrn = ("1*", "2*", "3*", "4*", "5*")
    logger = logtools.get_fast_logger("maintest", base_path)
    mnt = FileMaintainer(base_path, logger, pattrn)
    mnt.run(embedded=True)

    # Verify the results
    src_path = here.joinpath("datasets/_result_")
    files_src = filetools.get_files_tree(
        filetools.get_folders_tree(src_path, pattrn))
    files_src = [x.relative_to(src_path) for x in files_src]

    files_result = filetools.get_files_tree(
        filetools.get_folders_tree(base_path, pattrn))
    files_result = [x.relative_to(base_path) for x in files_result]

    assert len(files_src) == len(files_result)
    for file in files_src:
        assert file in files_result
    for file in files_result:
        assert file in files_src


if __name__ == "__main__":
    test_filemaintainer()
