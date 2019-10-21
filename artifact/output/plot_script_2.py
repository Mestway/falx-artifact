import argparse
import json
import os
import pandas as pd
from pprint import pprint
import numpy as np
from vega import VegaLite
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

def plot_solving_time(log_dir_list):
    titiles = log_dir_list
    all_result = read_log_result_list(log_dir_list, titiles)
    
    plot_data = []
    for i in np.linspace(0.01, MAX_TIME, 1000):
        cnt = {}
        for r in all_result:
            if r["exp_id"] not in cnt:
                cnt[r["exp_id"]] = 0
            if r["solved"] and r["time"] > 0 and r["time"] < i:
                cnt[r["exp_id"]] += 1
        for exp_id in cnt:
            plot_data.append({"time": i, "cnt": cnt[exp_id], "exp_id": exp_id })
    
    
    cdf_data = pd.DataFrame.from_dict(plot_data)
    chart2 = {
        "$schema": "https://vega.github.io/schema/vega-lite/v3.json",
        "mark": {"type": "line"},
        "encoding": {
            "y": {"field": "cnt", "type": "quantitative", "title": "# of solved benchmarks", "scale": {"domain": [0,83]}},
            "x": { "field": "time", "type": "quantitative", "title": "Time (s)"},# "scale": {"type": "log", "base": 10}},
            "color": {"field": "exp_id", "type": "nominal"},
            "order": {"field": "time"}
        }
    }
    chart2["data"] = { "values": plot_data }
    print(json.dumps(chart2))

if __name__ == '__main__':
    # python plot_script_2.py exp_falx_4 exp_morpheus_4 
    num_arguments = len(sys.argv) - 1
    plot_solving_time(sys.argv[1:])