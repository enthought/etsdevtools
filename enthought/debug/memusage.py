
import os
import sys

if os.name == "nt":
    from win32 import win32pdh
    
    # from win32pdhutil, part of the win32all package
    def GetPerformanceAttributes(object, counter, instance = None,
                                 inum=-1, format = win32pdh.PDH_FMT_LONG,
                                 machine=None):
        # NOTE: Many counters require 2 samples to give accurate results,
        # including "% Processor Time" (as by definition, at any instant, a
        # thread's CPU usage is either 0 or 100).  To read counters like this,
        # you should copy this function, but keep the counter open, and call
        # CollectQueryData() each time you need to know.
        # See http://msdn.microsoft.com/library/en-us/dnperfmo/html/perfmonpt2.asp
        # My older explanation for this was that the "AddCounter" process forced
        # the CPU to 100%, but the above makes more sense :)
        path = win32pdh.MakeCounterPath( (machine,object,instance, None,
                                          inum,counter) )
        hq = win32pdh.OpenQuery()
        try:
            hc = win32pdh.AddCounter(hq, path)
            try:
                win32pdh.CollectQueryData(hq)
                type, val = win32pdh.GetFormattedCounterValue(hc, format)
                return val
            finally:
                win32pdh.RemoveCounter(hc)
        finally:
            win32pdh.CloseQuery(hq)
    
    def get_mem_usage(processName="python", instance=0):
        return GetPerformanceAttributes("Process", "Virtual Bytes",
                                        processName, instance,
                                        win32pdh.PDH_FMT_LONG, None)
    
if sys.platform[:5] == 'linux': 
    def get_mem_usage(_proc_pid_stat='/proc/%s/stat' % os.getpid()): 
        """ Return virtual memory size in bytes of the running python. 
        """ 

        try: 
            f = open(_proc_pid_stat,'r') 
            l = f.readline().split(' ') 
            f.close() 
            return int(l[22]) 
        except: 
            return
