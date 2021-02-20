#!/usr/bin/env python3

import subprocess
import sys
import matplotlib.pyplot as plt

no_of_threads = ["1","2","4","8","16","32"]

def plot(res, curr_mm_name):
    if curr_mm_name == "mm_threadsn" or curr_mm_name == "mm_procn":
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
        else:
            plt.xlabel("Number of processes")
            plt.title("Plot for n-processes")
        plt.ylabel("Run time in seconds")            

        print(other_mms[1])
        y_seq = [float(other_mms[0][0][1].split("m")[1].strip("s")) for _ in range(6)]
        y_openmp = [float(other_mms[1][0][1].split("m")[1].strip("s")) for _ in range(6)]

        seq = plt.plot(x,y_seq, marker='o',linestyle='dashed', label="seq real time")
        openmp = plt.plot(x,y_openmp, marker='o',linestyle='dashed', label="openmp real time")
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
    for line in sys.stdin :
        payload = line.strip("\n").split("\t")
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

    plot(res, curr_mm_name)

if __name__ == "__main__":
    main()
