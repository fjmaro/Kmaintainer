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
from kjmarotools import proprietdin


class FileMaintainer:
    """
    --------------------------------------------------------------------------
    Kjmaro Files Modify-date maintainer
    --------------------------------------------------------------------------
    The purpose of this program is to update the files-modify date according
    to its Kjmaro DIN convention (if the files contain a valid date-in-name
    and this name is in the given year_bounds). It also includes the
    functionality of renaming 'proprietary' files to KDIN convention.
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
        self.log = logger
        self.__phs = "[MNT] <NewModulePhase> "
        self.__res = "[MNT] <NewResultsBlock> "

    def get_files_tree(self) -> List[Path]:
        """
        ----------------------------------------------------------------------
        Get all the files of the given path to be scanned and return the list
        ----------------------------------------------------------------------
        """
        self.log.info(f"{self.__phs}Scanning files in path...")
        folders2scan = filetools.get_folders_tree(self.base_path2scan,
                                                  self.fld_patterns)
        files_in_path = filetools.get_files_tree(folders2scan)
        return files_in_path

    def rename_proprietary_files(self, file_list: List[Path]) -> List[Path]:
        """
        ----------------------------------------------------------------------
        Rename the files with proprietary-name in the given list
        ----------------------------------------------------------------------
        """
        self.log.info(f"{self.__phs}Finding proprietary files to rename...")
        output_list: List[Path] = []
        duplicated = 0
        renamed = 0

        for file in file_list:
            if proprietdin.is_proprietary_din(file, self.year_bounds):
                new_name = proprietdin.rename_proprietary_din_file(
                    file, self.year_bounds)
                if new_name == file:
                    duplicated += 1
                    kdin_name = proprietdin.kdin_from_proprietary_din(file)
                    self.log.info("[MNT] [Duplicated] (%s): %s",
                                  kdin_name.name,
                                  file.relative_to(self.base_path2scan))
                else:
                    renamed += 1
                    self.log.info("[MNT] [PropRenamed]: %s",
                                  new_name.relative_to(self.base_path2scan))
                output_list.append(new_name)

            else:
                output_list.append(file)

        dplmsg = " (not renamed because the renamed file already exists)"
        self.log.info(f"{self.__res}Files duplicated = {duplicated}" + dplmsg)
        self.log.info(f"{self.__res}Files renamed = {renamed}")
        return output_list

    def update_kdin_filedates(self, files_in_path: List[Path]) -> None:
        """
        ----------------------------------------------------------------------
        Update the modify date of all the files matching the KDIN convention
        ----------------------------------------------------------------------
        """
        self.log.info(f"{self.__phs}Finding KDIN files to update...")
        updated = 0

        for file in files_in_path:
            if conventions.is_file_kdin(file, self.year_bounds):
                din = conventions.get_file_kdin(file, self.year_bounds)
                mdt = ostools.get_file_modify_date(file)
                upd_newest = self.newest_only and mdt > din
                upd_matchs = not self.newest_only and mdt != din

                if upd_newest or upd_matchs:
                    updated += 1
                    ostools.set_file_modify_date(file, din)
                    self.log.info("[MNT] [DateUpdated]: %s",
                                  file.relative_to(self.base_path2scan))
        self.log.info(f"{self.__res}Files updated = {updated}")

    def run(self, embedded=False, rename_propriet=True) -> None:
        """
        ----------------------------------------------------------------------
        Execute FileMaintainer with the defined configuration
        - embedded: It won't stop after the execution
        - rename_propriet: Rename proprietary files to KDIN before updating
        ----------------------------------------------------------------------
        """
        self.log.info("[MNT] <INIT> FileMaintainer initialized ...")
        self.log.info(f"[MNT] <CNFG> base_path2scan = {self.base_path2scan}")
        self.log.info(f"[MNT] <CNFG> fld_patterns = {self.fld_patterns}")
        self.log.info(f"[MNT] <CNFG> year_bounds = {self.year_bounds}")
        self.log.info("[MNT] <TAGS> [Duplicated] [PropRenamed] [DateUpdated]")

        files_tree = self.get_files_tree()
        if rename_propriet:
            files_tree = self.rename_proprietary_files(files_tree)
        self.update_kdin_filedates(files_tree)

        if not embedded:
            input("\nPROCESS FINALIZED\n\t\tPRESS ENTER TO RESUME")
