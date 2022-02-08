import pathlib


def task_website():
    deps = ["index.rst", "conf.py"]
    docs = pathlib.Path("docs")
    for f in docs.glob("*.rst"):
        deps.append(str(f))
    return {
        "file_dep": deps,
        "actions": ["sphinx-build . website"],
        "verbosity": 2,
    }
