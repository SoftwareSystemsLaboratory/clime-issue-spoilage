from setuptools import setup

from clime_issue_spoilage import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clime-issue-spoilage",
    packages=["clime_issue_spoilage"],
    version=version.version(),
    description="CLIME - Issue Spoilage",
    author="Software and Systems Laboratory - Loyola University Chicago",
    author_email="ssl-metrics@ssl.luc.edu",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    project_urls={
        "Bug Tracker": "https://github.com/SoftwareSystemsLaboratory/clime-issue-spoilage/issues",
        "GitHub Repository": "https://github.com/SoftwareSystemsLaboratory/clime-issue-spoilage",
    },
    keywords=[
        "bugzilla",
        "bus factor",
        "bus factor",
        "cloc",
        "commits",
        "commits",
        "delta lines of code",
        "engineering",
        "git",
        "git",
        "github",
        "github",
        "gitlab",
        "installable",
        "issue density",
        "issue density",
        "issue spoilage",
        "issues",
        "issues",
        "kloc",
        "lines of code",
        "longitudinal graphs",
        "loyola university chicago",
        "loyola",
        "luc",
        "metrics",
        "metrics",
        "mining",
        "productivity",
        "python",
        "repository mining",
        "repository",
        "simple",
        "sloccount",
        "software engineering",
        "software metrics",
        "software systems laboratory",
        "software",
        "ssl",
        "thousands of lines of code",
        "tool",
        "vcs"
    ],
    python_requires=">=3.9",
    install_requires=[
        "intervaltree",
        "numpy",
        "matplotlib",
        "pandas",
        "progress",
        "python-dateutil",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "clime-issue-spoilage-compute = clime_issue_spoilage.main:main",
            "clime-issue-spoilage-graph = clime_issue_spoilage.graph:main",
        ]
    },
)
