from schedule_cruncher.scheduler import *
from schedule_cruncher.result_checker import answer
from datetime import datetime, timedelta

answer = (6, 4, 11, 1, 2, 10, 13, 8, 3, 9, 7, 12, 5)

teams.sort(key=lambda team: answer.index(team.idx))

two_minutes = timedelta(minutes=2)
quarter = timedelta(minutes=15)

teams[0].set_time(datetime(2020, 7, 9, hour=13, minute=45))
for i in range(1, len(teams)):
    team = teams[i]
    if i == 6:
        interval = quarter
    else:
        interval = two_minutes

    team.set_time(teams[i - 1].recording_end + interval)

print("57회 하계앙상블 팀별 시간표")
for i, team in enumerate(teams):
    rehearsal_start = str(team.rehearsal_start.time())[:-3]
    recording_start = str(team.recording_start.time())[:-3]
    recording_end = str(team.recording_end.time())[:-3]
    print()
    print(f"순번 {i + 1}: {team.name}")
    print(f"\t[리허설 시작: {rehearsal_start} | 녹화 시작: {recording_start} | 녹화 종료: {recording_end}]")
    print('\t' + ', '.join(team.members) + '')

total_people = [0] * 13

print()
print("연주자별 참여시간")
for member in sorted(member_to_idxs.keys()):
    relevant_teams = []
    indexes = []
    for i, team in enumerate(teams):
        if team.idx in member_to_idxs[member]:
            relevant_teams.append(team)
            indexes.append(i + 1)

    start_time = str(relevant_teams[0].rehearsal_start.time())[:-3]
    end_time = str(relevant_teams[-1].recording_end.time())[:-3]
    print()
    print(f"{member}: 참여곡 {indexes}")
    print(f"\t첫 곡 리허설 시작: {start_time} | 마지막 곡 녹화 종료: {end_time}")

    for i in range(indexes[0], indexes[-1] + 1):
        if i - 1 not in indexes:
            total_people[i - 1] += 1

print()
print('시간대별 대기인원수 추정')
print(total_people)
