"""
------------------------------------------------------------------------------
Kjmaro Files Modify-date maintainer
------------------------------------------------------------------------------
"""
# pylint: disable=too-many-instance-attributes,too-many-arguments
from logging import Logger
from pathlib import Path
from typing import List, Tuple

from kjmarotools.basics import filetools, conventions, ostools


class FileMaintainer:
    """
    --------------------------------------------------------------------------
    Kjmaro Files Modify-date maintainer
    --------------------------------------------------------------------------
    The purpose of this program is to update the files-modify date according
    to its Kjmaro DIN convention (if the files contain a valid date-in-name
    and this name is in the given year_bounds)
    - base_path2scan: The base folder to scan for photography/media
    - logger: Python logging.Logger class to attach
    - folder_patterns: Positive sub-folders to handle (based on patterns*)
    - neg_base_path: Limit the compatible date bounds of the file/folders.
    - newest_only: If True, only files with modify_date newest than its DIN
                   are updated, if False, all mismatching cases are updated.
    --------------------------------------------------------------------------
    """
    def __init__(self, base_path2scan: Path, logger: Logger,
                 folder_patterns: Tuple[str, ...] = (),
                 year_bounds=(1800, 2300), newest_only: bool = True) -> None:

        # Input variables to the class
        self.base_path2scan = base_path2scan
        self.fld_patterns = folder_patterns
        self.year_bounds = year_bounds
        self.newest_only = newest_only
        self.files2scan: List[Path] = []
        self.log = logger
        self.__phs = "[MNT] <NewModulePhase> "
        self.__res = "[MNT] <NewResultsBlock> "

    def get_files_to_scan(self) -> None:
        """
        ----------------------------------------------------------------------
        Get all the files of the given path to be scanned and return the list
        ----------------------------------------------------------------------
        """
        self.log.info(f"{self.__phs}Scanning files in path...")
        folders2scan = filetools.get_folders_tree(self.base_path2scan,
                                                  self.fld_patterns)
        files_in_path = filetools.get_files_tree(folders2scan)

        inf_msg = f"{self.__phs}Finding files with Kdate-in-name to update..."
        self.log.info(inf_msg)
        for file in files_in_path:
            if conventions.is_file_kdin(file, self.year_bounds):
                din = conventions.get_file_kdin(file, self.year_bounds)
                mdt = ostools.get_file_modify_date(file)
                upd_newest = self.newest_only and mdt > din
                upd_matchs = not self.newest_only and mdt != din
                if upd_newest or upd_matchs:
                    self.files2scan.append(file)

    def start_files_scanner(self) -> None:
        """
        ----------------------------------------------------------------------
        Update the modify date of all the files which matching the Kjmaro DIN
        naming convention with the DIN value
        ----------------------------------------------------------------------
        """
        totl = len(self.files2scan)
        inf_msg = f"{self.__res}Updating {totl} files modification dates..."
        self.log.info(inf_msg)
        for file in self.files2scan:
            date2add = conventions.get_file_kdin(file, self.year_bounds)
            ostools.set_file_modify_date(file, date2add)
            self.log.info("[MNT] [DateUpdated]: %s", file)

    def run(self, embedded=False) -> None:
        """
        ----------------------------------------------------------------------
        Execute FileMaintainer with the defined configuration
        - log_actions: log the files scanned
        - embedded: It won't stop after the execution
        ----------------------------------------------------------------------
        """
        self.log.info("[MNT] <INIT> FileMaintainer initialized ...")
        self.log.info(f"[MNT] <CNFG> base_path2scan = {self.base_path2scan}")
        self.log.info(f"[MNT] <CNFG> fld_patterns = {self.fld_patterns}")
        self.log.info(f"[MNT] <CNFG> year_bounds = {self.year_bounds}")
        self.log.info("[MNT] <TAGS> [DateUpdated]")

        self.get_files_to_scan()
        self.start_files_scanner()

        if not embedded:
            input("\nPROCESS FINALIZED\n\t\tPRESS ENTER TO RESUME")
