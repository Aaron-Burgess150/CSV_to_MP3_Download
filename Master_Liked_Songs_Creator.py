# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 12:48:36 2025

@author: Aaron A S Burgess
"""

import pandas as pd

# for testing and seeing the whole dataframe
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None) # Show all columns

# function to set up the individual playlist
def setUp_individual_playlist(filepath):
    try:
        # load the dataset in
        df = pd.read_csv(filepath)
    except FileNotFoundError:
       print(f"Error: File '{filepath}' not found!\n")
       return None

    
    # make the list to delete and delete those columns
    list_to_delete = ["Release Date", "Duration (ms)", "Popularity", "Explicit", "Added By", "Added At", "Genres", "Record Label", "Danceability", "Energy", "Key", "Loudness", "Mode", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo", "Time Signature"]
    dropped_df = df.drop(list_to_delete, axis=1)


    # check for empty cells and return if there are any
    # say what rows in the dataframe are missing songs
    dropped_isNa_df = dropped_df.isna().any()
    if(dropped_isNa_df.sum() > 0 or dropped_df.isin(['undefined']).any().any()):
        print(f"{filepath} is missing data in important columns (Track URI, Track Name, Album Name, or Artist Name(s))\n")
        copy = dropped_df.copy()
        mask = copy.isna() | (copy == "undefined")
        rows_missing = mask.any(axis=1)
        indexes = copy.index[rows_missing].tolist()
        indexes_1_based = [x+2 for x in indexes]
        print(f"Rows with missing or undefined data: {indexes_1_based}")
        return None
        
    
    # rename columns in the DataFrame (not using the isna one)
    new_df = dropped_df.rename(columns={'Track URI': 'Spotify - id', 'Track Name': 'Track name', 'Album Name':'Album', 'Artist Name(s)':'Artist name'})
    
    
    # change data to drop the spotifiy:track: from the Spotify - id
    new_df["Spotify - id"] = new_df["Spotify - id"].str.replace("spotify:track:", "", regex=False)
    new_df["Spotify - id"] = new_df["Spotify - id"].str.replace("spotify:episode:", "", regex=False)

    
    # sort the dataframe by Spotify ID
    sorted_df = new_df.sort_values(by="Spotify - id")

    # return the sorted and filtered dataframe
    return sorted_df


def sort_songs(filepath): #function for sorting the liked songs, both at start and after appending
    try:
        # load the dataset in
        df = pd.read_csv(filepath, encoding='cp1252')
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found!\n")
        return None

    #sort the liked songs by Spotify ID to match the sorting method of the playlist
    sorted_liked_songs = df.sort_values(by="Spotify - id")

    return sorted_liked_songs


def check_empty(liked_songs):
    liked_songs_isNa = liked_songs.isna().any()
    if (liked_songs_isNa.sum() > 0 or liked_songs_isNa.isin(['undefined']).any().any()):
        print("Liked_songs is missing data in important columns (Track URI, Track Name, Album Name, or Artist Name(s))\n")
        copy = liked_songs.copy()
        mask = copy.isna() | (copy == "undefined")
        rows_missing = mask.any(axis=1)
        indexes = copy.index[rows_missing].tolist()
        indexes_1_based = [x+2 for x in indexes]
        print(f"Rows with missing or undefined data: {indexes_1_based}")
    else:
        return


# THIS IS WHATS CAUSING THE DUPLICATES BOOOO YOU SUCK
# you were actually fine I think so idk what was going on but I debugged with smaller and copied

def find_shared_songs(liked_songs, playlist, i): #helper function to find the shared songs
    # to be ran in a for loop that calls the function and passes i as the active row in the playlist
    if playlist.iloc[i, 0] in liked_songs.iloc[:, 3].values: #if playlist song in liked songs
        return None #so the new i can be passed in
    else: #playlist song is not in liked songs, so append to liked songs
        return i


"""

# not needed I dont think
def find_in_liked_songs(liked_songs, playlist, i): #taking the song from playlist, find what row it's in in liked songs
    # NECESSARY that the song is in liked songs
    for j in range(len(liked_songs)): #go through the length of liked songs searching for the song
        if liked_songs.iloc[j, 3] == playlist.iloc[i, 0]:
            return j #returning the row the song is in in the liked songs df
        else:
            return 0 #check for a return value of 0 in the function that is calling this function
    return None


def artist_matcher(liked_songs, playlist, i, j): #if song isn't in liked, nothing to match
    # requirement that the two songs are exactly the same, use the same i and j as last helper function to check
    if liked_songs.iloc[j, 3] == playlist.iloc[i, 0]: #if the songs share the Spotify ID
        playlist.iat[i, 2] = liked_songs.iloc[j, 1] #make the artists match, this is for searching on youtube
    else:
        print(f"Unmatched songs at row {i} in playlist, row {j} in liked songs. Please advise!")
    return

