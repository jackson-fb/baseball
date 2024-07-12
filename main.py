import io
import pickle
import pandas as pd
import os
import csv
import pygame
import pygame_menu

from classes import *

eventsDirectory = "data/retrosheet/Test_Events/"
rostersDirectory = "data/retrosheet/Rosters/"
peopleDirectory = "./data/retrosheet/biofile.txt"
teamsDirectory = "./data/retrosheet/teams.txt"
fieldDirectory = "./data/retrosheet/fieldlocations.txt"

def interpret_play(play):
    print("Interpreting: " + play)
    splitPlay = play.split('/')
    if len(splitPlay) == 1:
        if len(splitPlay[0]) == 1:
            if (splitPlay[0] == 'W'):
                print("Walk!")
                return
            elif (splitPlay[0] == 'K'):
                print("Strikeout!")
                #self.out()
                print("Out!")
                return
            else:
                print(f"Unknown symbol: {splitPlay[0]}")
                return

    numSegments = len(splitPlay)
    fielders = [str(x) for x in range(1, 10)]
    for i in range(0, numSegments):
        currentSegment = splitPlay[i]
        playLength = len(currentSegment)
        if i == 0:
            # FIRST SEGMENT: play description, fielding
            #print("FIRST SEGMENT:")
            j = 0
            while j < playLength:
                if (currentSegment[j] == 'S'):
                    if (playLength > 1):
                        if (currentSegment[j + 1] == 'B'):
                            if (currentSegment[j + 2] == '2'):
                                print("Second base stolen!")
                                j += 2
                            elif (currentSegment[j + 2] == '3'):
                                print("Third base stolen!")
                                j += 2
                            elif (currentSegment[j + 2] == 'H'):
                                print("Home plate stolen!")
                                print("UNKNOWN: IS THIS SUPPOSED TO HAPPEN")
                                j += 2
                            else:
                                print(f"UNKNOWN SYMBOL OR STEAL ON PLAY:{play.play}")

                    print("Single!")
                elif (currentSegment[j] == 'D'):
                    # print("Double!")
                    if (playLength > 1):
                        if (currentSegment[j + 1] == 'G' and currentSegment[j + 2] == 'R'):
                            print("Ground rule double!")
                            j += 2
                        elif (currentSegment[j + 1] in fielders):
                            # print(f"Ball fielded by {get_position_readable(int(currentSegment[j+1]))}.")
                            print("Double!")
                            pass


                        else:
                            print(f"UNKNOWN SYMBOL ON PLAY {play.play}")



                elif (currentSegment[j] == 'T'):
                    print("Triple!")
                elif (currentSegment[j] == 'H'):
                    if (currentSegment[j + 1] == 'R'):
                        print("Home Run!")
                        j += 1
                    else:
                        print(f"UNKNOWN SYMBOL PROVIDED AFTER 'H': {currentSegment[j + 1]}")

                else:
                    if currentSegment[j] in fielders:
                        if playLength == 1:
                            print(f"Ball caught by {get_position_readable(int(currentSegment[j]))}!")
                            #self.out()
                            print("Out!")
                        else:
                            print(f"Ball fielded by {get_position_readable(int(currentSegment[j]))}.")
                            if (j == playLength):
                                #self.out()
                                print("Out!")
                    else:
                        if (currentSegment[j] == '('):
                            openBracketIndex = currentSegment[j:].find('(') + j
                            closeBracketIndex = currentSegment[j:].find(')') + j
                            bracketSection = currentSegment[openBracketIndex + 1:closeBracketIndex]
                            print("Put out runner")
                            print(bracketSection)
                            j = closeBracketIndex
                        elif currentSegment[j] == 'E':
                            print(f"Error by {get_position_readable(int(currentSegment[j + 1]))}")
                            j += 1
                        else:
                            print(f"idk man{currentSegment[j]}")
                j += 1
            pass
        elif i == 1:
            # Location
            #g = ground ball
            #l = line drive
            #p = pop fly
            #f = fly ball
            #bunts put a b before, BG, BP

            #print("SECOND SEGMENT:")
            j = 0
            while j < playLength:
                print(currentSegment[j])
                j += 1

        elif i == 2:
            # Description / advancements
            #print("THIRD SEGMENT:")
            j = 0
            while j < playLength:
                print(currentSegment[j])
                j += 1
        else:
            print(f"INVALID NUMBER OF SEGMENTS PROVIDED IN PLAY {play}")


