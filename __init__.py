from os import makedirs
from pathlib import Path
from shutil import which
from subprocess import run
from sys import argv, exit

from . import internals


def flag(flag: str) -> bool:
    """Return true if the flag was passed in the invocation of the compile script"""
    return flag in argv


class Executable:
    """Represents an executable project."""

    __slots__: tuple[str, ...] = (
        "__compiler",
        "__flags",
        "__include_directories",
        "__libraries",
        "__library_directories",
        "__name",
        "__opt_level",
        "__output_dir",
        "__source_files",
    )

    def __init__(self, name: str, compiler: str | None = None) -> None:
        self.__name: str = name
        self.__output_dir: str | None = None

        if compiler is not None:
            self.__compiler: str = compiler
        else:
            system_compiler: str | None = internals.get_default_compiler()
            if system_compiler is not None:
                self.__compiler = system_compiler
            else:
                print("Error: No compiler found on system path")
                exit(1)

        self.__source_files: list[str] = []
        self.__include_directories: list[str] = []
        self.__libraries: list[str] = []
        self.__library_directories: list[str] = []

        self.__flags: list[str] = []
        self.__opt_level = 0

    @property
    def opt_level(self) -> int:
        """The level of optimization to use during compilation.
        Possible levels are 0, 1, 2, and 3.
        Equivalent to the -O flag.
        """
        return self.__opt_level

    @opt_level.setter
    def opt_level(self, level: int) -> None:
        if not 0 <= level <= 3:
            print("WARNING: Opt level must be in the range [0, 3]. Defaulting to 0.")
            self.__opt_level = 0
        else:
            self.__opt_level = level

    @property
    def compiler(self) -> str:
        """The program to use as the compiler.
        NOTE: The specified program must be present on PATH.
        """
        return self.__compiler

    @compiler.setter
    def compiler(self, program: str) -> None:
        if which(program):
            self.__compiler = program
        else:
            print(
                f"[W]: Cannot find program {program}, defaulting to {self.__compiler}"
            )

    def add_include_dir(self, path: str) -> None:
        """Add a directory to the project's include paths.
        Equivalent to the -I flag.
        """
        if path not in self.__include_directories:
            self.__include_directories.append(path)

    def add_source_file(self, file: str) -> None:
        """Add a source file to the project."""
        if file not in self.__source_files:
            self.__source_files.append(file)

    def add_source_dir(self, directory: str, file_names: list[str]) -> None:
        """Add multiple source files to the project.

        This function can be used as a short-hand to the standard `add_source_file` function.
        Instead of one call per file, this function can take multiple files as a list, with
        all the files under one shared directory.
        """
        directory_path: Path = Path(directory)
        for file_name in file_names:
            full_path: str = str(directory_path / file_name)
            if full_path not in self.__source_files:
                self.__source_files.append(full_path)

    def add_flag(self, flag: str) -> None:
        """Add a flag to the project to use during compilation."""
        if flag not in self.__flags:
            self.__flags.append(flag)

    def add_library_dir(self, *, link: str, include: str) -> None:
        """Add a library directory to the project.
        Equivalent to the -L flag.
        """
        if link not in self.__library_directories:
            self.__library_directories.append(link)
        if include not in self.__include_directories:
            self.__include_directories.append(include)

    def add_library(self, library: str) -> None:
        """Add a library to the program.
        Equivalent to the -l flag."""
        if library not in self.__libraries:
            self.__libraries.append(library)

    def set_output_dir(self, directory: str) -> None:
        """Set the project's output directory.
        Creates the directory on build if it does not exist, including all parent directories.
        """
        self.__output_dir = directory

    def build(self) -> None:
        """Build the project as configured."""
        args: list[str] = [self.__compiler]

        args += self.__flags
        args.append(f"-O{self.__opt_level}")

        args += self.__source_files
        for include_dir in self.__include_directories:
            args.append(f"-I{include_dir}")

        for library_dir in self.__library_directories:
            args.append(f"-L{library_dir}")

        if self.__output_dir:
            output_path: str = self.__output_dir + "/" + self.__name
            makedirs(self.__output_dir, exist_ok=True)
        else:
            output_path: str = self.__name

        args += ["-o", output_path]

        for library in self.__libraries:
            args.append(f"-l{library}")

        run(args, check=False)
