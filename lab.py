#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for lab 2 will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).


def acted_together(data, actor_id_1, actor_id_2):
    """

    Parameters
    ----------
    data : a list of tuples, with the format (actor1_id, actor2_id, movie_id)
    actor_id_1 : an id corresponding to a specific actor.
    actor_id_2 : an id corresponding to another actor.

    Returns
    -------
    bool
        returns True if actor_id_1 and actor_id_2 are both in a movie together
        as seen in data. returns False otherwise.

    """
    for movie in data:
        if movie[0] == actor_id_1 or movie[1] == actor_id_1:
            if actor_id_2 == movie[0] or actor_id_2 == movie[1]:
                return True
    return False

def actors_with_bacon_number(data, n):
    """
    Parameters
    ----------
    data : a list of tuples, with the format (actor1_id, actor2_id, movie_id)
    n : the bacon number of the actors we are finding

    Returns
    -------
    prev_level : returns a set of all of the actors at the bacon level n
    """
    seen = set([4724])
    prev_level = set([4724])
    bacon_level = set()
    for i in range(n):
        for movie in data:
            actor1 = movie[0]
            actor2 = movie[1]
            if actor1 in prev_level:
                if actor2 not in seen:
                    bacon_level.add(actor2)
                    seen.add(actor2)
            elif actor2 in prev_level:
                if actor1 not in seen:
                    bacon_level.add(actor1)
                    seen.add(actor1)
        prev_level= bacon_level.copy()
        bacon_level = set()
        if len(prev_level) == 0:
            break
    return prev_level
                


def bacon_path(data, actor_id):
    return actor_to_actor_path(data, 4724, actor_id)
        
def convert_data_to_dict(data):
    data_dict = {}
    for movie in data:
        actor1_id = movie[0]
        actor2_id = movie[1]
        if actor1_id in data_dict:
            data_dict[actor1_id].add(actor2_id)
        else:
            data_dict[actor1_id] = set([actor2_id])
        if actor2_id in data_dict:
            data_dict[actor2_id].add(actor1_id)
        else:
            data_dict[actor2_id] = set([actor1_id])
    return data_dict

def actor_to_actor_path(data, actor_id_1, actor_id_2):
    data_dict = convert_data_to_dict(data)
    linked_list_seen = {}
    found_path = False
    queue = {"oldest": 0, "newest": 0, 0: actor_id_1}
    while not found_path:
        if len(queue) == 2:
            return None
        oldest_id = queue[queue["oldest"]]
        if oldest_id != actor_id_2:
            for connection in data_dict[oldest_id]:
                if connection not in linked_list_seen:
                    next_avail_pos = queue["newest"] + 1
                    queue['newest'] += 1
                    queue[next_avail_pos] = connection
                    linked_list_seen[connection] = oldest_id
            del queue[queue["oldest"]]
            queue["oldest"] += 1
        else:
            found_path = True
    output_path = []
    added_id = actor_id_2
    while added_id != actor_id_1:
        output_path = [added_id] + output_path
        added_id = linked_list_seen[added_id]
    return [actor_id_1] + output_path

def build_actors_movie_dictionary(data):
    actor_movies = {}
    for movie in data:
        actor1_id = movie[0]
        actor2_id = movie[1]
        movie_id = movie[2]
        if actor1_id in actor_movies:
            actor_movies[actor1_id].add(movie_id)
        else:
            actor_movies[actor1_id] = set([movie_id])
        if actor2_id in actor_movies:
            actor_movies[actor2_id].add(movie_id)
        else:
            actor_movies[actor2_id] = set([movie_id])
    return actor_movies

def movie_path(data, actor_id_1, actor_id_2):
    my_path = actor_to_actor_path(data, actor_id_1, actor_id_2)
    actor_movies = build_actors_movie_dictionary(data)
    out_path = []
    with open('resources/movies.pickle', 'rb') as f:
        movie_data = pickle.load(f)
    for i in range(len(my_path) - 1):
        actor1_movies = actor_movies[my_path[i]]
        actor2_movies = actor_movies[my_path[i + 1]]
        movie_id = 0
        for movie in actor1_movies:
            if movie in actor2_movies:
                movie_id = movie
                break
        for m_name, m_id in movie_data.items():
            if movie_id == m_id:
                out_path.append(m_name)
                break
    return out_path

def actor_path(data, actor_id_1, goal_test_function):
    with open('resources/names.pickle', 'rb') as f:
        names = pickle.load(f)
    valid_actors = []
    for actor_id in names.values():
        if goal_test_function(actor_id):
            valid_actors.append(actor_id)
    if len(valid_actors) == len(names):
        return [actor_id_1]
    if len(valid_actors) == 0:
        return None
    best_path = []
    for actor in valid_actors:
        my_path = actor_to_actor_path(data, actor_id_1, actor)
        if len(best_path) == 0 or len(my_path) < len(best_path):
            best_path = my_path
    return best_path

def actors_connecting_films(data, film1, film2):
    actor_1_id = 0
    actor_2_id = 0
    actor_3_id = 0
    actor_4_id = 0
    for movie in data:
        if movie[2] == film1:
            actor_1_id = movie[0]
            actor_2_id = movie[1]
        elif movie[2] == film2:
            actor_3_id = movie[0]
            actor_4_id = movie[1]
    path1 = actor_to_actor_path(data, actor_1_id, actor_3_id)
    path2 = actor_to_actor_path(data, actor_1_id, actor_4_id)
    path3 = actor_to_actor_path(data, actor_2_id, actor_3_id)
    path4 = actor_to_actor_path(data, actor_2_id, actor_4_id)
    paths = [path1, path2, path3, path4]
    valid_paths = []
    for i in range(4):
        if paths[i] != None:
            valid_paths.append(paths[i])
    if len(valid_paths) == 0:
        return None
    min_path = []
    for path in valid_paths:
        if len(min_path) == 0 or len(path) < len(min_path):
            min_path = path
    return min_path
    
    
if __name__ == '__main__':
    # with open('resources/small.pickle', 'rb') as f:
    #     smalldb = pickle.load(f)
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    
    
    with open('resources/large.pickle', 'rb') as f:
        large = pickle.load(f)
    for movie in large:
        if movie[2] == 142416:
            print(movie[0],movie[1])
    # print(actors_connecting_films(large, 142416, 44521))
  