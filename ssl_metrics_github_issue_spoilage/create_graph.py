import json
from argparse import ArgumentParser, Namespace
from datetime import datetime
from os.path import exists
from typing import Any

import matplotlib.pyplot as plt
from dateutil.parser import parse
from intervaltree import IntervalTree
from matplotlib.figure import Figure
from progress.spinner import MoonSpinner
import math

# imports are above
# arguments are below

def getArgparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Graph GitHub Issues",
        usage="This program outputs a series of graphs based on GitHub issue data.",
    )
    parser.add_argument(
        "-u",
        "--upper-window-bound",
        help="Argument to specify the max number of days to look at. NOTE: window bounds are inclusive.",
        type=int,
        required=False,
        default=None,
    )
    parser.add_argument(
        "-l",
        "--lower-window-bound",
        help="Argument to specify the start of the window of time to analyze. NOTE: window bounds are inclusive.",
        type=int,
        required=False,
        default=None,
    )
    parser.add_argument(
        "-c",
        "--closed-issues-graph-filename",
        help="The filename of the output graph of closed issues",
        type=str,
        required=False,
        default="closed.pdf",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input JSON file that is to be used for graphing",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--line-of-issues-spoilage-filename",
        help="The filename of the output graph of spoiled issues",
        type=str,
        required=False,
        default="spoilage.pdf",
    )
    parser.add_argument(
        "-o",
        "--open-issues-graph-filename",
        help="The filename of the output graph of open issues",
        type=str,
        required=False,
        default="open.pdf",
    )
    parser.add_argument(
        "-x",
        "--joint-graph-filename",
        help="The filename of the joint output graph of open and closed issues",
        type=str,
        required=False,
        default="joint.pdf",
    )
    parser.add_argument(
        "-s",
        "--stepper",
        help="The frequency of days with which you want to see the number of issues for",
        type=int,
        required=False,
        default=None,
    )
    parser.add_argument(
        "-e",
        "--export",
        help="The filename of the json file with issue spoilage data against time",
        type=str,
        required=False,
        default=None,
    )


    return parser.parse_args()

#function below makes the data a more readable format for the functions following it

def issue_processor(filename: str) -> list:

    issues: list = None

    try:
        with open(file=filename, mode="r") as file:
            issues: list = json.load(file)
            file.close()
    except FileNotFoundError:
        print(f"{filename} does not exist.")
        quit(4)

    day0: datetime = parse(issues["created_at"]["0"]).replace(tzinfo=None)
    dayN: datetime = datetime.today().replace(tzinfo=None)
    data: list = []

    issue: dict
    for i in range(len(list((issues["number"].keys())))):
        value: dict = {
            "issue_number": None,
            "created_at": None,
            "created_at_day": None,
            "closed_at": None,
            "closed_at_day": None,
            "state": None,
        }

        value["issue_number"] = issues["number"][str(i)]
        value["created_at"] = issues["created_at"][str(i)]
        value["state"] = issues["state"][str(i)]

        if issues["closed_at"][str(i)] is None:
            value["closed_at"] = dayN.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            value["closed_at"] = issues["closed_at"][str(i)]

        createdAtDay: datetime = parse(issues["created_at"][str(i)]).replace(
            tzinfo=None
        )

        value["created_at_day"] = (createdAtDay - day0).days

        if value["state"] == "open":
            value["closed_at_day"] = (dayN - day0).days
        else:
            value["closed_at_day"] = (
                parse(issues["closed_at"][str(i)]).replace(tzinfo=None) - day0
            ).days

        data.append(value)

    return data


# converting the data into an interval tree