def interpret_pitches(pitches):
    pitchesArray = []
    i = 0
    strikes = 0
    balls = 0
    while i < len(pitches):
        # +>*.
        if pitches[i] == '+':
            pitchesArray.append(pitches[i:i + 2])
            i += 1
        elif pitches[i] == '>':
            pitchesArray.append(pitches[i:i + 2])
            i += 1
        elif pitches[i] == '*':
            pitchesArray.append(pitches[i:i + 2])
            i += 1
        else:
            pitchesArray.append(pitches[i])
        i += 1

    for pitch in pitchesArray:
        line = f"Count is {balls} and {strikes}.\n"
        extra = ""
        if (len(pitch) > 1):
            if (pitch[0] == '+'):
                extra = "Threw by Catcher!"
            elif pitch[0] == '*':
                extra = "Wild! Blocked by Catcher."
            elif pitch[0] == '>':
                extra = "Runner went!"  # TODO what does this mean
            pitch = pitch[1:]
        if (pitch == 'C'):
            pitchResult = "Called Strike"
            strikes += 1
        elif (pitch == 'S'):
            pitchResult = "Swinging Strike"
            strikes += 1
        elif (pitch == 'B'):
            pitchResult = "Ball"
            balls += 1
        elif (pitch == 'F'):
            pitchResult = "Foul Ball"
            if (strikes < 2):
                strikes += 1
        elif (pitch == 'X'):
            pitchResult = "Ball put into play"
        elif (pitch == 'T'):
            pitchResult = "Foul Tip"
            if (strikes < 2):
                strikes += 1
        elif (pitch == 'H'):
            pitchResult = "Hit By Pitch"
        elif (pitch == 'L'):
            pitchResult = "Foul Bunt"
            if (strikes < 2):
                strikes += 1
        elif (pitch == 'M'):
            pitchResult = "Missed Bunt"
            strikes += 1
        elif (pitch == 'P'):
            pitchResult = "Pitchout"
        elif (pitch == 'N'):
            pitchResult = "No Pitch"
        elif (pitch == 'V'):
            pitchResult = "Automatic Ball"
            balls += 1
        elif (pitch == 'K'):
            pitchResult = "Strike of unknown type"
            strikes += 1
        elif (pitch == 'U'):
            pitchResult = "Unknown Pitch"
        elif (pitch == 'Q'):
            pitchResult = "Swinging Strike on Pitchout"
            strikes += 1
        elif (pitch == 'R'):
            pitchResult = "Foul Ball on Pitchout"
            if (strikes < 2):
                strikes += 1
        elif (pitch == '1'):
            pitchResult = "Throw to First"
        elif (pitch == '2'):
            pitchResult = "Throw to Second"
        elif (pitch == '3'):
            pitchResult = "Throw to Third"
        elif (pitch == '.'):
            pitchResult = "Play interrupted!"
        else:
            print(f"UNKNOWN SYMBOL!!!! provided: {pitch}")

        line += f"{pitchResult} {extra}"
        print(line)
        if (len(extra) > 0):
            # print(extra)
            extra = ""

class PBP_Element:
    pass


class Play(PBP_Element):
    def __init__(self, line):
        self.inning = line["inning"]
        self.isHome = line["home"] == '1'
        self.id = line["retro_id"]
        self.count = line["count"]
        self.pitches = line["pitches"]
        self.play = line["play"]
        # print(self)


