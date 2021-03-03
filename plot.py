#!/usr/bin/env python3

import subprocess
import sys
import matplotlib.pyplot as plt

no_of_threads = ["1","2","4","8","16","32"]

def plot2(arr):
    for mm in arr:
        name = mm[0]
        curr = mm[1:]
        x = [int(t) for t in no_of_threads]
        y_real = [float(x[1].split("m")[1].strip("s")) for x in curr]
        if name == "mm_seq":
            y_real = [float(curr[0][1].split("m")[1].strip("s")) for _ in range(6)]
        real = plt.plot(x,y_real, marker='o', label="real time for " + name)
    plt.xlim(0,35)
    plt.xticks([int(x) for x in no_of_threads])
    plt.xlabel("Number of threads")
    plt.title("Plot for real time taken by all four matrix multiplication methods")
    plt.ylabel("Run time in seconds")
    plt.legend(loc="upper left")
    plt.savefig("realtimes.png", bbox_inches='tight')
    plt.show()
def plot(res, curr_mm_name):
    if curr_mm_name == "mm_threadsn" or curr_mm_name == "mm_procn" or curr_mm_name == "mm_openmp":
        curr = res[:6]
        other_mms = res[6:]

        x = [int(t) for t in no_of_threads]
        y_real = [float(x[0][1].split("m")[1].strip("s")) for x in curr]
        y_user = [float(x[1][1].split("m")[1].strip("s")) for x in curr]
        y_sys = [float(x[2][1].split("m")[1].strip("s")) for x in curr]

        real = plt.plot(x,y_real, marker='o', label="real time")
        user = plt.plot(x,y_user, marker='o', label="user time")
        sys = plt.plot(x,y_sys, marker='o', label="sys time")
        
        plt.xlim(0,35)
        plt.xticks([int(x) for x in no_of_threads])
        if curr_mm_name == "mm_threadsn":
            plt.xlabel("Number of threads")
            plt.title("Plot for n-threading")
        elif curr_mm_name == "mm_openmp":
            plt.xlabel("Number of threads")
            plt.title("Plot for n-threading using OpenMP")
        else:
            plt.xlabel("Number of processes")
            plt.title("Plot for n-processes")
        plt.ylabel("Run time in seconds")            

        y_seq = [float(other_mms[0][0][1].split("m")[1].strip("s")) for _ in range(6)]

        seq = plt.plot(x,y_seq, marker='o',linestyle='dashed', label="seq real time")
        plt.legend(loc="upper left")
        plt.savefig(curr_mm_name+".png", bbox_inches='tight')
        plt.show()

    else:
        x = [int(t) for t in no_of_threads]
        seq_real = [float(res[0][0][1].split("m")[1].strip("s")) for _ in range(6)]
        seq_user = [float(res[0][1][1].split("m")[1].strip("s")) for _ in range(6)]
        seq_sys = [float(res[0][2][1].split("m")[1].strip("s")) for _ in range(6)]
        openmp_real = [float(res[1][0][1].split("m")[1].strip("s")) for _ in range(6) ]
        openmp_user = [float(res[1][1][1].split("m")[1].strip("s")) for _ in range(6)]
        openmp_sys = [float(res[1][2][1].split("m")[1].strip("s")) for _ in range(6)]
        plt.plot(x,seq_real, marker='o', label="seq real time")
        plt.plot(x,seq_user, marker='o', label="seq user time")
        plt.plot(x,seq_sys, marker='o', label="seq sys time")
        plt.plot(x,openmp_real, marker='o', label="openmp real time")
        plt.plot(x,openmp_user, marker='o', label="openmp user time")
        plt.plot(x,openmp_sys, marker='o', label="openmp sys time")
        plt.xlim(0,35)
        plt.xlabel("Number of threads")
        plt.title("Plot for Sequential MM and Sequential W/ OpenMP MM")
        plt.ylabel("Run time in seconds")
        plt.legend(loc="upper left")
        plt.savefig("others.png",bbox_inches='tight')
        plt.show()

def main():
    res = []
    i = 0
    tmp = []
    curr_mm_name = ""
    handle_real = False 
    for line in sys.stdin :
        payload = line.strip("\n").split("\t")
        if "other" in line:
            handle_real = False
        if "real time" in line:
            handle_real = True
        if not handle_real:
            if "mm" in line or "others" in line:
                curr_mm_name = payload[0]
            elif len(payload) > 1:
                if i < 2:
                    tmp.append(payload)
                    i += 1
                else:
                    tmp.append(payload)
                    res.append(tmp)
                    tmp = []
                    i = 0
        else:
            if "mm" in line:
                res.append(tmp)
                tmp = []
                curr_mm_name = payload[0]
                tmp.append(curr_mm_name)
            else:
                if len(payload) > 1 and payload[0] == "real":
                    tmp.append(payload)
    if not handle_real:
        plot(res, curr_mm_name)
    else:
        res.append(tmp)
        plot2(res[1:])


if __name__ == "__main__":
    main()
