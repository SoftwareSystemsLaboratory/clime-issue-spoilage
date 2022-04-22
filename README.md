# CLIME Issue Spoilage

> A tool to calculate the issue spoilage of a repository using the issues reported in its issue tracker

## Table of Contents

- [CLIME Issue Spoilage](#clime-issue-spoilage)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Arguements](#command-line-arguements)

## About

The Software Systems Laboratory (SSL) GitHub Issue Spoilage Project is a `python` tool to calculate the issue spoilage of a GitHub repository. It is reliant upon the output of the [GitHub Issue](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-github-issues) tool.

### Licensing

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## How To Use

### Installation

You can install the tool via `pip` with either of the two following one-liners:

- `pip install --upgrade pip clime-metrics`
- `pip install --upgrade pip clime-issue-spoilage`

### Command Line Arguements

`clime-issue-spoilage-graph -h`

```shell
options:
  -h, --help            show this help message and exit
  -u UPPER_WINDOW_BOUND, --upper-window-bound UPPER_WINDOW_BOUND
                        Argument to specify the max number of days to look at. NOTE: window bounds are inclusive.
  -l LOWER_WINDOW_BOUND, --lower-window-bound LOWER_WINDOW_BOUND
                        Argument to specify the start of the window of time to analyze. NOTE: window bounds are inclusive.
  -c CLOSED_ISSUES_GRAPH_FILENAME, --closed-issues-graph-filename CLOSED_ISSUES_GRAPH_FILENAME
                        The filename of the output graph of closed issues
  -i INPUT, --input INPUT
                        The input JSON file that is to be used for graphing
  -d LINE_OF_ISSUES_SPOILAGE_FILENAME, --line-of-issues-spoilage-filename LINE_OF_ISSUES_SPOILAGE_FILENAME
                        The filename of the output graph of spoiled issues
  -o OPEN_ISSUES_GRAPH_FILENAME, --open-issues-graph-filename OPEN_ISSUES_GRAPH_FILENAME
                        The filename of the output graph of open issues
  -x JOINT_GRAPH_FILENAME, --joint-graph-filename JOINT_GRAPH_FILENAME
                        The filename of the joint output graph of open and closed issues
```
