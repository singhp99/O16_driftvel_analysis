from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from event_processing import process_event
import sys

def parallelize(run_number,min_event, max_event, trace_file_path):
    results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_event, ev, trace_file_path): ev for ev in range(min_event, max_event)}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Events", file=sys.stdout):
            res = future.result()
            if res is not None:
                event_number,drift,micromg,window = res

                row_data = {"run_number":run_number,"event_number":event_number,"drift_velocity_tb":drift,"micromegas_tb":micromg,"window_tb":window}
                results.append(row_data)

    return results