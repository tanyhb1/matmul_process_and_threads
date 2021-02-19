import os
import subprocess
name = input()
name_c = name+".c"
name_out = name+".out"
time_log = name+"_time.log"
no_of_threads = ["1","2","4","8","16","32"]

#base bash command
s = "gcc " + name_c + " mm_test.c -o " + name_out +  " -I . -O3 -Wall -Werror -Wextra -lpthread"

#re-define macro depending on whetehr we are dealing with threads or proc.
if name == "mm_threadsn":
    s += " -DNUM_THREADS="
else:
    s += " -DNUM_PROCESSES="

#generate all commands based on the number of threads    
commands = [(s+x, "\"(time ./" + name_out + " test500.txt > test500.log) &>> " + time_log + "\"") for x in no_of_threads]

#set up time log properly
if os.path.exists(time_log):
    os.remove(time_log)
else:
    print("CANT DELETE")

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
print(time_log + " | python plot.py")
subprocess.call("cat "+  time_log + " | python plot.py", shell=True)
