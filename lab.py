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
    return prev_level
                


def bacon_path(data, actor_id):
    raise NotImplementedError("Implement me!")


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")


def actor_path(data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == '__main__':
    with open('resources/small.pickle', 'rb') as f:
        smalldb = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    # with open('resources/names.pickle','rb') as f:
    #     names = pickle.load(f)
    # print(names['Kevin Bacon'])
    # for name, id_num in names.items():
    #     if id_num == 1033185:
    #         print(name)
    #         break
    with open('resources/large.pickle','rb') as f:
        large = pickle.load(f)
  
    print(actors_with_bacon_number(large, 6))
  