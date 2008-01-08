"""This is a very simple wrapper around the xnee command.

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005, Prabhu Ramachandran, Enthought, Inc.
# License: BSD Style.

import os
import tempfile


def record(display=None, out=None, all_events=False,
           no_expose=False, first_last=False, loops=1000,
           time=0, stop_key=None, pause_key=None, resume_key=None,
           insert_key=None, mouse=False, keyboard=False,
           recorded_resolution=None, sync=True,
           device_event_range=None, other_args=''):
    """Record the action to a file specified as out.  If out is not
    specified it returns the recorded data as a string.
    """
    cmd_line = 'xnee -rec -l %s'%loops
    if display:
        cmd_line += ' --display %s'%display
    if out:
        cmd_line += ' -o %s'%out
    if all_events:
        cmd_line += ' --all-events'
    if no_expose:
        cmd_line += ' --no-expose'    
    if first_last:
        cmd_line += ' -fl'
    if time:
        cmd_line += ' --time %s'%time
    if stop_key:
        cmd_line += ' --stop-key %s'%stop_key
    if pause_key:
        cmd_line += ' --pause-key %s'%pause_key
    if resume_key:
        cmd_line += ' --resume-key %s'%resume_key
    if insert_key:
        cmd_line += ' --insert-key %s'%insert_key
    if recorded_resolution:
        cmd_line += ' --recorded-resolution %s'%recorded_resolution
    if mouse:
        cmd_line += ' --mouse'
    if keyboard:
        cmd_line += ' --keyboard'
    if not sync:
        cmd_line += ' --no-sync'
    if device_event_range:
        cmd_line += ' --device-event-range %s'%device_event_range

    cmd_line += ' %s'%other_args
    print "Running: %s"%cmd_line
    if out:
        return os.system(cmd_line)
    else:
        output = os.popen(cmd_line, 'r')
        return output.read()

    
def play(display=None, fname=None, string=None, all_events=False,
         no_expose=False, time=0, mouse=False, keyboard=False,
         speed_percent=None, replay_resolution=None, sync=True,
         device_event_range=None, other_args=''):
    """Playback the action from given file or string.
    """
    cmd_line = 'xnee -rep'
    if display:
        cmd_line += ' --display %s'%display
    if fname:
        cmd_line += ' -f %s'%fname
    if all_events:
        cmd_line += ' --all-events'
    if no_expose:
        cmd_line += ' --no-expose'    
    if time:
        cmd_line += ' --time %s'%time
    if mouse:
        cmd_line += ' --mouse'
    if keyboard:
        cmd_line += ' --keyboard'
    if not sync:
        cmd_line += ' --no-sync'
    if replay_resolution:
        cmd_line += ' --replay-resolution %s'%recorded_resolution
    if speed_percent:
        cmd_line += ' --speed-percent %s'%speed_percent
    if device_event_range:
        cmd_line += ' --device-event-range %s'%device_event_range

    cmd_line += ' %s'%other_args
    print "Running: %s"%cmd_line
    if fname:
        return os.system(cmd_line)
    elif string:
        inp, out = os.popen2(cmd_line, 'r')
        inp.write(string)
        return inp.close()
    else:
        raise RuntimeError, 'Need to set either the fname or string args.'
    
