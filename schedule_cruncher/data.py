from unicodedata import normalize
from datetime import timedelta

csv = """1,"Schubert, String Quartet No. 14 in D minor ""Death and the maiden"" 1st mvt.",4,"김경태, 하준수, 전준탁, 정지욱",13
2,"Mozart, Eine Kleine Nachtmusik, K. 525 Allegro, Rondo",5,"김지현, 권영재, 여정민, 이수빈, 이수진",10
3,"Schubert, Piano Quintet D.667 'Trout', 4th mvt.",5,"김종호, 이호은, 강은서, 신승원, 이병우",8
4,Beethoven Violin Sonata no.9 'Kreutzer' 1st mvt,2,"최준원, 김민수",12
5,"L. v. Beethoven, String Quartet No.14, Op.131, 6th and 7th mvt.",4,"김명혜, 윤선혜, 노희원, 이희수",10
6,지브리/ 이웃집 토토로 - path of the wind,2,"최준원, 이민철",4
7,Fritz Kreisler - Praeludium and Allegro,2,"김동진, 황준호",6
8,"Maurice Ravel, String Quartet in F major (1st mvt.)",4,"강은서, 김지현, 이호은, 김민주",8
9,<스누피아> A. Dvorak - Piano Quintet no.2 Op.81 2nd mov.,5,"김민수, 황준호, 전유진, 박마음, 김민주",14
10,<스누피아> A. Dvorak - Piano Quintet no.2 Op.81 4th mov.,5,"김종호, 김지현, 권영재, 서용삼, 이수빈",7
11,<스누피아> F. Mendelssohn - Piano Trio no.1 Op.49 1st mov.,3,"김민우, 김경태, 정지욱",10
12,<스누피아> Gabriel Fauré - Après un rêve,2,"이예림, 김민수",4
13,<스누피아> Schubert Piano Quintet d.667 'Trout' 1st mvt,5,"김민수, 김경태, 서용삼, 이수빈, 김민주",13"""

csv = normalize('NFKC', csv)

csv.replace('""', '%')

# Convert csv to semicolon-separated values
ssv = ''
inside_string = False
for x in csv:
    if not inside_string and x == ',':
        x = ';'
    if x != '"':
        ssv += x
    if x == '"':
        inside_string = not inside_string

csv.replace('%', '"')

lines = ssv.split('\n')

fields = [line.split(';') for line in lines]

for field in fields:
    integers = (0, 2, 4)
    for i in integers:
        field[i] = int(field[i])

    field[3] = field[3].split(', ')


class Team:
    def __init__(self, idx, name, members, length):
        self.idx = idx
        self.name = name
        self.members = members
        self.length = length
        self.rehearsal_start = None
        self.recording_start = None
        self.recording_end = None

    def __repr__(self):
        return str([self.idx, self.name, self.members, self.length])

    def set_time(self, rehearsal_start):
        self.rehearsal_start = rehearsal_start
        rehearsal_time = int((self.length + 1) * 1.5)
        self.recording_start = self.rehearsal_start + timedelta(minutes=rehearsal_time)
        self.recording_end = self.recording_start + timedelta(minutes=self.length)


teams = []

for field in fields:
    teams.append(Team(field[0], field[1], field[3], field[4]))