class Sub(PBP_Element):
    def __init__(self, line):
        self.id = line[1]
        self.name = line[2]
        self.isHome = line[3] == "1"
        self.battingOrder = line[4]
        self.position = line[5]

    pass


class Com(PBP_Element):
    def __init__(self, line):
        self.text = line[1]


class Game:
    def __init__(self, df):
        self.info = {}
        self.playbyplay = []
        self.home_lineup = ["??"]
        # TODO LOAD STARTERS
        for index, row in df.iterrows():
            if (row[0] == "info"):
                self.info[row[1]] = row[2]
            if (row[0] == "play"):
                self.playbyplay.append(Play(row))
            if (row[0] == "sub"):
                self.playbyplay.append(Sub(row))
            if (row[0] == "com"):
                self.playbyplay.append(Com(row))


class team:
    def __init__(self, dfs, roster):
        self.games = []
        self.roster = roster
        for df in dfs:
            self.games.append(Game(df))


class Data:
    def __init__(self, _years, _people, _teams, _field):
        self.years = _years
        self.people = _people
        self.teams = _teams
        self.field = _field

    def getReadableTeamName(self, teamid):
        team = self.teams[self.teams["id"] == teamid]
        city = team["city"].values[0]
        name = team["name"].values[0]
        return f"{city} {name}"


class Lineup:
    def __init__(self):
        self.pitcher = ""
        self.catcher = ""
        self.first_base = ""
        self.second_base = ""
        self.third_base = ""
        self.short_stop = ""
        self.left_field = ""
        self.center_field = ""
        self.right_field = ""
        self.designated_hitter = ""