"""

def check_sharing_and_append(liked_songs, playlist):
    # check playlist song by song and check to see if its in liked
    # if not in liked, append to the end of liked
    # check for sharing by Spotify ID
    for i in range(len(playlist)):
        j = find_shared_songs(liked_songs, playlist, i)
        if j is None: #playlist song is in liked songs
            continue

        if j == i:
            row = playlist.iloc[i]
            liked_songs = pd.concat([liked_songs, row.to_frame().T], ignore_index=True)

    return liked_songs





if __name__ == "__main__":
    # loop through all files in folder
    # use the updated liked songs master list for each new iteration for checking playlist

    playlist_filepaths = [
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\make_out_chilling_tuesday_late_night.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Brent_Faiyaz.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Chill.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Death_Grips.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Frank_Ocean.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\GHOST_.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Good_tiktok_songs.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Good_Times_(edit_using_songs_in_notes_and_delete_unliked_and_love_me_harder)(change_name_to_vibes).csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\JuiceWRLD.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\KDOT.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\laufey_.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Mixed.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Music_Recs_.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Nihon.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Old_But_Good.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\ONE_MONTH_.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\PEGGY_.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\rap.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Rick_and_Morty.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\The_Weeknd.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Tyler,_The_Creator.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Uhhhh_ok.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\Vickys_recommendations.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\violin.csv',
        r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Playlists\youd_be_surprised.csv'
    ]

    playlists = []
    for filepath in playlist_filepaths:
        playlist_X = setUp_individual_playlist(filepath)
        if playlist_X is None:
            print(f"Failure to create pandas dataframe from filepath: \n{filepath}\n")
            continue

        else:
            playlists.append(playlist_X)


    # LS is a dataframe of all the liked songs, to be updated after each playlist
    LS = sort_songs(r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Spotify_Liked_Songs.csv')
    check_empty(LS)

    liked_list_to_delete = ["Playlist name", "Type", "ISRC"]
    refined_LS = LS.drop(liked_list_to_delete, axis=1)

    #debugging
    # print("Refined liked songs:\n")
    # print(refined_LS.head())
    # print("\n")
    # print("playlist 1:\n")
    # print(playlists[0].head())
    # print("\n")
    # print(playlists[0].iloc[0, 0])
    # print("\n")
    # print(refined_LS.iloc[0, 3])
    # print("\n")
    # print(refined_LS.iloc[0:5, 3].values)
    # print("\n")
    # print(playlists[0].iloc[0, 0] in refined_LS.iloc[0:5, 3].values)
    # print("\n")
    #
    #
    # sample_df_data_1 = { #liked songs
    #     'Name' : ['Jack', 'Bob', 'Ron', 'Alice', 'Jessica', 'Becky'],
    #     'Age' : [12, 13, 14, 15, 16, 17]
    # }
    #
    # sample_df_data_2 = { #playlists
    #     'Age': [12, 13, 24, 25],
    #     'Name': ['Jack', 'Bob', 'Tom', 'Bella']
    # }
    #
    # df1 = pd.DataFrame(sample_df_data_1)
    # df2 = pd.DataFrame(sample_df_data_2)
    #
    # print(df1)
    # print(df2)
    #
    # for i in range(len(df2)):
    #
    #     print(df2.iloc[i, 1])
    #     print(df1.iloc[:, 0].values)
    #
    #     if df2.iloc[i, 1] in df1.iloc[:, 0].values:  # if subset name is in the list of names in the master list
    #         j = None  # so the new i can be passed in
    #     else:  # playlist song is not in liked songs, so append to liked songs
    #         j = i
    #
    #     if j is None: #playlist song is in liked songs
    #         print("j is None so go to next song")
    #         continue
    #
    #     if j == i:
    #         print("j is i, so its not in the main df")
    #         row = df2.iloc[i]
    #         df1 = pd.concat([df1, row.to_frame().T], ignore_index=True)
    #
    # print(df1)
    # print(df2)


    for i in range(len(playlists)):
        refined_LS = check_sharing_and_append(refined_LS, playlists[i])


    # print(playlists[13]), this is Nihon

    # maybe go throught the refined_LS and find non-english characters (not including (, [, and punc.)
    # dont count !
    # take all rows and make a new df for correcting
    # using the spotify ID, go back to the master list and replace the title, album, or artist with the correct info
    # correct info will be given by the user
    #   for me, most will come from Nihon
    # you can take all playlists, make a huge df and then search for the spotify ID and replace
    # the right characters are in the playlists df but not the main one

    # refined_LS.to_csv(r'C:\Users\Aaron A S Burgess\Desktop\Music Project\Master_Liked_Songs.csv', index=False)