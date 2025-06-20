from spyral.core.run_stacks import form_run_string
from pathlib import Path
import h5py as h5
import os

from event_processing import process_event
from parallel_utils import parallelize
from helper import event_range
import numpy as np
import pandas as pd

def main():
    trace_path = Path("/mnt/scratch/singhp19/O16_runs")
    all_valid_events = []
    run_num_ls = [53,54,55,56,58,59,60,61,62,63,64,65,66,67,68,70,71,72,73,74,77,78,83,84,85,86,87,88,89,90,91,92,94,96,97,98,99,100,101,102,103,104,105,106,108,109,110,111,112,113,114,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,139,140,141,142,143,144,145,146,148,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169]

    for run_number in run_num_ls:
        trace_file_path = trace_path / f"{form_run_string(run_number)}.h5"

        with h5.File(trace_file_path, "r") as trace_file:
            min_event, max_event = event_range(trace_file)
        
        print(f"Total number of events in run {run_number}: {len(range(min_event,max_event))}")

        valid_events = parallelize(run_number,min_event, max_event, trace_file_path)
        all_valid_events.extend(valid_events)
        print(f"Processed valid events: {len(valid_events)}")
        print(f"Percentage of data lost for run {run_number}: {1-(len(valid_events)/(len(range(min_event,max_event))))}")

    return all_valid_events


if __name__ == "__main__":
   valid_events = main()
   df = pd.DataFrame(valid_events)
   df.to_parquet("/mnt/home/singhp19/O16_driftvel_analysis/drift_vel_calc/all_drift_vel.parquet")
   print("Done! All drift velocities determined!")