class GameState:
    def __init__(self, game):
        self.home_id = game.info["hometeam"]
        self.away_id = game.info["visteam"]
        self.year = game.info["date"][:4]
        self.home_score = 0
        self.away_score = 0
        self.home_hits = 0
        self.away_hits = 0
        self.inning = 0
        self.top = False
        self.outs = 0
        self.strikes = 0
        self.balls = 0

    def out(self):
        self.outs += 1
        print(f"Out! {self.outs} outs.")
        if(self.outs==3):
            print("3 outs! Change side!")
            self.outs = 0


        # for playSegment in splitPlay:
        #     print(f"SEG: {playSegment}")
        #     i = 0
        #     while i < len(playSegment):
        #         if playSegment[i]
        #
        #         i+=1

    # def interpret_pitches(self, pitches):
    #     pitchesArray = []
    #     i = 0
    #     while i < len(pitches):
    #         # +>*.
    #         if pitches[i] == '+':
    #             pitchesArray.append(pitches[i:i + 2])
    #             i += 1
    #         elif pitches[i] == '>':
    #             pitchesArray.append(pitches[i:i + 2])
    #             i += 1
    #         elif pitches[i] == '*':
    #             pitchesArray.append(pitches[i:i + 2])
    #             i += 1
    #         else:
    #             pitchesArray.append(pitches[i])
    #         i += 1
    #
    #     for pitch in pitchesArray:
    #         line = f"Count is {self.balls} and {self.strikes}.\n"
    #         extra = ""
    #         if (len(pitch) > 1):
    #             if (pitch[0] == '+'):
    #                 extra = "Threw by Catcher!"
    #             elif pitch[0] == '*':
    #                 extra = "Wild! Blocked by Catcher."
    #             elif pitch[0] == '>':
    #                 extra = "Runner went!"  # TODO what does this mean
    #             pitch = pitch[1:]
    #         if (pitch == 'C'):
    #             pitchResult = "Called Strike"
    #             self.strikes += 1
    #         elif (pitch == 'S'):
    #             pitchResult = "Swinging Strike"
    #             self.strikes += 1
    #         elif (pitch == 'B'):
    #             pitchResult = "Ball"
    #             self.balls += 1
    #         elif (pitch == 'F'):
    #             pitchResult = "Foul Ball"
    #             if (self.strikes < 2):
    #                 self.strikes += 1
    #         elif (pitch == 'X'):
    #             pitchResult = "Ball put into play"
    #         elif (pitch == 'T'):
    #             pitchResult = "Foul Tip"
    #             if (self.strikes < 2):
    #                 self.strikes += 1
    #         elif (pitch == 'H'):
    #             pitchResult = "Hit By Pitch"
    #         elif (pitch == 'L'):
    #             pitchResult = "Foul Bunt"
    #             if (self.strikes < 2):
    #                 self.strikes += 1
    #         elif (pitch == 'M'):
    #             pitchResult = "Missed Bunt"
    #             self.strikes += 1
    #         elif (pitch == 'P'):
    #             pitchResult = "Pitchout"
    #         elif (pitch == 'N'):
    #             pitchResult = "No Pitch"
    #         elif (pitch == 'V'):
    #             pitchResult = "Automatic Ball"
    #             self.balls += 1
    #         elif (pitch == 'K'):
    #             pitchResult = "Strike of unknown type"
    #             self.strikes += 1
    #         elif (pitch == 'U'):
    #             pitchResult = "Unknown Pitch"
    #         elif (pitch == 'Q'):
    #             pitchResult = "Swinging Strike on Pitchout"
    #             self.strikes += 1
    #         elif (pitch == 'R'):
    #             pitchResult = "Foul Ball on Pitchout"
    #             if (strikes < 2):
    #                 self.strikes += 1
    #         elif (pitch == '1'):
    #             pitchResult = "Throw to First"
    #         elif (pitch == '2'):
    #             pitchResult = "Throw to Second"
    #         elif (pitch == '3'):
    #             pitchResult = "Throw to Third"
    #         elif (pitch == '.'):
    #             pitchResult = "Play interrupted!"
    #         else:
    #             print(f"UNKNOWN SYMBOL!!!! provided: {pitch}")
    #
    #         line += f"{pitchResult} {extra}"
    #         print(line)
    #         if (len(extra) > 0):
    #             # print(extra)
    #             extra = ""

    def play(self, _play):
        battingTeam = self.home_id if _play.isHome else self.away_id
        # print(data.people[_play.id])
        self.strikes = 0
        self.balls = 0
        if (_play.play == "NP"):
            return
        print()
        print("********************")

        batter = data.people[data.people.PLAYERID == _play.id]
        print(_play.play)
        print(_play.pitches)
        print(
            f"{batter['NICKNAME'].values[0]} {batter['LAST'].values[0]} to bat for the {data.getReadableTeamName(battingTeam)}.")
        # print(_play.pitches)
        interpret_pitches(_play.pitches)
        interpret_play(_play.play)








def load_retrosheet():
    originalfiles = []
    for filename in os.scandir(eventsDirectory):
        if filename.is_file():
            if filename.name.endswith("EVA") or filename.name.endswith("EVN"):
                # pad files
                f_orig = open(filename, "r")
                originalfiles.append(f_orig.read())
                f_orig.close()


    originalfiles = [file.split('\n') for file in originalfiles]
    modifiedfiles = []
    for file in originalfiles:

        modifiedfile = [line + ',' * (6-line.count(',')) for line in file]

        modifiedfiles.append(modifiedfile)


    dfs = []

    for file in modifiedfiles:
        teamdfs = []
        fullfile = io.StringIO('\n'.join(file))

        filestring = fullfile.getvalue()
        filestring = filestring.split('\n')
        currentdf = []
        for line in filestring:

            if line.startswith("id,") and len(currentdf) > 1:
                #print(line)

                teamdf = pd.read_csv(io.StringIO('\n'.join(currentdf)),
                                     names=['type', 'inning', 'home', 'retro_id', 'count', 'pitches', 'play'])

                #labeleddf = (teamdf["inning"][0], teamdf)
                teamdfs.append(teamdf)
                currentdf.clear()
                currentdf.append(line)
            else:
                currentdf.append(line)
        if len(currentdf) > 1:
            teamdf = pd.read_csv(io.StringIO('\n'.join(currentdf)), names=['type', 'inning', 'home', 'retro_id', 'count', 'pitches', 'play'])
            # labeleddf = (teamdf["inning"][0], teamdf) used to label with id, getting rid
            teamdfs.append(teamdf)
            #print("a")

        labeleddf = teamdfs[0]["inning"]
        dfs.append(teamdfs)
        #dfs.append(pd.read_csv(, names=['type','inning','home', 'retro_id','count','pitches','play']))

    # testgame = Game(dfs[0][0][1])

    print("done loading")
    return dfs

