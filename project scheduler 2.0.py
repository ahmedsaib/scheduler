import copy
from collections import deque
import time
class processes:
  def __init__(self,pid,arrival,burst,priority=0):
    self.pid=pid
    self.arr=arrival
    self.burst= burst
    self.priority= priority
    self.remainingt= burst
    self.start_time = -1
    self.completion_time = 0
    self.waiting_time = 0
    self.turnaround_time = 0

  def __repr__(self):
        return f"{self.pid}"

def calcul(processes,throughput,check=False):
   sum_waiting_time=0
   sum_turnaround_time=0
   processes_completed=0

   for p in processes:
      p.turnaround_time = p.completion_time - p.arr
      p.waiting_time = p.turnaround_time - p.burst
      sum_turnaround_time+=p.turnaround_time
      sum_waiting_time+=p.waiting_time
      if p.completion_time>throughput:
          pass
      else:
          processes_completed+=1

      if check==True:
          print(f"Process {p.pid}: Waiting Time = {p.waiting_time}, Turnaround Time = {p.turnaround_time}")
   if throughput != 0:
      debit=processes_completed/throughput
   else:
      debit=0
   average_waiting_time=sum_waiting_time/len(processes)
   average_turnaround_time=sum_turnaround_time/len(processes)
   return {
      "Average Waiting Time":average_waiting_time,
      "Average Turnaround Time":average_turnaround_time,
      "Throughput":debit
      }

def gantt(timeline):
    print("\nGantt Chart:")
    top = "|"
    bottom = ""

    for block in timeline:
        pid = block["pid"]
        start = block["start"]
        stop = block["stop"]                                      # calculating the width of each block based on start and stop time
        width = stop - start
        top += f" P{pid} ".ljust(width + 2, "-") + "|"             
        bottom += f"{start}".ljust(width + 3)

    bottom += f"{timeline[-1]['stop']}"  
    print(top)
    print(bottom)

def FCFS(processes,timeline):
   current_time=0
   processes=sorted(processes,key=lambda x:x.arr)
   for p in processes:
      if current_time<p.arr:
         current_time=p.arr
      p.start_time=current_time
      current_time+=p.burst
      p.completion_time=current_time
      timeline.append({
         "pid": p.pid, 
         "start": p.start_time,
         "stop": p.completion_time})
   return processes,current_time

def SJF(processes, timeline):
   processes=sorted(processes,key=lambda x:x.arr)
   current_time = 0
   completed = []
   ready_queue = deque(processes)
   
   while ready_queue:
      available = [p for p in ready_queue if p.arr <= current_time]
      if not available:
         current_time = min(p.arr for p in ready_queue)
         available = [p for p in ready_queue if p.arr <= current_time]      
      p = min(available, key=lambda x: x.burst)

      p.start_time = current_time
      current_time += p.burst
      p.completion_time = current_time

      timeline.append({
         "pid": p.pid,
         "start": p.start_time,
         "stop": p.completion_time
      })

      completed.append(p)
      ready_queue.remove(p)

   return completed, current_time
def SRTF(processes, timeline):
   processes = sorted(processes, key=lambda x: x.arr)
   current_time = 0
   completed = []
   ready_queue = deque(processes)                 # putting all processes in the ready queue
   while ready_queue:
      available = [p for p in ready_queue if p.arr <= current_time]   #if a process has arrived in the current time it enters the list
      if not available:
         current_time = min(p.arr for p in ready_queue)
         available = [p for p in ready_queue if p.arr <= current_time]
      p = min(available, key=lambda x: x.remainingt)          # choosing the process with the smallest rt

      if p.start_time == -1:
         p.start_time = current_time

      current_time += 1
      p.remainingt -= 1
 
      if timeline and timeline[-1]["pid"] == p.pid:        
         timeline[-1]["stop"] = current_time               
      else:
         timeline.append({
            "pid": p.pid,
            "start": current_time - 1,
            "stop": current_time
         })

      if p.remainingt == 0:
         p.completion_time = current_time
         completed.append(p)
         ready_queue.remove(p)
   return completed, current_time

def round_robin(processes, timeline, quantum):
    processes = sorted(processes, key=lambda x: x.arr)
    current_time = 0
    completed = []
    ready_queue = deque()          
    i = 0                          
    n = len(processes)
    while len(completed) < n:
        while i < n and processes[i].arr <= current_time:
            ready_queue.append(processes[i])
            i += 1
        if not ready_queue:
            current_time = processes[i].arr
            continue

        p = ready_queue.popleft() 

        if p.start_time == -1:
            p.start_time = current_time

        start = current_time      
        time = min(quantum, p.remainingt)

        current_time += time
        p.remainingt -= time

        timeline.append({
            "pid": p.pid,
            "start": start,       
            "stop": current_time
        })
        while i < n and processes[i].arr <= current_time:
            ready_queue.append(processes[i])
            i += 1
        if p.remainingt == 0:
            p.completion_time = current_time
            completed.append(p)
        else:
            ready_queue.append(p)  
    return completed, current_time
def non_preemptive_priority(processes, timeline):
    current_time=0
    ready_queue=deque()
    completed=[]
    processes=sorted(processes,key=lambda x:x.arr)
    while len(completed)<len(processes):
        for p in processes:
            if p.arr<=current_time and p not in ready_queue and p not in completed:
                ready_queue.append(p)
        if not ready_queue:
         current_time+=1
         continue
        p=min(ready_queue,key=lambda x:x.priority)                
        p.start_time=current_time
        current_time+=p.burst
        p.completion_time=current_time
        timeline.append({
            "pid": p.pid, 
            "start": p.start_time,
            "stop": p.completion_time})
        completed.append(p)
        ready_queue.remove(p)
    return processes,current_time
