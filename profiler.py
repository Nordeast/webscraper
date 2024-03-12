from datetime import datetime

program_start_time = datetime.now()

def start():
    program_start_time = datetime.now()

def end():
    # print how long the program took to run
    program_duration = datetime.now() - program_start_time
    seconds = program_duration.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print("Time to complete:")
    print('{:02}:{:02}:{:02} HH:MM:SS'.format(
        int(hours), int(minutes), int(seconds)))