def load_testfiles():
    first = open("first.txt", "r")
    first_data = first.read()
    first.close()

    second = open("second.txt", "r")
    second_data = second.read()
    second.close()

    third = open("third.txt", "r")
    third_data = third.read()
    third.close()

    baddies = open("baddies.txt", "r")
    baddies_data = baddies.read()
    baddies.close()

    first_data = [x.strip() for x in first_data.split('\n') if len(x.strip()) >= 1]
    second_data = [x.strip() for x in second_data.split('\n') if len(x.strip()) >= 1]
    third_data = [x.strip() for x in third_data.split('\n') if len(x.strip())  >= 1]
    baddies_data = [x.strip() for x in baddies_data.split('\n') if len(x.strip())  >= 1]

    return first_data, second_data, third_data, baddies_data



def load_rosters():
    rosterYears = {}
    rosterID = ""
    rosterYear = ""
    rosterData = {}
    rosterLines = []
    for filename in os.scandir(rostersDirectory):
        if filename.is_file():
            if filename.name.endswith(".ROS"):
                f = open(filename, "r")
                rosterID = filename.name[:3]
                rosterYear = filename.name[3:7]
                if rosterYear not in rosterYears:
                    rosterYears[rosterYear] = {}

                rosterString = f.read()
                f.close()

                rosterLines = [x.strip() for x in rosterString.split('\n') if len(x.strip()) > 5]

                rosterdf = pd.read_csv(io.StringIO('\n'.join(rosterLines)),
                                     names=['id', 'last_name', 'first_name', 'bats', 'throws', 'team', 'position'])

                rosterYears[rosterYear][rosterID] = rosterdf
                f.close()


                # Year
                # > TeamID
                # > > Roster
    print("done loading rosters")
    return rosterYears

def parse_retrosheet(dfs, teams): #TODO remove teams
    # this is a list of games, all by a team in a year
    # 3 characters for team, followed by 4 for year
    # list of games
    # > tuple, ID, gamedf (do i need this tuple? probably not)
    years = {}
    rosterYears = load_rosters()

    for df in dfs:
        teamID = df[0]["inning"][0][:3]
        teamName = teams[teams["id"] == teamID]["city"].values[0] + " " + teams[teams["id"] == teamID]["name"].values[0]
        teamyear = df[0]["inning"][0][3:7]
        print(f"Loading {teamyear} {teamName}")
        if teamyear not in years:
            years[teamyear] = {}
        roster = rosterYears[teamyear][teamID]
        years[teamyear][teamID] = team(df, roster)

        print("done")
    print("done loading")
    return years

def load_field():
    print("loading field from file")
    field_dict = {}
    f = open(fieldDirectory, "r")
    field_data = f.read()
    f.close()
    field_lines = [x.strip().split(',') for x in field_data.split('\n') if len(x.strip()) > 2]
    #field_info
    for x in field_lines:
        field_dict[x[0]] = x[1]

    print("Done loading!")
    return field_dict


def load_teams():
    teams = pd.read_csv(teamsDirectory, names=["id", "league", "city", "name", "founded", "ended"])
    return teams