def createIntervalTree(data: list, filename: str) -> IntervalTree:
    tree: IntervalTree = IntervalTree()
    # day0: datetime = parse(data[0]["created_at"]).replace(tzinfo=None)
    args: Namespace = getArgparse()
    factor: int
    if args.stepper == None or args.stepper <= 0:
        factor = 1
    else:
        factor = args.stepper
    with MoonSpinner(f"Creating interval tree from {filename}... ") as pb:
        for i in range(int(len(data)/factor)):
            begin: int = data[i*factor]["created_at_day"]
            end: int = data[i*factor]["closed_at_day"]

            try:
                data[i*factor]["endDayOffset"] = 0
                tree.addi(begin=begin, end=end, data=data[i*factor])
            except ValueError:
                data[i*factor]["endDayOffset"] = 1
                tree.addi(begin=begin, end=end + 1, data=data[i*factor])

            pb.next()

    return tree


# converting an interval tree into a dictionary of overlapping spoiled issues

def issue_spoilage_data(
    data: IntervalTree,
):
    args: Namespace = getArgparse()
    factor: int
    if args.stepper == None or args.stepper <= 0:
        factor = 1
    else:
        factor = args.stepper
    # startDay: int = data.begin()
    endDay: int = data.end()
    dict_of_spoilage_values = dict()
    for i in range(int(endDay/factor)+1):
        if i*factor == 1*factor:
            temp_set = data.overlap(0, 1*factor)
            proc_overlap = []
            for issue in temp_set:
                # if issue.data["state"] == "open":
                #     proc_overlap.append(issue)
                if issue.begin != issue.end - 1*factor and issue.data["endDayOffset"] != 1:
                    proc_overlap.append(issue)
                    # list_of_intervals.append(issue.end - startDay)
            dict_of_spoilage_values[i*factor] = len(proc_overlap)
        elif i*factor == 0:
            pass
        else:
            temp_set = data.overlap(
                i*factor-1*factor, i*factor
            )  # can change the step size by making the -1 a variable and chaning the top if statement overlap to 0, step size
            proc_overlap = []
            for issue in temp_set:
                # if issue.data["state"] == "open":
                #     proc_overlap.append(issue)
                if issue.begin != issue.end - 1*factor and issue.data["endDayOffset"] != 1:
                    proc_overlap.append(issue)
                    # list_of_intervals.append(issue.end - startDay)
            dict_of_spoilage_values[i*factor] = len(proc_overlap)
    return dict_of_spoilage_values

# extra graph functionality functions

def shrink_graph(keys=None):
    args: Namespace = getArgparse()
    if args.upper_window_bound != None:
        if args.lower_window_bound != None:
            plt.xlim(args.lower_window_bound, args.upper_window_bound)
        else:
            plt.xlim(0, args.upper_window_bound)
    else:
        if args.lower_window_bound != None:
            plt.xlim(args.lower_window_bound, len(keys))

def stepper(data: dict = None):
    args: Namespace = getArgparse()
    newData: dict = dict()
    if args.stepper == None:
        return data
    elif args.stepper <= 0:
        return data
    else:
        for i in range(int(len(data)/args.stepper) + 1):
            newData[i*args.stepper] = data[i*args.stepper]
        return newData

# graphs