def preemptive_priority(processes, timeline):
   processes = sorted(processes, key=lambda x: x.arr)
   current_time = 0
   completed = []
   ready_queue = deque()
   n=len(processes)
   i=0
   
   while len(completed) < n:
      while i < n and processes[i].arr <= current_time:
         ready_queue.append(processes[i])
         i += 1
      if not ready_queue:
            current_time +=1
            continue
      p = min(ready_queue, key=lambda x: x.priority)

      if p.start_time == -1:
         p.start_time = current_time

      current_time += 1
      p.remainingt -= 1

      if timeline and timeline[-1]["pid"] == p.pid:
         timeline[-1]["stop"] = current_time
      else:
         timeline.append({
            "pid": p.pid,
            "start": current_time - 1,
            "stop": current_time
         })

      if p.remainingt == 0:
         p.completion_time = current_time
         completed.append(p)
         ready_queue.remove(p)
   return completed, current_time
def main():
    try:
        n = int(input("Enter number of processes: "))
        if n < 1: raise ValueError
    except:   
        print("Invalid input. N should be >0 .")
        return  
    process = []
    t=time.time()
    for i in range(n):
        print(f"\nProcess P{i+1}")
        if i==0:
            print(" The first arrival time is always = 0 ")      
            arr = 0
        else:
            arr=int(time.time()-t)
            print(f" Current system time for arrival: {arr}")            #the arrival time is calculated based on how much time i spent inputing the data
        burst = int(input("  Burst time: "))
        priority = int(input("  priority: "))
        process.append(processes(i+1, arr, burst, priority))

    quantum = int(input("\nEnter time quantum (Round Robin): "))
    throughput = int(input("\nEnter throughtput time:"))

    
    print("\n===== FCFS =====")
    fcfs = copy.deepcopy(process)                                 # using deepcopy to avoid overwriting the original process data
    timeline_fcfs = []

    completed_fcfs, _ = FCFS(fcfs, timeline_fcfs)
    gantt(timeline_fcfs)
    print(calcul(completed_fcfs, throughput,True))

   
    print("\n===== SJF =====")
    sjf = copy.deepcopy(process)
    timeline_sjf = []

    completed_sjf, _ = SJF(sjf, timeline_sjf)
    gantt(timeline_sjf)
    print(calcul(completed_sjf, throughput,True))

    
    print("\n===== SRTF =====")
    srtf = copy.deepcopy(process)
    timeline_srtf = []

    completed_srtf, _ = SRTF(srtf, timeline_srtf)
    gantt(timeline_srtf)
    print(calcul(completed_srtf, throughput,True))

    
    print(f"\n===== ROUND ROBIN (Quantum = {quantum}) =====")
    rr = copy.deepcopy(process)
    timeline_rr = []

    completed_rr, _ = round_robin(rr, timeline_rr, quantum)
    gantt(timeline_rr)
    print(calcul(completed_rr, throughput,True))

    print("\n==== preemptive priority =====")
    pp = copy.deepcopy(process)
    time_line_pp = []
    completed_pp, _ =preemptive_priority(pp,time_line_pp)
    gantt(time_line_pp)
    print(calcul(completed_pp,throughput,True))

    print("\n==== non preemptive priority =====")
    npp = copy.deepcopy(process)
    time_line_npp = []
    completed_npp, _ =non_preemptive_priority(npp,time_line_npp)
    gantt(time_line_npp)
    print(calcul(completed_npp,throughput,True))

    print("\n==== Ranking the algorithms based on Average Waiting Time, Average Turnaround Time And Throughput ====\n")
    algos = {
       "FCFS":calcul(completed_fcfs,throughput),
       "SJF":calcul(completed_sjf,throughput),
       "SRTF":calcul(completed_srtf,throughput),                                      # putting all algo in a dictionary
      "Round Robin":calcul(completed_rr,throughput),
      "preemptive priority":calcul(completed_pp,throughput),
      "non preemptive priority":calcul(completed_npp,throughput)
    }
    Ranked_by_awt = sorted(algos.items(), key=lambda x:float(x[1]["Average Waiting Time"]))      # sorting the dictionary based on metrics
    Ranked_by_att = sorted(algos.items(), key=lambda x:float(x[1]["Average Turnaround Time"])) 
    ranked_by_throu = sorted(algos.items(), key=lambda x:float(x[1]["Throughput"]), reverse=True)
    print(" Ranking by Average Waiting Time :")
    for rank, (algo,metrics)in enumerate(Ranked_by_awt,start=1):
        print(f" {rank}. {algo} - Average Waiting Time: {metrics['Average Waiting Time']}")
    print("\n Ranking by Average Turnaround Time :")
    for rank, (algo,metrics)in enumerate(Ranked_by_att,start=1):
        print(f" {rank}. {algo} - Average Turnaround Time: {metrics['Average Turnaround Time']}")    #print the rankings
    print("\n Ranking by Throughput :")
    for rank, (algo,metrics)in enumerate(ranked_by_throu,start=1):
        print(f" {rank}. {algo} - Throughput: {metrics['Throughput']}")
    print("\n==== End of Scheduling Simulation. ====")   
if __name__ == "__main__":
    main()