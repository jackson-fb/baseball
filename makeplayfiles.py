import io
import pickle
import pandas as pd
import os
import re
import csv

eventsDirectory = "data/retrosheet/Test_Events/"


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

def load_pickle():
    print("loading pickle...")
    try:
        with open("uniqueplays.pickle", "rb") as f:
            data = pickle.load(f)
            print("done!")
            return data
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

def clear_duplicates(_list):
    result = list(set(_list))
    result.sort()
    return result

def create_pickle():
    teams = load_retrosheet()
    filteredplays = []
    uniqueplays = []
    for team in teams:
        for game in team:
            plays = game[game['type'] == 'play']
            for index, row in plays.iterrows():
                uniqueplays.append(row['play'])
                print(len(uniqueplays))

    uniqueplays = clear_duplicates(uniqueplays)


    print("Pickling...")
    try:
        with open("uniqueplays.pickle", "wb") as f:
            pickle.dump(uniqueplays, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)
    print("Pickled!")

def dump_to_file(data, filename):
    print(f"writing {len(data)} lines to {filename}")
    f = open(filename, "w")
    for datum in data:
        f.write(datum + '\n')
    f.close()
    print("done!")


def smartsplit(_string, sep, compiledre):
    if '(' not in _string:
        return _string.split(sep)
    #iterator = compiledre.finditer(_string)
    result = re.findall("\([^\)/]*/[^\)/]*\)", _string)
    for i in result:
        problemsection = str(i)
        problemsection = problemsection.replace('/', '|')
        _string = _string.replace(i, problemsection)




    #split by sep unless sep is inside bracket. if it is, replace with temp sep, then seperate, then revert
    #for i in range(0, len(_string)):
        #if _string[i] == sep:
            #if in brackets
    _string = _string.split('/')
    # for segment in _string:
    #     segment = segment.replace()
    return _string
    #print("")


if __name__ == '__main__':

    #create_pickle()

    #total plays, first, second, third, baddies
    uniqueplays = load_pickle()

    print("writing to files...")

    first = []
    second = []
    third = []
    baddies = []
    compiledre = re.compile("\([^\)/]*/[^\)/]*\)")
    for play in uniqueplays:
        print(play)
        splitplay = smartsplit(play, '/', compiledre)
        #splitplay = play.split('/')
        if len(splitplay) == 2:
            first.append(splitplay[0])
            second.append(splitplay[1])

        elif len(splitplay) == 3:
            first.append(splitplay[0])
            second.append(splitplay[1])
            third.append(splitplay[2])
        else:
            baddies.append(play)

    first = clear_duplicates(first)
    second = clear_duplicates(second)
    third = clear_duplicates(third)
    baddies = clear_duplicates(baddies)


    #smartsplit("46(1)/FO/G4.2-H(E6/TH)(NR)(UR);B-2(E6/TH)", '', compiledre)

    dump_to_file(uniqueplays, "uniqueplays.txt")
    dump_to_file(first, "first.txt")
    dump_to_file(second, "second.txt")
    dump_to_file(third, "third.txt")
    dump_to_file(baddies, "baddies.txt")



    #for play in uniqueplays:




    print("done writing!")
