# CLIME Issue Spoilage

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6454355.svg)](https://doi.org/10.5281/zenodo.6454355)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/clime-issue-spoilage/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/clime-issue-spoilage/actions/workflows/release.yml)

> A tool to calculate the issue spoilage of a repository using the issues reported in its issue tracker

## Table of Contents

- [CLIME Issue Spoilage](#clime-issue-spoilage)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Options](#command-line-options)

## About

The Software Systems Laboratory (SSL) GitHub Issue Spoilage Project is a `python` tool to calculate the issue spoilage of a GitHub repository. It is reliant upon the output of the [GitHub Issue](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues) tool.

### Licensing

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## How To Use

### Installation

You can install the tool via `pip` with either of the two following one-liners:

- `pip install --upgrade pip clime-metrics`
- `pip install --upgrade pip clime-issue-spoilage`

### Command Line Options

`clime-issue-spoilage-compute -h`

``` shell
usage: CLIME Issue Spoilage Calculator [-h] [-i INPUT] [-o OUTPUT] [-v]

A tool to calculate the issue spoilage of a repository

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Issues JSON file. DEFAULT: ./github_issues.json
  -o OUTPUT, --output OUTPUT
                        Output JSON file. DEFAULT: ./issue_spoilage.json
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Rohan Sethi, Jacob Palmer, George K.
Thiruvathukal
```

`clime-issue-spoilage-graph -h`

``` shell
usage: CLIME Issue Spoilage Grapher [-h] [-i INPUT] [-o OUTPUT] [--type TYPE]
                                    [--title TITLE] [--x-label X_LABEL]
                                    [--y-label Y_LABEL]
                                    [--stylesheet STYLESHEET] [-v]

A tool to graph the issue spoilage of a repository

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        JSON export from CLIME GitHub Bus Factor Compute.
                        DEFAULT: ./issue_spoilage.json
  -o OUTPUT, --output OUTPUT
                        Filename of the graph. DEFAULT: ./issue_spoilage.pdf
  --type TYPE           Type of figure to plot. DEFAULT: line
  --title TITLE         Title of the figure. DEFAULT: ""
  --x-label X_LABEL     X axis label of the figure. DEFAULT: ""
  --y-label Y_LABEL     Y axis label of the figure. DEFAULT: ""
  --stylesheet STYLESHEET
                        Filepath of matplotlib stylesheet to use. DEFAULT: ""
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, Rohan Sethi, Jacob Palmer, George K.
Thiruvathukal

```
