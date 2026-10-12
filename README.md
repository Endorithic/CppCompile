# CppCompile
A VERY SIMPLE AND STUPID way to make C++ compilation scripts using Python.

## What is this for?
So, as a simple check of my GitHub profile can show you, I don't like the process
of building C++ projects lol. I am working on a [project](https://github.com/Endorithic/Ignitec-rs) 
that does it better, but until that project reaches a usable state, I need something else. That's where
THIS project comes in.

## What can CppCompile do?
Basically nothing. It's extremely simple, and extremely stupid. It's really meant
for my personal setup where I have a few files, and that's about it. It does not
do incremental compilation, or even parallel compilation for that matter.
It's really only meant to be a programmatic approach to the standard `compile.sh`
approach, but with Python instead of shell scripting. Cause why not?

## Current features
The features currently supported are:
- Specifying the optimization level (`-O0`, `-O3`, etc.)
- Specifying the target output directory using `set_output_dir()`
- Adding include directories using `add_include_dir()`
- Adding individual source files using `add_source_file()`
- Adding MULTIPLE source files using `add_source_dir()`
- Adding any flag you want using `add_flag()`
- Specifying the compiler, either using `project.compiler = ...` or passing it to the constructor
- Library support, either with system-wide libraries using `add_library()`, or custom paths using `add_library_dir()`

## Installation
If you, for some reason, wanna install this, you're gonna have to do it manually cause ain't no way
I am putting this on pip or something. I personally just have it in `~/.local/lib/python` and put
that path on Python's module search path, but you do it however you want lol.

## Example
This is a short, simple example of what a build file for a tiny C++ project would look like.
This specific example is made for my other repository, [lagrange-simulation](https://github.com/Endorithic/lagrange-simulation).

```py
#! /usr/bin/env python3

from cppcompile import Executable, flag

project: Executable = Executable("lagrange-sim", compiler="clang++")

project.add_include_dir("include")
project.add_source_dir(
    "src",
    ["main.cpp", "lagrange.cpp", "managed_window.cpp", "objects.cpp", "utilities.cpp"],
)

project.add_library("raylib")

project.add_flag("-std=c++26")
project.add_flag("-Wpedantic")
project.add_flag("-Wall")
project.add_flag("-Werror")

project.set_output_dir("target")

is_release: bool = flag("--release")
if is_release:
    project.add_flag("-DNDEBUG")
    project.add_flag("-march=native")
    project.opt_level = 3
else:
    project.opt_level = 0

project.build()
```
