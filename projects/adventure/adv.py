from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/main_maze.txt"


# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = dict()


def mark_visited(room_id, direction=None, next_room_id=None):
    if room_id not in visited:
        visited[room_id] = {
            room_exit: None for room_exit in player.current_room.get_exits()}
    if direction is not None and next_room_id is not None:
        visited[room_id][direction] = next_room_id


def find_dead_end():
    reverse = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }

    while True:
        cur_room_id = player.current_room.id
        mark_visited(cur_room_id)
        exits = []
        for e in player.current_room.get_exits():
            if visited[cur_room_id][e] is None:
                exits.append(e)

        if len(exits) == 0:
            break

        prev_room_id = cur_room_id
        direction = random.choice(exits)
        player.travel(direction)
        traversal_path.append(direction)
        cur_room_id = player.current_room.id
        mark_visited(prev_room_id, direction, cur_room_id)
        mark_visited(cur_room_id, reverse[direction], prev_room_id)


def find_new_path():
    queue = Queue()
    cur_room_id = player.current_room.id
    breadth_visited = {cur_room_id}

    for direction, room in visited[cur_room_id].items():
        queue.enqueue([(room, direction)])

    while queue.size() > 0:
        cur_path = queue.dequeue()
        next_room = cur_path[-1][0]

        if None in visited[next_room].values():
            for room, direction in cur_path:
                traversal_path.append(direction)
                player.travel(direction)
            break

        for direction, room in visited[next_room].items():
            path_copy = cur_path.copy()
            if room not in breadth_visited:
                breadth_visited.add(room)
                path_copy.append((room, direction))
                queue.enqueue(path_copy)
        breadth_visited.add(next_room)


def traverse_map():
    while len(visited) < len(room_graph):
        find_dead_end()
        find_new_path()


# This allows for better traversal speeds
random.seed(345047)

traverse_map()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
