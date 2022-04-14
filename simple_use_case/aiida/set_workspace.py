import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser("replace GITHUB_WORKPACE")
    parser.add_argument("--input", required=True, help="input file")
    parser.add_argument("--output", required=True, help="output file")
    args = parser.parse_args()

    with open(args.output, "w") as outstream:
        with open(args.input, "r") as instream:
            content = instream.read()
            new = content.replace(
                "${GITHUB_WORKSPACE}",
                "${GITHUB_WORKPACE}/simple_use_case/aiida/aiida-core",
            )
            outstream.write(new)
