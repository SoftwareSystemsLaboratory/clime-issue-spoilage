from argparse import Namespace
from datetime import datetime

import pandas
from dateutil.parser import parse as dateParse
from intervaltree import IntervalTree
from pandas import DataFrame

from clime_issue_spoilage.args import mainArgs
from clime_issue_spoilage.version import version


def getIssueTimelineIntervals(day0: datetime, issues: DataFrame) -> list:
    intervals = []

    foo: str | datetime
    bar: str | datetime
    for foo, bar in zip(issues["created_at"], issues["closed_at"]):
        startDate: datetime = dateParse(str(foo)).replace(tzinfo=None)
        endDate: datetime = dateParse(str(bar)).replace(tzinfo=None)

        startDaySince0: int = (startDate - day0).days
        endDaySince0: int = (endDate - day0).days

        intervals.append((startDaySince0, endDaySince0))

    return intervals


def buildIntervalTree(intervals: list) -> IntervalTree:
    tree: IntervalTree = IntervalTree()

    interval: tuple
    for interval in intervals:
        tree.addi(interval[0], interval[1] + 1, 1)

    return tree


def getDailyIssueSpoilage(intervals: IntervalTree, timeline: list) -> list:
    return [len(intervals[day]) for day in timeline]


def main() -> None:
    args: Namespace = mainArgs()

    if args.version:
        print(f"clime-issue-spoilage-compute version {version()}")
        quit(0)

    issues: DataFrame = pandas.read_json(args.input).T

    day0: datetime = dateParse(issues["created_at"][0]).replace(tzinfo=None)
    dayN: datetime = datetime.now().replace(tzinfo=None)
    timeline: list = [day for day in range((dayN - day0).days)]

    issues["created_at"] = issues["created_at"].fillna(day0)
    issues["closed_at"] = issues["closed_at"].fillna(dayN)

    intervals: list = getIssueTimelineIntervals(day0, issues)
    intervalTree: IntervalTree = buildIntervalTree(intervals)

    dailyIssuesSpoilage: list = getDailyIssueSpoilage(intervalTree, timeline)

    data: dict = {
        "days_since_0": timeline,
        "issue_spoilage": dailyIssuesSpoilage,
    }

    DataFrame(data).to_json(args.output)


if __name__ == "__main__":
    main()
