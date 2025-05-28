
from spyral.phases.pointcloud_legacy_phase import get_event_range

def event_range(trace_file):
    min_event, max_event = get_event_range(trace_file)
    return min_event, max_event 
