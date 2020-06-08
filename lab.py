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

def movie_path(data, movie_data, actor_id_1, actor_id_2):
    my_path = actor_to_actor_path(data, actor_id_1, actor_id_2)
    actor_movies = build_actors_movie_dictionary(data)
    out_path = []
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
    raise NotImplementedError("Implement me!")


def actors_connecting_films(data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == '__main__':
    # with open('resources/small.pickle', 'rb') as f:
    #     smalldb = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    
    with open('resources/movies.pickle', 'rb') as f:
        movies = pickle.load(f)
    with open('resources/large.pickle', 'rb') as f:
        large = pickle.load(f)
    with open('resources/names.pickle', 'rb') as f:
        names = pickle.load(f)
    for name, m_id in names.items():
        if name == "Steve Guttenberg":
            print("Steve", m_id)
        if name == "Iva Ilakovac":
            print("Iva", m_id)
    
        
    print(movie_path(large, movies, 26472, 1345462))
  