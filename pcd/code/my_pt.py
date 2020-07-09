import numpy as np 
import ftools
import matplotlib.pyplot as plt

# configuration variables
ECG_DATA_PATH = "./data"
SIG_FREQ = 360

def QRS_detector_offline(data_path, number_samples=0):
    raw_ecg = load_ecg(data_path, number_samples)
    integrated_ecg, peaks = detect_peaks(raw_ecg, False)
    qrs = detect_qrs(raw_ecg, peaks)
    return raw_ecg, integrated_ecg, qrs

def load_ecg(data_path, number_samples=0):
    """
    Load the ECG signal from the raw data present at ./data/${signal_name}
    """
    raw_ecg = np.loadtxt(data_path, skiprows=1, delimiter=',', dtype='int')
    raw_ecg = raw_ecg[:,1]
    if number_samples != 0:
        raw_ecg = raw_ecg[:number_samples]
    raw_ecg = np.array(raw_ecg)
    
    return raw_ecg
    
def detect_peaks(raw_ecg, plotting=False):
    """
    Extract the peaks of the csv signal
    """
    
    FITLER_LOWCUT = 0.0
    FILTER_HIGHCUT = 15.0
    FILTER_ORDER = 1
    INTEGRATION_WINDOW = 15

    FP_LIMIT = 0.35
    FP_SPACING = 50


    filtered_ecg = None
    differentiated_ecg = None
    squared_ecg = None
    integrated_ecg = None
    detected_peaks_indices = None
    detected_peaks_values = None

    #Step one: filter the ECG
    filtered_ecg = ftools.bandpass_filter(raw_ecg, FITLER_LOWCUT, 
                                        FILTER_HIGHCUT, SIG_FREQ, FILTER_ORDER)
    filtered_ecg[:5] = filtered_ecg[5]
    if plotting:
        plt.plot(filtered_ecg)
        plt.show()

    #Step two: differentiate 
    differentiated_ecg = np.ediff1d(filtered_ecg) 
    if plotting:
        plt.plot(differentiated_ecg)
        plt.show()
        
    #Step three: square the ecg
    squared_ecg = differentiated_ecg ** 2
    if plotting:
        plt.plot(squared_ecg)
        plt.show()
    
    #Step four: integrate the ecg
    integrated_ecg = np.convolve(squared_ecg, np.ones(INTEGRATION_WINDOW))
    if plotting:
        plt.plot(integrated_ecg)
        plt.show()
        
    #find the peaks 
    detected_peaks_indices = ftools.find_peaks(integrated_ecg, FP_SPACING, FP_LIMIT)
    detected_peaks_values = raw_ecg[detected_peaks_indices]
    peaks = [detected_peaks_indices, detected_peaks_values]
    
    return integrated_ecg, peaks

def detect_qrs(raw_ecg, peaks):
    """
    Extract the QRS complex
    """
    
    REFRAC_PERIOD = 120
    QRS_PEAK_FILTERING_FACTOR = 0.125
    NOISE_PEAK_FILTERING_FACTOR = 0.125
    QRS_NOISE_DIFF_WEIGHT = 0.25

    qrs_peak_value = 0.0
    noise_peak_value = 0.0
    threshold_value = 0.0

    qrs_peaks_indices = np.array([], dtype=int)
    
    for detected_peak_index, detected_peaks_value in zip(peaks[0], peaks[1]):

        try:
            last_qrs_index = qrs_peaks_indices[-1]
        except IndexError:
            last_qrs_index = 0

        if detected_peak_index - last_qrs_index > REFRAC_PERIOD or not qrs_peaks_indices.size:
            if detected_peaks_value > threshold_value:
                qrs_peaks_indices = np.append(qrs_peaks_indices, detected_peak_index)
                qrs_peak_value = QRS_PEAK_FILTERING_FACTOR * detected_peaks_value + \
                                        (1 - QRS_PEAK_FILTERING_FACTOR) * qrs_peak_value
            else:
                noise_peak_value = NOISE_PEAK_FILTERING_FACTOR * detected_peaks_value + \
                                        (1 - NOISE_PEAK_FILTERING_FACTOR) * noise_peak_value
            threshold_value = noise_peak_value + \
                                    QRS_NOISE_DIFF_WEIGHT * (qrs_peak_value - noise_peak_value)
    qrs = [qrs_peaks_indices, raw_ecg[qrs_peaks_indices]]
    
    return qrs

def QRS_waves(record, number_samples=0, return_raw=False):
    raw_ecg, integrated_ecg, qrs = QRS_detector_offline('.\\data\\' + record + '.csv', number_samples)
    size = qrs[0].size
    q = [[], []]
    s = [[], []]
    for peak in range(1, size - 1):
        q[0].append(qrs[0][peak] - 18)
        q[1].append(raw_ecg[qrs[0][peak] - 18])
        s[0].append(qrs[0][peak] + 18)
        s[1].append(raw_ecg[qrs[0][peak] + 18])
    
    qrs = [qrs[0][1:-1], qrs[1][1:-1]]
    
    if return_raw: 
        return raw_ecg, q, qrs, s
    else:
        return q, qrs, s
    




    