def plot_IssueSpoilagePerDay(
    pregeneratedData: dict,
    filename: str = None,
):
    figure: Figure = plt.figure()

    plt.title("Number of Spoiled Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    data: dict = pregeneratedData
    keys = data.keys()
    values = data.values()

    plt.plot(keys, values)

    shrink_graph(keys=keys)

    figure.savefig(filename)

    return exists(filename)


def plot_OpenIssuesPerDay_Line(
    pregeneratedData: dict = None,
    filename: str = None,
):
    figure: Figure = plt.figure()

    plt.title("Number of Open Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    data: dict = pregeneratedData
    plt.plot(data.keys(), data.values())
    shrink_graph(keys=data.keys())
    figure.savefig(filename)

    return exists(filename)


def plot_ClosedIssuesPerDay_Line(
    pregeneratedData: dict = None,
    filename: str = None,
):
    figure: Figure = plt.figure()

    plt.title("Number of Closed Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    data: dict = pregeneratedData
    x_values = [int(i) for i in data.keys()]
    y_values = [int(i) for i in data.values()]
    # z = derivative(x_values, y_values)
    # p = np.poly1d(z)
    plt.plot(data.keys(), data.values(), color="blue", label="discrete")
    # plt.plot(x_values, p(x_values), color="red", label="continuous")

    shrink_graph(keys=data.keys())
    # plt.legend()
    figure.savefig(filename)

    return exists(filename)


def plot_OpenClosedSpoiledIssuesPerDay_Line(
    pregeneratedData_OpenIssues: dict = None,
    pregeneratedData_ClosedIssues: dict = None,
    pregeneratedData_SpoiledIssues: list = None,
    filename: str = None,
    ):

    figure: Figure = plt.figure()

    plt.title("Number of Issues Per Day")
    plt.ylabel("Number of Issues")
    plt.xlabel("Day")

    openData: dict = pregeneratedData_OpenIssues
    closedData: dict = pregeneratedData_ClosedIssues
    spoiledData: dict = pregeneratedData_SpoiledIssues

    keys = spoiledData.keys()
    values = spoiledData.values()

    plt.plot(openData.keys(), openData.values(), color="blue", label="Open Issues")
    plt.plot(closedData.keys(), closedData.values(), color="red", label="Closed Issues")
    plt.plot(keys, values, color="green", label="Spoiled Issues")
    plt.legend()
    shrink_graph(keys=openData.keys())
    shrink_graph(keys=closedData.keys())
    shrink_graph(keys=keys)
    figure.savefig(filename)

    return exists(filename)

# exports a json file only for issue spoilage data

def return_json(dictionary: dict):
    the_file = None
    args: Namespace = getArgparse()
    if args.export != None:
        with open(args.export, 'w') as new_file:
            the_file = json.dump(dictionary, new_file)
        return the_file
    else:
        pass

# creates a dictionary of the values

def fillDictBasedOnKeyValue(
    dictionary: dict, tree: IntervalTree, key: str, value: Any
) -> dict:
    data: dict = {}
    keys = dictionary.keys()

    maxKeyValue: int = max(keys)
    minKeyValue: int = min(keys)

    with MoonSpinner(
        f'Getting the total number of "{key} = {value}" issues per day... '
    ) as pb:
        for x in range(minKeyValue, maxKeyValue):
            try:
                data[x] = dictionary[x]
            except KeyError:
                count = 0
                interval: IntervalTree
                for interval in tree.at(x):
                    if interval.data[key] == value:
                        count += 1
                data[x] = count

            pb.next()

    return data

# runs entire file depending on user input and preferences

def main() -> None:
    args: Namespace = getArgparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    jsonData: list = issue_processor(filename=args.input)

    tree: IntervalTree = createIntervalTree(data=jsonData, filename=args.input)

    startDay: int = tree.begin()
    endDay: int = tree.end()

    if len(tree.at(endDay)) == 0:
        endDay -= 1

    baseDict: dict = {startDay: len(tree.at(startDay)), endDay: len(tree.at(endDay))}

    openIssues: dict = fillDictBasedOnKeyValue(
        dictionary=baseDict, tree=tree, key="state", value="open"
    )

    closedIssues: dict = fillDictBasedOnKeyValue(
        dictionary=baseDict, tree=tree, key="state", value="closed"
    )

    new_list: dict = issue_spoilage_data(
        data=tree,
    )

    return_json(
            new_list
    )


    plot_OpenIssuesPerDay_Line(
        pregeneratedData=openIssues, filename=args.open_issues_graph_filename
    )

    plot_ClosedIssuesPerDay_Line(
        pregeneratedData=closedIssues, filename=args.closed_issues_graph_filename
    )

    plot_OpenClosedSpoiledIssuesPerDay_Line(
        pregeneratedData_ClosedIssues=closedIssues,
        pregeneratedData_OpenIssues=openIssues,
        pregeneratedData_SpoiledIssues=new_list,
        filename=args.joint_graph_filename,
    )

    plot_IssueSpoilagePerDay(
        pregeneratedData=new_list,
        filename=args.line_of_issues_spoilage_filename,
    )


if __name__ == "__main__":
    main()
