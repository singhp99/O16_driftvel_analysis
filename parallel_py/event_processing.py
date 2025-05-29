from spyral.trace.get_legacy_event import (
    GET_DATA_TRACE_START,
    GET_DATA_TRACE_STOP,
)

from spyral.core.legacy_beam_pads import LEGACY_BEAM_PADS
from spyral import GetParameters, PadParameters, DEFAULT_LEGACY_MAP
import h5py as h5
import numpy as np
from plotly.subplots import make_subplots
from scipy import signal
import tqdm as tqdm



def baseline_smoothing(mesh,baseline_window_scale):
    
    mesh[0] = mesh[1]
    mesh[-1] = mesh[-2]

    window = np.arange(-256.0,256.0,1.0)

    fil = np.fft.ifftshift(np.sinc(window / baseline_window_scale))
    transformed = np.fft.fft(mesh)
    result = np.real(
        np.fft.ifft(transformed * fil)
        )

    return result

def find_mesh_peaks(result):

    pks, props = signal.find_peaks(
        result,
        distance=400,
        prominence=300,
        width=(350, 400), #changed to 350 from 300
        rel_height=0.96
        )
    return pks,props

def process_event(event_number, trace_file_path):
     with h5.File(trace_file_path, "r") as trace_file:
        trace_group = trace_file['get']
        event_data = trace_group[f'evt{event_number}_data']

        mesh = np.zeros(512)
        for trace in event_data:
            if trace[4] in LEGACY_BEAM_PADS:
                mesh += trace[GET_DATA_TRACE_START:GET_DATA_TRACE_STOP]
        

        result = baseline_smoothing(mesh,baseline_window_scale=60)
        pks, props = find_mesh_peaks(result)

        if len(pks) == 0:
            return None
        drift = props["widths"][0]
        micromg = props["left_ips"][0]
        window = props["right_ips"][0]

        if micromg > 50:
            return event_number,drift,micromg,window

        else:
            return None
