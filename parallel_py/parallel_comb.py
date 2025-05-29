from spyral.core.run_stacks import form_run_string
from pathlib import Path
import h5py as h5

from event_processing import process_event
from parallel_utils import parallelize
from helper import event_range
import numpy as np
import pandas as pd

def main():
    trace_path = Path("/mnt/scratch/singhp19/O16_runs")
    all_valid_events = []
    run_num_ls = [104,105,106,108,109,110,111,112,113,114,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,169]
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