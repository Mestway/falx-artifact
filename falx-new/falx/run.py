from falx.interface import FalxInterface
import json
from pprint import pprint
import sys

import argparse

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", dest="input_file", default=None, help="the input json file containing input data and visual sketch")
parser.add_argument("--output_file", dest="output_file", default=None, 
                    help="the output file for the synthesized visualization (as a Vega-Lite script), if none, the synthesis result will be print to commandline")


if __name__ == '__main__':

    flags = parser.parse_args()
    if flags.input_file is None:
        print("[Error] Input file not provided.")
        sys.exit(-1)
    else:
        with open(flags.input_file, "r") as f:
            input_content = json.load(f)
            input_data = input_content["input_data"]
            visual_sketch = input_content["raw_trace"]

    result = FalxInterface.synthesize(inputs=[input_data], raw_trace=visual_sketch, extra_consts=[], backend="vegalite")

    print(json.dumps(json.loads(result[0][1].to_vl_json())))
    if flags.output_file is not None:
        with open(flags.output_file, "w") as f:
            json.dump(json.loads(result[0][1].to_vl_json()), f, indent=4)
