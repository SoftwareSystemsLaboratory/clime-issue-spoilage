from argparse import ArgumentParser, Namespace

name: str = "CLIME"
authors: list = [
    "Nicholas M. Synovic",
    "Rohan Sethi",
    "Jacob Palmer",
    "George K. Thiruvathukal",
]


def mainArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Issue Spoilage Calculator",
        description="A tool to calculate the issue spoilage of a repository",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=open,
        help="Issues JSON file. DEFAULT: ./github_issues.json",
        default="github_issues.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output JSON file. DEFAULT: ./issue_spoilage.json",
        type=str,
        default="issue_spoilage.json",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display version of the tool",
        action="store_true",
        default=False,
    )

    return parser.parse_args()


def graphArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Issue Spoilage Grapher",
        description="A tool to graph the issue spoilage of a repository",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        help=f"JSON export from {name} GitHub Bus Factor Compute. DEFAULT: ./issue_spoilage.json",
        type=str,
        required=False,
        default="issue_spoilage.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Filename of the graph. DEFAULT: ./issue_spoilage.pdf",
        type=str,
        required=False,
        default="issue_spoilage.pdf",
    )
    parser.add_argument(
        "--type",
        help="Type of figure to plot. DEFAULT: line",
        type=str,
        required=False,
        default="line",
    )
    parser.add_argument(
        "--title",
        help='Title of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--x-label",
        help='X axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--y-label",
        help='Y axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--stylesheet",
        help='Filepath of matplotlib stylesheet to use. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display version of the tool",
        action="store_true",
        default=False,
    )

    return parser.parse_args()
