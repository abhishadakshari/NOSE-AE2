import math

from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):

        for p in self.processes:
            if p.process_state == ProcessStates.READY:
                return p


    def dispatcher_func(self, cur_process):

        cur_process.process_state = ProcessStates.RUNNING
        execution_time = cur_process.run_for(self.quantum, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type= EventTypes.PROC_CPU_DONE, event_time= self.time + execution_time)


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):

        min_time = 100
        process = 0
        for p in self.processes:
            if p.service_time < min_time and p.process_state == ProcessStates.READY:
                process = p
                min_time = p.service_time

        return process

    def dispatcher_func(self, cur_process):

        cur_process.process_state = ProcessStates.RUNNING
        execution_time = cur_process.run_for(self.quantum, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE,
                     event_time=self.time + execution_time)

class RR(SchedulerDES):
    def scheduler_func(self, cur_event):

        for p in self.processes:
            if p.process_state == ProcessStates.READY:
                return p


    def dispatcher_func(self, cur_process):


        execution_time = cur_process.run_for(self.quantum, self.time)
        cur_process.process_state = ProcessStates.RUNNING

        if cur_process.remaining_time == 0.0:

            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE,
                         event_time=self.time + execution_time)

        else:
            self.processes.remove(cur_process)
            self.processes.append(cur_process)
            cur_process.process_state = ProcessStates.READY
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ,
                         event_time=self.time + execution_time)

class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):

        min_time = 100
        process = 0
        for p in self.processes:
            if p.remaining_time < min_time and p.process_state == ProcessStates.READY:
                process = p
                min_time = p.remaining_time

        return process

    def dispatcher_func(self, cur_process):

        #time between current time and the time of the next event occuring
        time_to_stop =  self.next_event_time() - self.time
        #execute for until time of next event
        execution_time = cur_process.run_for(time_to_stop, self.time)

        #if it has mangaged to complete processing then terminate
        if cur_process.remaining_time == 0.0:
            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE,
                         event_time=self.time + execution_time)


        else:
            cur_process.process_state = ProcessStates.READY
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ,
                         event_time=self.time + execution_time)



