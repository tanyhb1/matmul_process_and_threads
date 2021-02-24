import os
import subprocess
name = input()
name_c = name+".c"
name_out = name+".out"
time_log = name+"_time.log"
no_of_threads = ["1","2","4","8","16","32"]


if name == "mm_openmp":

    s = "gcc " + name_c + " mm_test.c -o " + name_out +  " -I . -O3 -Wall -Werror -Wextra -fopenmp"
    if os.path.exists(time_log):
        os.remove(time_log)
    else:
        print("CANT DELETE")
        
    #start time_log with the name of matmul we're using so plot.py can handle accordingly
    subprocess.call("echo other" + " > " + time_log, shell=True)
    subprocess.call("echo " + name + " > " + time_log, shell=True)

    #generate all commands based on the number of threads    
    commands = [(s, "\"(time " + "OMP_NUM_THREADS=" + x + " ./" + name_out + " test500.txt > test500.log) &>> " + time_log + "\"") for x in no_of_threads]
    
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

    subprocess.call(sseq, shell=True)

    subprocess.call("/bin/bash -c \"(time ./mm_seq test500.txt > test500.log) &>> " + time_log + " \"", shell=True)
    
    #pass time log to plot function
    print(" **************** ")
    print("plot for openmp")
    print(" **************** ")
    subprocess.call("cat "+  time_log + " | python3 plot.py", shell=True)

elif name == "all real time":
    sseq = "gcc mm_seq.c mm_test.c -o mm_seq.out -I . -O3 -Wall -Werror -Wextra"
    sopenmp = "gcc mm_openmp.c mm_test.c -o mm_openmp.out -I . -O3 -Wall -Werror -Wextra -fopenmp"
    sthreadsn = "gcc mm_threadsn.c mm_test.c -o mm_threadsn.out -I . -O3 -Wall -Werror -Wextra -lpthread -DNUM_THREADS="
    sprocn = "gcc mm_procn.c mm_test.c -o mm_procn.out -I . -O3 -Wall -Werror -Wextra -lpthread -DNUM_PROCESSES="
    #set up time log properly
    time_log = "realtime.log"
    if os.path.exists(time_log):
        os.remove(time_log)
    else:
        print("CANT DELETE")

    names = {"mm_seq": sseq, "mm_openmp": sopenmp, "mm_threadsn":sthreadsn, "mm_procn":sprocn}
    subprocess.call("echo real time" + " >> " + time_log, shell=True)
    for name in names:
        print(name)

        name_c = name+".c"
        name_out = name+".out"
        s = names[name]
        #start time_log with the name of matmul we're using so plot.py can handle accordingly
        subprocess.call("echo " + name + " >> " + time_log, shell=True)
        if name == "mm_seq":
            commands = [(s, "\"(time ./" + name_out + " test500.txt > test500.log) &>> " + time_log +
                         "\"")]
        elif name == "mm_threadsn" or name == "mm_procn":
            commands = [(s+x, "\"(time ./" + name_out + " test500.txt > test500.log) &>> " + time_log + "\"") for x in no_of_threads]
        else:
            #generate all commands based on the number of threads    
            commands = [(s, "\"(time " + "OMP_NUM_THREADS=" + x + " ./" + name_out + " test500.txt > test500.log) &>> " + time_log + "\"") for x in no_of_threads]
            #run the commands and store to the time log
        for i in range(len(commands)):
            print("No of threads = " + str(no_of_threads[i]) + " ")
            if os.path.exists(name_out):
                os.remove(name_out)
            else:
                print("CANT DELETE")
            subprocess.call( commands[i][0], shell=True)
            subprocess.call("/bin/bash -c " + commands[i][1], shell=True) #/bin/bash is here to handle the piping with stderror which requries & which is a bashism

             
    #pass time log to plot function
    print(" **************** ")
    print("plot for the real time taken by all methods")
    print(" **************** ")
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
    subprocess.call("echo other" + " > " + time_log, shell=True)
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

    subprocess.call(sseq, shell=True)

    subprocess.call("/bin/bash -c \"(time ./mm_seq test500.txt > test500.log) &>> " + time_log + " \"", shell=True)
    

    #pass time log to plot function
    print(" **************** ")
    print("plot for " + name )
    print(" **************** ")
    subprocess.call("cat "+  time_log + " | python3 plot.py", shell=True)

