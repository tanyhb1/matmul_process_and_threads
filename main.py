import os
import subprocess
name = input()
name_c = name+".c"
name_out = name+".out"
time_log = name+"_time.log"
no_of_threads = ["1","2","4","8","16","32"]


if name == "others":
    sseq = "gcc mm_seq.c mm_test.c -o mm_seq -I . -O3 -Wall -Werror -Wextra -lpthread"
    sopenmp = "gcc mm_openmp.c mm_test.c -o mm_openmp -I . -O3 -Wall -Werror -Wextra -fopenmp"
    subprocess.call(sseq, shell=True)
    subprocess.call(sopenmp, shell=True)
    if os.path.exists(time_log):
        os.remove(time_log)
    else:
        print("CANT DELETE")
    #start time_log with the name of matmul we're using so plot.py can handle accordingly
    subprocess.call("echo " + name + " > " + time_log, shell=True)


    subprocess.call("/bin/bash -c \"(time ./mm_seq test500.txt > test500.log) &>> " + time_log + " \"", shell=True)
    subprocess.call("/bin/bash -c \"(time ./mm_openmp test500.txt > test500.log) &>> " + time_log + " \"", shell=True)

    #pass time log to plot function
    subprocess.call("cat "+  time_log + " | python3 plot.py", shell=True)
else:
    #base bash command
    s = "gcc " + name_c + " mm_test.c -o " + name_out +  " -I . -O3 -Wall -Werror -Wextra -lpthread"

    #re-define macro depending on whetehr we are dealing with threads or proc.
    if name == "mm_threadsn":
        s += " -DNUM_THREADS="
    else:
        s += " -DNUM_PROCESSES="

    
        #set up time log properly
    if os.path.exists(time_log):
        os.remove(time_log)
    else:
        print("CANT DELETE")

    #start time_log with the name of matmul we're using so plot.py can handle accordingly
    subprocess.call("echo " + name + " > " + time_log, shell=True)

    #generate all commands based on the number of threads    
    commands = [(s+x, "\"(time ./" + name_out + " test500.txt > test500.log) &>> " + time_log + "\"") for x in no_of_threads]



    #run the commands and store to the time log
    for i in range(len(commands)):
        print("No of threads = " + str(no_of_threads[i]) + " ")
        if os.path.exists(name_out):
            os.remove(name_out)
        else:
            print("CANT DELETE")
        subprocess.call( commands[i][0], shell=True)
        subprocess.call("/bin/bash -c " + commands[i][1], shell=True) #/bin/bash is here to handle the piping with stderror which requries & which is a bashism

    #just pass along the 2 process and openmp stuff too
    sseq = "gcc mm_seq.c mm_test.c -o mm_seq -I . -O3 -Wall -Werror -Wextra -lpthread"
    sopenmp = "gcc mm_openmp.c mm_test.c -o mm_openmp -I . -O3 -Wall -Werror -Wextra -fopenmp"
    subprocess.call(sseq, shell=True)
    subprocess.call(sopenmp, shell=True)
    subprocess.call("/bin/bash -c \"(time ./mm_seq test500.txt > test500.log) &>> " + time_log + " \"", shell=True)
    subprocess.call("/bin/bash -c \"(time ./mm_openmp test500.txt > test500.log) &>> " + time_log + " \"", shell=True)

    #pass time log to plot function
    subprocess.call("cat "+  time_log + " | python3 plot.py", shell=True)
