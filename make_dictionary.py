"""
    Name: Xiuyi Feng
    Email: xiuyi.feng15@myhunter.cuny.edu
    Resources:  geeksforgeeks.org for min.() and max.() format
                Think CS Chapter 12 for dictionary contents
"""
import os

def make_dictionary(data, kind = "min"):
    """
    Creating a dictionary with a key of the remote unit ID + turnstile unit number.
    Depending on kind, the resulting dictionary will store the minimum entry
    number seen (as an integer), the maximum entry number seen (as an integer),
    or the station name (as a string).
    Returns the resulting dictionary.

    Keyword arguments:
    kind -- kind of dictionary to be created:  min, max, station
    """

    #Placeholder-- replace with your code
    new_dict = {}
    for line in data:
        words=line[:-1].split(',')
        key=words[1]+ ","+ words[2]
        if kind=="min":
            if key in new_dict:
                new_dict[key]=min(new_dict[key],int(words[-2]))
            else:
                new_dict[key]=int(words[-2])
        elif kind=="max":
            if key in new_dict:
                new_dict[key]=max(new_dict[key],int(words[-2]))
            else:
                new_dict[key]=int(words[-2])
        elif kind=="station":
            new_dict[key]=words[3]
    return new_dict

def get_turnstiles(station_dict, stations = None):
    """
    If stations is None, returns the names of all the turnstiles stored as keys
    in the inputted dictionary.
    If non-null, returns the keys which have value from station in the inputed dictionary.
    Returns a list.

    Keyword arguments:
    stations -- None or list of station names.
    """

    #Placeholder-- replace with your code
    lst = []
    if stations is None:
        lst=list(station_dict.keys())
    else:
        for key in station_dict.keys():
            if station_dict[key] in stations:
                lst.append(key)
    return lst

def compute_ridership(min_dict,max_dict,turnstiles = None):
    """
    Takes as input two dictionaries and a list, possibly empty, of turnstiles.
    If no value is passed for turnstile, the default value of None is used
    (that is, the total ridership for every station in the dictionaries).
    Returns the ridership (the difference between the minimum and maximum values)
    across all turnstiles specified.

    Keyword arguments:
    turnstiles -- None or list of turnstile names
    """

    #Placeholder-- replace with your code
    total = 0
    if turnstiles is None:
        for key in min_dict.keys():
            total+=(max_dict[key]-min_dict[key])
    else:
        for name in turnstiles:
            total+=(max_dict[name]-min_dict[name])
    return total

def main():
    """
    Opens a data file and computes ridership, using functions above.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(here, 'turnstile_220611.txt')
    #file_name = 'turnstile_220611.txt'
    #Store the file contents in data:
    with open(file_name,encoding='UTF-8') as file_d:
        lines = file_d.readlines()
    #Discard first line with headers:
    data = lines[1:]

    #Set up the three dictionaries:
    min_dict = make_dictionary(data, kind = "min")
    max_dict = make_dictionary(data, kind = "max")
    station_dict = make_dictionary(data, kind = "station")

    #Print out the station names, alphabetically, without duplicates:
    print(f'All stations: {sorted(list(set(station_dict.values())))}')

    #All the turnstiles from the data:
    print(f'All turnstiles: {get_turnstiles(station_dict)}')
    #Only those for Hunter & Roosevelt Island stations:
    print(get_turnstiles(station_dict, stations = ['68ST-HUNTER CO','ROOSEVELT ISLND']))

    #Checking the ridership for a single turnstile
    ridership = compute_ridership(min_dict,max_dict,turnstiles=["R051,02-00-00"])
    print(f'Ridership for turnstile, R051,02-00-00:  {ridership}.')

    #Checking the ridership for a station
    hunter_turns = get_turnstiles(station_dict, stations = ['68ST-HUNTER CO'])
    ridership = compute_ridership(min_dict,max_dict,turnstiles=hunter_turns)
    print(f'Ridership for Hunter College: {ridership}.')

if __name__ == "__main__":
    main()
