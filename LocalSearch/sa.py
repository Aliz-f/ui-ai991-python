from math import exp
from random import randint


def local_search(problem, turns_left, initial_temp=20, main_iteration=12, sub_iteration=9, alpha=0.6):
    '''
    local search using Simulated Anealing algorithm
    a new permutation is created in each iteration
    the permutation is evaluated and if it is of a greater
    value than the current permutation then it is substituted
    if it is not of a better value the substitution is happend
    with a possibility which depends on the current temprature
    and difference between the two permutation value
    '''
    temp = initial_temp
    current_soloution = problem.create_random_soloution(
        turns_left, initial=True)
    best_soloution = current_soloution

    for i in range(main_iteration):
        for j in range(sub_iteration):
            next_soloution = problem.create_random_soloution(
                turns_left, sol=current_soloution)
            delta = delta_E(current_soloution, next_soloution, turns_left)
            if delta <= 0:
                current_soloution = next_soloution
            else:
                # generate a random number for choosing weather to go to the next soloution or not
                random_number = randint(0, 1)

              # it goes to the next soloution only if the random number is above the possibility
                if random_number >= exp(-delta/temp):
                    current_soloution = next_soloution

            # update the best soloution ever found
            # if best_soloution['score'] < current_soloution['score']:
            #     if best_soloution['cost'] > current_soloution['cost']:
            if delta_E(current_soloution, best_soloution, turns_left) >= 0:
                best_soloution = current_soloution
        temp *= alpha
        print(best_soloution)

    return best_soloution


def delta_E(first_order, second_order, turns_left):
    '''
    the function which calculates the delta between cost
    of the two orders plus their collected scores
    '''
    first_value = first_order['score'] + \
        (turns_left/10 - first_order['cost']/10)
    second_value = second_order['score'] + \
        (turns_left/10 - second_order['cost']/10)
    return first_value - second_value
