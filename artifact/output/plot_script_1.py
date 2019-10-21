import argparse
import json
import os
import pandas as pd
from pprint import pprint
import numpy as np
import sys

# default directories
OUTPUT_DIR = os.path.join(".")
MAX_TIME = 600

def parse_log_content(exp_id, data_id, lines):
    """parse a log file"""
    status = {
        "exp_id": exp_id,
        "data_id": data_id,
        "num_candidates": [],
        "table_prog": None,
        "vis_spec": None,
        "time": MAX_TIME
    }
    for i, l in enumerate(lines):
        if l.startswith("# candidates before getting the correct solution: "):
            status["num_candidates"].append(int(l.split(":")[-1].strip()) + 1)
        if l.startswith("# time used (s): "):
            status["time"] = float(l.split(":")[-1].strip())
        if l.startswith("# table_prog:") and len(lines) > i + 1:
            #status["table_prog"] = lines[i + 1]
            pass
        if l.startswith("# vis_spec:") and len(lines) > i + 1:
            #status["vis_spec"] = lines[i + 1]
            pass
    status["solved"] = False if status["time"] >= MAX_TIME else True
    status["num_explored"] = sum(status["num_candidates"])
    status.pop("num_candidates")
    return status

def read_log_result_list(log_dir_list, titles=None):
    all_result = []
    for i, log_dir in enumerate(log_dir_list):
        for fname in os.listdir(log_dir):
            if not fname.endswith(".log"): continue
            fpath = os.path.join(log_dir, fname)
            title = log_dir if titles is None else titles[i]
            with open(fpath) as f:
                status = parse_log_content(title, fname.split(".")[0], f.readlines())
                all_result.append(status)
    all_result.sort(key=lambda x:x["time"])
    return all_result
    
def plot_num_candidates(log_dir_list):
    titles = log_dir_list
    all_result = read_log_result_list(log_dir_list, titles)
    df = pd.DataFrame.from_dict(all_result)
    df = df[df["solved"] == True]
    
    for t in titles:
        cases_solved_within_top_5 = []
        print("# {}".format(t))
        dft = df[df["exp_id"]==t]
        #print("# cases solved within top 5:")
        #print(list(dft[dft["num_explored"] <= 5]["data_id"]))
        print("  # cases solved solved within top 1: {}".format(len(dft[dft["num_explored"] <= 1])))
        print("  # cases solved solved within top 3: {}".format(len(dft[dft["num_explored"] <= 3])))
        print("  # cases solved solved within top 5: {}".format(len(dft[dft["num_explored"] <= 5])))
        print("  # cases solved within time limit:   {}".format(len(dft)))

if __name__ == '__main__':

    # python plot_script_1.py exp_falx_4 exp_falx_6 exp_falx_8 

    num_arguments = len(sys.argv) - 1
    args = sys.argv[1:]

    plot_num_candidates(args)