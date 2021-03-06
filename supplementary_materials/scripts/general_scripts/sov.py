import sys
import os
import numpy as np
from scipy import stats
import statistics

def extract_segments(sequence, ss):
    sequence = sequence.rstrip()
    segments = []
    position = 0
    
    while position < len(sequence):
        
        segment = []
        
        while sequence[position] == ss and position < len(sequence) - 1:
            segment.append(position)
            position += 1
        
        if segment and position == len(sequence)-1:     
            segment.append(position)
            
        if len(segment) > 0:
            segments.append(set(segment))
       
        position += 1

    return(segments)


def sov_score(original_segments, predicted_segments):
    summatory =[]
    normalization = 0

    for orig_segment in original_segments:
        normalization += len(orig_segment)
        
        for pred_segment in predicted_segments:

            if orig_segment & pred_segment:
                min_ov = len(orig_segment & pred_segment)
                max_ov = len(orig_segment | pred_segment)
                delta = min([(max_ov - min_ov), min_ov, (len(orig_segment)//2), (len(pred_segment)//2)])
                summatory.append(((min_ov + delta)/max_ov*len(orig_segment)))

    if normalization != 0:
        sov = sum(summatory) * (1/normalization) * 100
        
    elif normalization == 0:
        sov = 100

    return(sov)


def get_sov(original_file, predicted_file):
    seq_counter = 0
    ss_list = ["H", "E", "-"]
    ss_dict = dict([ss, np.zeros(2)] for ss in ss_list)
    sov_dict = {'H': [], 'E':[], '-':[]}
    with open(original_file, "r") as open_orig:
        orig_lines = open_orig.readlines()
        
    with open(predicted_file, "r") as open_pred:
        pred_lines = open_pred.readlines()
    
    for original, predicted in zip (orig_lines, pred_lines):
        original_seq = original.rstrip()
        predicted_seq = predicted.rstrip()
             
        for ss in ss_list:

            orig_segments = extract_segments(original_seq, ss)
            pred_segments = extract_segments(predicted_seq, ss)
            sov_dict[ss].append(sov_score(orig_segments, pred_segments))
            #ss_dict[ss][0] += sov_score(orig_segments, pred_segments)
            #seq_counter += 1

    #seq_counter = seq_counter / 3
    #for ss in ss_dict.values():
    #    ss[1] = ss[0]/int(seq_counter)
    
    #print("Number of sequences:\t" + str(int((seq_counter))))
    #for ss in ss_list:
    #    print(ss + ":\t" + str(ss_dict[ss][1]))
    print('SOV\tAVG\t\tSTDERR')
    for i in sov_dict.items():
        print(i[0], statistics.mean(i[1]), stats.sem(i[1], ddof = 0))
    return()

if __name__ == "__main__":
    original_file = sys.argv[1]
    predicted_file = sys.argv[2]
    get_sov(original_file,predicted_file)