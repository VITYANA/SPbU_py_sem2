import argparse
import copy
import random
import time
from typing import Any

import matplotlib
import numpy as np
import Sort
from matplotlib.pyplot import legend, plot, savefig, show, title, xlabel, ylabel

matplotlib.use("TkAgg")


def parse_cmd() -> dict[str, Any]:
    parser = argparse.ArgumentParser(prog="Comparing merge sort")
    parser.add_argument("list_size", type=int)
    parser.add_argument("thread_count", type=int, nargs="+")
    parser.add_argument("output_file", type=str)
    parser.add_argument("--multiprocess", type=bool)
    args = parser.parse_args()

    return vars(args)


def check_time(size: int, threads: list[int], num_of_tests: int, multiprocess: bool) -> list:
    output_time = []
    array = random.sample(range(-1000000, 1000000), size)
    for thread_cnt in threads:
        total_time = 0.0
        for j in range(num_of_tests):
            arr_copy = copy.copy(array)
            start = time.perf_counter()
            Sort.merge_sort(arr_copy, thread_cnt, multiprocess)
            total_time += time.perf_counter() - start
        output_time.append(total_time / num_of_tests)
    return output_time


if __name__ == "__main__":
    input_data = parse_cmd()
    x_axis = np.array(input_data["thread_count"])
    y_axis_threading = check_time(input_data["list_size"], input_data["thread_count"], 3, input_data["multiprocess"])
    y_axis_recursive = check_time(
        input_data["list_size"], [0] * len(input_data["thread_count"]), 3, input_data["multiprocess"]
    )
    plot(x_axis, y_axis_threading, color="g", label="thread")
    plot(x_axis, y_axis_recursive, color="b", label="recursive")
    title(
        label=f"size: {input_data['list_size']}, threads: {input_data['thread_count']}, multiprocess: {input_data['multiprocess']}"
    )
    ylabel("time, sec")
    xlabel("threads, count")
    legend()
    savefig(input_data["output_file"])
    show()
