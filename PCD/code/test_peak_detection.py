from pantompkins import *
import numpy as np
import wfdb
import sys
# testing on on signal1 of 106.csv = [sample #, raw signal1, raw signal2]
records = ['100', '101', '102', '103', '104', '105', '106', '107', '108',
           '109', '111', '112', '113', '114', '115', '116', '117', '118',
           '119', '121', '122', '123', '124', '200', '201', '202', '203',
           '205', '207', '208', '209', '210', '212', '213', '214', '215',
           '217', '219', '220', '221', '222', '223', '228', '230', '231',
           '232', '233', '234']

# record = 100
avg_error = 0
test_sigs = sys.argv[1:]
print("TESTING PAN TOMPKINS ON SIGNALS ", test_sigs, " OF MIT-BIH")

for record in test_sigs:
    print("\nTESTING ON SIGNAL ...", record)
    ann = wfdb.rdann('./wfdb/' + str(record), 'atr')
    ann.sample = np.array([ann.sample[ind] for ind in range(len(ann.sample[:-1])) if ann.sample[ind] != ann.sample[ind + 1]])
    sequence = np.loadtxt('./data/' + str(record) + '.csv', skiprows=1, delimiter=',')
    sequence = sequence[:21600, 1]
    qrs_peaks_indices, flag = run(sequence, True)
    number_peaks = min(ann.sample.size, qrs_peaks_indices.size)
    err = 0
    err_margin = 31 #31 samples for sampling rate of 360 per second is 0.08 second which is acceptable for ECG
    my_ind = 0
    mit_ind = 0
    while my_ind < number_peaks and mit_ind < number_peaks:
        if abs(ann.sample[mit_ind] - qrs_peaks_indices[my_ind]) < err_margin:
            mit_ind += 1
            my_ind += 1
            continue
        if qrs_peaks_indices[my_ind] - ann.sample[mit_ind] > err_margin:
            mit_ind += 1
        else:
            my_ind += 1
            err += 1
    print("\nPEAKS DETECTED: ", qrs_peaks_indices.size,  " PEAKS MISSED: ", err)
    avg_error = avg_error + err / number_peaks
avg_error /= 5
avg_error *= 100
print('\nAVERAGE ERROR RATE IS ', avg_error, "%.")
