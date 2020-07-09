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

test_sigs = sys.argv[1:]
print("TESTING PAN TOMPKINS ON SIGNALS ", test_sigs, " OF MIT-BIH")
for record in test_sigs:
    print("\nTESTING ON 30 SEQUENCES OF SIGNAL ...", record)
    ann = wfdb.rdann('./wfdb/' + str(record), 'atr')
    PVC_indices = np.array([i for i in range(len(ann.symbol)) if ann.symbol[i] =='V'])
    sequence = np.loadtxt('./data/' + str(record) + '.csv', skiprows=1, delimiter=',')
    sequence = sequence[:, 1]
    seq_size = 1260
    seqs = list(range(sequence.size // seq_size))
    PVCs = 0
    # print("PROCESSING ", seqs[-1] + 1, " SEQUENCES OF SIGNAL ", record, " ...\n")
    for seq in seqs[:-1]:
            flag = run(sequence[seq * seq_size:min((seq + 1) * seq_size, 650000)])
            if flag:
                PVCs = PVCs + 1

    print("\nPVC PEAKS DETECTED: ", PVCs, " PVC PEAKS MISSED: ", PVC_indices.size - PVCs)
    print("\nERROR RATE OF: ", 100 * (PVC_indices.size - PVCs)/ PVC_indices.size, "%.")
