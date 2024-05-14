######################### DIME . PY ###############################

import datetime

meeting = 15
half_count = 2
half_duration = 45
start_delay = 15
intermission = 30
intermission_count = 1
inspection_and_leaving = 30
encore_count = 0
encore_duration = 5

concert_start = datetime.timedelta(hours=19)
concert_duration = datetime.timedelta(seconds=(
        meeting*60 +
        half_count*half_duration*60 +
        start_delay*60 +
        intermission*60 +
        intermission_count*60 +
        inspection_and_leaving*60 +
        encore_count*encore_duration*60
    ))
concert_end = concert_start + concert_duration

print(f"concert_start: {concert_start}")
print(f"concert_duration: {concert_duration}")
print(f"concert_end: {concert_end}")