def load_people():
    print("loading people from file")

    f = open(peopleDirectory, "r")
    people_data = f.read()
    f.close()
    people_lines = [x.strip() for x in people_data.split('\n') if len(x.strip()) > 5]

    people = pd.read_csv(io.StringIO('\n'.join(people_lines)), index_col=False)
    #                      names=["id", "last_name", "first_name", "use_name", "birth_date",
    #                             "birth_city", "birth_state", "birth_country", "player_debut",
    #                             "player_last_game", "coach_debut", "coach_last_game", "ump_debut",
    #                             "ump_last_game", "death_date", "death_city", "death_state", "death_country",
    #                             "bat", "throw", "height", "weight", "cemetery", "cemetery_city", "cemetery_state",
    #                             "cemetery_country", "cemetery_note", "birth_name", "name_change", "bat_change", "hof"
    #                             ],
    #                      dtype={'cemetery': "string", 'bat_change': "string", 'hof': "string"}
    #                      )
    #print(people.dtypes)
    print("done loading")
    return people

def create_pickle():
    play_by_play, teams, people, field = load_data()
    print("Pickling...")
    try:
        with open("data.pickle", "wb") as f:
            pickle_data = Data(play_by_play, people, teams, field)
            pickle.dump(pickle_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)
    print("Pickled!")

# def pickle_data():
#     raw_dfs = load_retrosheet()
#     print("Loaded raw data, parsing...")
#     years = parse_retrosheet(raw_dfs)
#     print("Parsed! Adding rosters...")
#
#     print("Added!")
#     print("Pickling...")
#     try:
#         with open("data.pickle", "wb") as f:
#             pickle.dump(years, f, protocol=pickle.HIGHEST_PROTOCOL)
#     except Exception as ex:
#         print("Error during pickling object (Possibly unsupported):", ex)
#     print("Pickled!")

def load_pickle():

    try:
        with open("data.pickle", "rb") as f:
            data = pickle.load(f)
            return data
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

def get_field_position(location: str) -> str:
    #TODO fill this out
    pass

def get_position_acronym(number: int) -> str:
    acronyms = ["??", "P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"]
    if number < 1 or number > 9:
        print(f"INVALID POSITION NUMBER PROVIDED! {number}")
        return -1
    return acronyms[number]

def get_position_readable(number):
    name = ["??????", "Pitcher", "Catcher", "First Base", "Second Base", "Third Base", "Shortstop",
                "Left Fielder", "Centre Fielder", "Right Fielder"]
    if number < 1 or number > 9:
        print(f"INVALID POSITION NUMBER PROVIDED! {number}")
        return -1
    return name[number]

def playGame(game, data):
    game_state = GameState(game)
    awayTeamID = game.info["visteam"]
    homeTeamID = game.info["hometeam"]
    homeTeamName = data.getReadableTeamName(homeTeamID)
    awayTeamName = data.getReadableTeamName(awayTeamID)
    print(f"{awayTeamName} at {homeTeamName}")

    for play in game.playbyplay:
        try:
            #print(play.play)
            game_state.play(play)
        except AttributeError:
            pass

def load_data():
    field = load_field()
    pbp_dfs = load_retrosheet()
    teams = load_teams()
    playbyplay = parse_retrosheet(pbp_dfs, teams)
    people = load_people()


    return playbyplay, teams, people, field

    pass

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #load_people()
    #load_rosters()
    #create_pickle()
    #years = load_pickle()

    #create_pickle()

    # pygame.init()
    # surface = pygame.display.set_mode((600, 400))
    #
    # menu = pygame_menu.Menu('Welcome', 400, 300,
    #                         theme=pygame_menu.themes.THEME_BLUE)
    #
    # menu.add.text_input('Name :', default='John Doe')
    # menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    # menu.add.button('Play', start_the_game)
    # menu.add.button('Quit', pygame_menu.events.EXIT)
    #
    # menu.mainloop(surface)


    data = load_pickle()

    first, second, third, baddies = load_testfiles()

    print("Ready!")

    for play in first:
        interpret_play(play + "//")

    print("done loading")
    playGame(data.years["2021"]["TOR"].games[60], data)