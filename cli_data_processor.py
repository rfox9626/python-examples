import argparse
import time
import json
import functools

class CodeTimer:
    def __init__(self, tag=None):
        self.tag = tag
        self.start_time = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        time_diff = time.perf_counter() - self.start_time
        if self.tag == None:
            label = "Execution Time"
        else:
            label = self.tag

        print(f"[{label}]: {time_diff:.6f}")


def read_log_file(file):
    with open(file, "r") as f:
        for line in f:
            yield line


def filter_cri_maj(lines):
    for line in lines:
        if "CRITICAL" in line or "MAJOR" in line:
            yield line

def audit_log(func):
    @functools.wraps(func)

    def wrapper(*args, **kwargs):
        print(f"[AUDIT] Calling function '{func.__name__}' with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"[AUDIT] Function '{func.__name__}' returned: {result}")
        return result

    return wrapper


@audit_log
def parse_single_line(line):
    q = line.split("]")
    timestamp = q[0].strip().replace("[", "")
    level = q[1].strip().replace("[", "")
    section = q[2].strip().replace("[", "")
    msg = q[3].strip()

    return {
        "timestamp": timestamp,
        "level": level,
        "section": section,
        "message": msg
    }


def parse_lines(lines):
    for line in lines:
        yield parse_single_line(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to process user data.")
    parser.add_argument("--input", type=str, help="Path of the input file")
    parser.add_argument("--output", type=str, help="Path of the output file")
    args = parser.parse_args()

    print(f"Processing: {args.output}")

    raw_lines = read_log_file(args.input)
    filtered_lines = filter_cri_maj(raw_lines)
    parsed_logs = parse_lines(filtered_lines)

    with CodeTimer("File I/O"):
        with open(args.output, "w") as f:
            for log in parsed_logs:
                f.write(json.dumps(log) + "\n")
