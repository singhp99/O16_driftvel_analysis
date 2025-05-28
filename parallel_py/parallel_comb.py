from spyral.core.run_stacks import form_run_string
from pathlib import Path
import h5py as h5

from event_processing import process_event
from parallel_utils import parallelize
from helper import event_range
import numpy as np
import pandas as pd

def main():
    trace_path = Path("/Volumes/researchEXT/O16/O16_runs")
    results = []
    run_num_ls = [169,105]
    for run_number in run_num_ls:
        trace_file_path = trace_path / f"{form_run_string(run_number)}.h5"

        with h5.File(trace_file_path, "r") as trace_file:
            min_event, max_event = event_range(trace_file)
        
        print(f"Total number of events in run {run_number}: {len(range(min_event,max_event))}")

        valid_events = parallelize(results,run_number,min_event, max_event, trace_file_path)

        print(f"Processed valid events: {len(valid_events)}")
        print(f"Percentage of data lost for run {run_number}: {1-(len(valid_events)/(len(range(min_event,max_event))))}")

    return valid_events


if __name__ == "__main__":
   valid_events = main()
   print(valid_events)
   df = pd.DataFrame(valid_events)
   
   df.to_parquet("/Users/mahesh/Desktop/academics/research/e20009_analysis/notebooks/parallelization/16O_driftvelocities_h5/all_drift_vel.parquet")
