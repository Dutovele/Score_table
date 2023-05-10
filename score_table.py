import re

teams = []
num_lines = 0
textlines = []
games_container = []
summed_container = []
team_container = []
team_dic = {}

output_matrix = []

class Game:
    global teams
    global games_container

    def __init__(self, id,team1, team2,team1_score,team2_score):
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.score_t1 = team1_score
        self.score_t2 = team2_score

class Class_team:
    global team_container

    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.scores = []

    def generate_scores_index(self):

        for i in range(len(team_container)):
            self.scores.append([i,0])

    def append_score(self,team,score):
        old_score = self.scores[team][1]
        new_score = old_score+score
        self.scores[team][1] = new_score


def connect_scores(team1,team2,score1,score2):
    global team_container
    global team_dic
    team1_id = team_dic[team1]
    team2_id = team_dic[team2]

    team1_obj = team_container[team1_id]
    team1_obj.append_score(team2_id,score2)
    team2_obj = team_container[team2_id]
    team2_obj.append_score(team1_id, score1)


def get_inputs():
    global teams
    global num_lines
    global textlines
    global teams_with_spaces
    global team_container
    global team_dic

    line1 = input()
    templine = line1.strip("\n")
    templine = line1.split(" ")
    for i in templine:
        teams.append(i.strip("\n"))

    for team in teams:
        temp_team = Class_team(len(team_container), team)
        team_dic[team] = len(team_container)
        team_container.append(temp_team)

    for team in team_container:
        team.generate_scores_index()

    for i in range(len(teams) + 1):
        column = []
        for j in range(len(teams) + 1):
            column.append("")
        output_matrix.append(column)

    line2 = input()
    num_lines = int(line2.strip("\n"))

    for line in range(num_lines):
        if line != "\n":
            temp_line = input().strip("\n")
            # temp_lìne = line.split()
            textlines.append(temp_line)


def line_iterator():
    """ From this function we add data into the class Game"""
    global teams
    global textlines
    global games_container

    hash1 = re.compile(r'(?<!\S)([\d]{1,2}):([\d]{1,2})(?!\S)')

    line_number =3
    for line in textlines:
        valid_scores = []
        # print("Looking at: ",line)
        scores = list(re.finditer(hash1, line))
        # print("Line Number: ", line_number)
        all_scores = hash1.findall(line)

        for s in all_scores:
            first_score = s[0]
            second_score = s[1]
            if int(first_score) <= 20 and int(second_score) <= 20:
                valid_scores.append(s)
        if len(valid_scores) == 1:
            if len(valid_scores) != 0 :
                first_score = valid_scores[0][0]
                second_score = valid_scores[0][1]
                if int(first_score)<=20 and int(second_score)<=20:

                    found_teams = find_team_names(line)
                    if found_teams != -1:

                        temp_game = Game(len(games_container),found_teams[0],found_teams[1],int(first_score),int(second_score))
                        connect_scores(found_teams[0],found_teams[1],int(first_score),int(second_score))
                        games_container.append(temp_game)

        line_number+=1


def find_team_names(line):

    global teams
    team_pos = []

    for team in teams:
        # print(team)
        length = len(team)
        all_teams = list(re.finditer(team, line))

        if len(all_teams)>1:
            return -1
        else:
            temp_starting_pos = line.find(team)

            if temp_starting_pos != -1:
                temp_end_pos = is_team_valid(line,temp_starting_pos,length)
                if temp_end_pos != -1:

                    team_pos.append([temp_starting_pos,temp_end_pos,team])

    if len(team_pos) < 2 or len(team_pos) > 2:
        return -1
    else:
        # print(team_pos)
        # print(line[team_pos[0][0]], line[team_pos[0][1]])
        # print(line[team_pos[1][0]], line[team_pos[1][1]])
        if team_pos[0][0] < team_pos[1][0]:
            return [team_pos[0][2],team_pos[1][2]]
        if team_pos[1][0] < team_pos[0][0]:
            return [team_pos[1][2],team_pos[0][2]]


def is_team_valid(line,starting_pos,length):
    length_of_line = len(line)

    if starting_pos == 0 and starting_pos+length < length_of_line:

        atend_pos = starting_pos + length
        if line[atend_pos] == " ":
            return atend_pos - 1
        else:
            return -1

    elif starting_pos > 0 and starting_pos+length < length_of_line:

        infront_pos = starting_pos-1
        atend_pos = starting_pos+length
        if line[infront_pos] == " " and line[atend_pos] == " ":
            return atend_pos-1
        else:
            return -1

    elif starting_pos > 0 and starting_pos+length == length_of_line:

        infront_pos = starting_pos - 1
        atend_pos = starting_pos + length
        if line[infront_pos] == " ":
            return atend_pos - 1
        else:
            return -1


def matrix_print():
    global team_dic
    global team_container
    team_names = []

    team_names.append(sorted(team_dic.keys()))

    scores = []
    data_scores = []

    for column in sorted(team_dic.keys()):

        for row in sorted(team_dic.keys()):
            column_id = team_dic[column]
            row_id = team_dic[row]

            column_obj = team_container[column_id]
            row_obj = team_container[row_id]

            column_score = row_obj.scores[column_id][1]
            row_score = column_obj.scores[row_id][1]

            data_scores += ["{}:{}".format(column_score, row_score)]


    n = len(team_names[0])
    for k in range(0, len(data_scores), n):
        scores.append(data_scores[k:k+n])

    for i in range(len(scores)):
        for j in range(len(scores)):
            if i == j:
                scores[i][j] = "     "
            else:
                continue

    format_row = "{:>8}"*(n+1)
    print(format_row.format("", *team_names[0]))
    for team, row in zip(team_names[0], scores):
        print(format_row.format(team, *row))


get_inputs()
line_iterator()
matrix_print()

