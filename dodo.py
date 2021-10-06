import pathlib


def task_website():
    deps = ["index.rst", "conf.py"]
    docs = pathlib.Path("docs")
    sources = list(docs.glob("*.rst"))
    return {
            "file_dep": deps + sources,
            "actions": ["sphinx-build . website"],
            "verbosity": 2,
            }
