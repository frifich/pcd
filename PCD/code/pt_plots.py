import numpy as np
from scipy.signal import butter, lfilter

#the ecg sequence must be numpy ndarray of (numbersamples,)
def run(ecg_sequence):
    try:
        ecg_sequence = ecg_sequence.astype(int)
    except:
        print("failed to convert the ecg into integer")
        return False
    signal_frequency = 360
    refractory_period = 120
    integration_window = 15
    spacing = 50
    indices, values = detect_peaks(ecg_sequence, signal_frequency, integration_window, spacing)
    qrs_peaks_indices = detect_qrs(indices, values, refractory_period)

def bandpass_filter(data, lowcut, highcut, signal_freq, filter_order):
    nyquist_freq = 0.5 * signal_freq
    low = lowcut / nyquist_freq
    high = highcut / nyquist_freq
    b, a = butter(filter_order, [low, high], btype="band")
    y = lfilter(b, a, data)
    return y

def findpeaks(data, spacing=1, limit=None):
    len = data.size
    x = np.zeros(len + 2 * spacing)
    x[:spacing] = data[0] - 1.e-6
    x[-spacing:] = data[-1] - 1.e-6
    x[spacing:spacing + len] = data
    peak_candidate = np.zeros(len)
    peak_candidate[:] = True
    for s in range(spacing):
        start = spacing - s - 1
        h_b = x[start: start + len]
        start = spacing
        h_c = x[start: start + len]
        start = spacing + s + 1
        h_a = x[start: start + len]
        peak_candidate = np.logical_and(peak_candidate, np.logical_and(h_c > h_b, h_c > h_a))

    ind = np.argwhere(peak_candidate)
    ind = ind.reshape(ind.size)
    if limit is not None:
        ind = ind[data[ind] > limit]
    return ind

def detect_peaks(ecg_sequence, signal_frequency, integration_window, spacing):
    filtered_ecg_sequence = bandpass_filter(ecg_sequence, lowcut= 0.0,
                                                          highcut= 15.0, signal_freq=signal_frequency,
                                                          filter_order=1)
    filtered_ecg_sequence[:5] = filtered_ecg_sequence[5]
    differentiated_ecg_sequence = np.ediff1d(filtered_ecg_sequence)
    squared_ecg_sequence = differentiated_ecg_sequence ** 2
    integrated_ecg_sequence = np.convolve(squared_ecg_sequence, np.ones(integration_window))
    detected_peaks_indices = findpeaks(data=integrated_ecg_sequence,
                                                 limit=0.35,
                                                 spacing=spacing)
    detected_peaks_values = integrated_ecg_sequence[detected_peaks_indices]
    

    return detected_peaks_indices, detected_peaks_values

def detect_qrs(indices, values, refractory_period):

    qrs_peak_value = 0.0
    noise_peak_value = 0.0
    threshold_value = 4000.0

    qrs_peak_filtering_factor = 0.125
    noise_peak_filtering_factor = 0.125
    qrs_noise_diff_weight = 0.25

    qrs_peaks_indices = np.array([], dtype='int')

    for detected_peak_index, detected_peaks_value in zip(indices, values):

        #for the first iteration
        try:
            last_qrs_index = qrs_peaks_indices[-1]
        except IndexError:
            last_qrs_index = 0

        # after 200 ms refractory period
        if detected_peak_index - last_qrs_index > refractory_period or not qrs_peaks_indices.size:
            # every peak is qrs if it surpasses the threshold value else it is noise.
            if detected_peaks_value > threshold_value:
                qrs_peaks_indices = np.append(qrs_peaks_indices, detected_peak_index)
                qrs_peak_value = qrs_peak_filtering_factor * detected_peaks_value + \
                                      (1 - qrs_peak_filtering_factor) * qrs_peak_value
            else:
                noise_peak_value = noise_peak_filtering_factor * detected_peaks_value + \
                                        (1 - noise_peak_filtering_factor) * noise_peak_value

            #update threshold
            threshold_value = noise_peak_value + \
                                   qrs_noise_diff_weight * (qrs_peak_value - noise_peak_value)
    return qrs_peaks_indices
