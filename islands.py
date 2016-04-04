def true_coordinates_only(lst_of_lsts):
    """Given an n x m matrix, return the set of coordinates where the value is True:

    >>> true_coordinates_only([[True, False, True], [False, True, False], [True, False, True]]) == set([(0,0),(0,2),(1,1),(2,0),(2,2)])
    True

    """

    set_of_trues = set()

    for y in range(len(lst_of_lsts)):
        for x in range(len(lst_of_lsts[y])):
            if lst_of_lsts[y][x]:
                set_of_trues.add((y, x))

    return set_of_trues


def explore(coord, set_visited, set_true, n, m):
    """Recursive function to return all coordinates that comprise a contiguous island by the four cardinal directions"""

    # TODO - FOR REFACTORING, I WILL WRITE BASE CASE(S) FIRST AND CONSIDER HOW I CAN EXPLORE ALL COORDINATES WITHOUT VALIDATING TRUE COORDINATES FIRST.
    set_visited.add(coord)
    final_set = set([coord])

    y, x = coord
    north = None
    east = None
    south = None
    west = None

    # given a coordinate (y, x), get the coordinates north, east, south and west of the original
    if y - 1 >= 0:
        north = (y - 1, x)
    if x + 1 < m:
        east = (y, x + 1)
    if y + 1 < n:
        south = (y + 1, x)
    if x - 1 >= 0:
        west = (y, x - 1)

    # given the list of adjacent coordinates, determine which are valid, and if valid, check if in the True set
    island_coord_list = []

    for coordinate in [north, south, east, west]:
        if coordinate and coordinate in set_true and coordinate not in set_visited:
            island_coord_list.append(coordinate)

    # base case - return if no valid neighbors for current coordinate
    if not island_coord_list:
        return final_set

    # recursively add valid neighbors of any given island to the stack and return final set when all coordinates of any given island is found
    final_set |= set(island_coord_list)
    for pos in island_coord_list:
        island_continuation_from_neighbors = explore(pos, set_visited, set_true, n, m)
        final_set |= island_continuation_from_neighbors

    return final_set


def how_many_islands(lst_of_lsts):
    """Given an n x m matrix, return the number of islands in the matrix:

    >>> how_many_islands([[True, False, True], [False, True, False], [True, False, True]])
    5

    >>> how_many_islands([[False, True, False, True, False], [True, True, True, True, True], [False, False, False, False, False], [True, True, False, False, True], [False, True, False, True, True], [True, False, True, False, True]])
    5

    """

    island_list = []
    set_of_trues = true_coordinates_only(lst_of_lsts)
    set_of_visited = set()
    max_y = len(lst_of_lsts)
    if lst_of_lsts[0]:
        max_x = len(lst_of_lsts[0])

    for coordinate in list(set_of_trues):
        if coordinate not in set_of_visited:
            island_set = explore(coordinate, set_of_visited, set_of_trues, max_y, max_x)
            island_list.append(list(island_set))

    return len(island_list)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
