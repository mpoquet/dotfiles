#!/usr/bin/env python3
'''Timewarrior on-modify hook to call timew on start/stop commands.'''
import json
import shlex
import subprocess
import sys

def retrieve_args_dict():
    '''Read process arguments and store them in a dictionary.'''
    process_args = sys.argv[1:]
    dictionary = dict()
    for process_arg in process_args:
        splitted = process_arg.split(':')
        if len(splitted) > 1:
            key = splitted[0]
            value = ''.join(splitted[1:])
            dictionary[key] = value
    return dictionary

def determine_timew_tags(task):
    '''Determine which timew "tags" should be used for the task.'''
    tags = list()

    # Keys associated with one value
    for key in ['project', 'description']:
        if key in task:
            tags.append(task[key])

    # Keys associated with several values
    for key in ['tags']:
        if key in task:
            tags.extend(task[key])

    return tags

def generate_timew_command(cmd, tags):
    '''Generate an input for subprocess.call.'''
    tags_as_string = ' '.join(["'{}'".format(tag) for tag in tags])
    cmd_string = f'timew {cmd} {tags_as_string} :yes'
    return shlex.split(cmd_string)

def main():
    '''Main function of this module.'''
    old_task = json.loads(sys.stdin.readline())
    new_task = json.loads(sys.stdin.readline())
    args = retrieve_args_dict()

    # Do something.
    feedback = None
    if 'api' in args: # Only do something for known API.
        if args['api'] in ['2']: # APIs that give us a 'command' key.
            cmd = args['command']
            if cmd in ['start', 'stop']: # Only do something on 'start' or 'stop'.
                timew_tags = determine_timew_tags(new_task)
                timew_cmd = generate_timew_command(cmd, timew_tags)
                subprocess.call(timew_cmd)

    # Generate output as task expects it.
    print(json.dumps(new_task))
    if feedback is not None:
        print(feedback)
    sys.exit(0)

if __name__ == "__main__":
    main()
