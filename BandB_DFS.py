# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 19:47:29 2020

@author: Manting
"""

import sys
import pandas as pd
import heapq as hq
import time

#%%
df = (pd.read_excel("test instance.xlsx" ,header = None)).transpose() # read excel
proc = df.values.tolist() # transform to list
job = proc[1 : 11]
#job = [[6, 0], [2, 2], [3, 2], [2, 6], [5, 7], [2, 9]]

#%% MinHeap
def heap_insert(arr, n, x):
    j = n - 1
    parent = (j - 1) // 2
    while parent >= 0:
        if x[0] < arr[parent][0]:
            arr[j] = arr[parent]
            j = parent
            if parent == 0:
                break
            parent = (parent - 1) // 2
        else:
            break
    arr[j] = x
    
def heapify(arr, n):
    x = arr[n - 1]
    i = 0
    j = 2 * i + 1
    while j < n:
        if j + 1 < n:
            if arr[j][0] > arr[j + 1][0]:
                j += 1
        if arr[j][0] >= x[0]:
            break
        else:
            arr[(j - 1) // 2] = arr[j]
            j = 2 * j + 1
    arr[(j - 1) // 2] = x
    arr.pop(n - 1)

#%% SRPT
def srptHeap(procc, t):
    #t = 0 # current arrive time
    complete = 0 # already number of finished process
    srpt = [] # heap
    total = 0 # the objective value
    proc = procc.copy()
    job_q = len(proc)
    
    while complete != job_q: # until all processes finished
        while proc !=[] and proc[0][1] <= t:
            srpt.append(proc[0])
            heap_insert(srpt, len(srpt), proc[0].copy())
            proc.remove(proc[0])
            # print(srpt) 
        if len(srpt) != 0 and srpt[0][0] == 0: # heapify
            heapify(srpt, len(srpt))
            complete += 1
            total += t
            # print(total,t)
        if len(srpt) != 0: # reduce remaining time
            srpt[0][0] -= 1
            
        t += 1
    return total 
    
#%% counting makespan and sumC
def SRPT(makespan, seq, sumC):
    if makespan == 0:
        makespan = sum(seq)
        return makespan, makespan
    else:
        if makespan < seq[1]:
            makespan_new = sum(seq)
        else:
            makespan_new = makespan + seq[0]
        return makespan_new, sumC + makespan_new

#%% Depth First Search
def dfs(all_job, makespan, sumC, seq):
    global count, ubc, best, best_seq
    count += 1
    
    if(len(all_job) == 0): # until visit leaf nodes
        return sumC
    
    for i in range(len(all_job)):
        all_job_temp = all_job[ : i] + all_job[i + 1 : ] 
        makespan_n, sumC_n = SRPT(makespan, all_job[i], sumC)
        LB = sumC_n + srptHeap(all_job_temp, makespan_n)  
        
        if LB <= best:
            seq_temp = seq + [all_job[i]]
            sumC_tmp = dfs(all_job_temp, makespan_n, sumC_n, seq_temp)  

            if sumC_tmp < best:
                best = sumC_tmp
                best_seq = seq_temp
                ubc += 1
    
    return best

#%% main()
s = time.time()
count, ubc, best, best_seq = 0, 0, sys.maxsize, []
x = dfs(job, 0, 0, [])
e = time.time()
print('DFS:')
print(' Objective value: ', x,'\n Optimal permutation: ', best_seq, '\n DFS run time:', e-s)
print(' count: ', count)
print(' UB下降次數: ', ubc)




