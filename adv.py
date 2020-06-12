from room import Room
from player import Player
from world import World

from collections import deque
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
# print(player.current_room.id)



# Fill this out with directions to walk
# traversal_path = ['n', 'n']--------------------------------------------------

### Helpers ###
def graph_entry(directions_list):
    new_entry = {
        "n": None,
        "e": None,
        "s": None,
        "w": None
    }
    for dir in directions_list:
        new_entry[dir] = dir

    return new_entry
### End Helpers ###

traversal_path = []

rooms_graph = dict()
visited = set() # track nodes that are visited

# dict used to create reverse directions for backtracking
reverse_directions = {
    "n": "s",
    "e": "w",
    "s": "n",
    "w": "e"
}

backtrack_route_stack = deque() 
# this ^^^ will be used to keep track of the path for backtracking, every move forward in an unexplored node will add the oppopsite direction to the stack. If the current room does not have any explored paths, it will pop this direction off and move backwards until there is a new adjacent room to explore. This will g



while len(visited) < len(world.rooms):
    paths = player.current_room.get_exits() # This returns an array of string directions
    room_id = player.current_room.id # variable for readability
    if room_id not in visited: # adding the current room to the visited
        visited.add(room_id)

    if room_id not in rooms_graph:
        rooms_graph[room_id] = graph_entry(paths) # Creates default dict set up for the room
        for next_room in paths: 
            # iterating over the possible exits, and assigning the value of that direction in the dict value of room_id to the room_id of the next room
            rooms_graph[room_id][next_room] = player.current_room.get_room_in_direction(next_room).id

    unexplored_route = None # If a path from the current room is unexplored, this will hold the direction

    for dir in rooms_graph[room_id]:
        if rooms_graph[room_id][dir] is not None and rooms_graph[room_id][dir] not in visited:
            unexplored_route = dir # assigns a direction to move to an existing and un-explored room.

    # traverse
    if unexplored_route is None: # start backtracking
        backtrack_route = backtrack_route_stack.pop() # grab the backtracking direction
        traversal_path.append(backtrack_route) 
        player.travel(backtrack_route)
        
    else: # move to unexplored room
        traversal_path.append(unexplored_route)
        backtrack_route_stack.append(reverse_directions[unexplored_route]) # add the reverse of the direction moved to the backtrack_route_stack
        player.travel(unexplored_route)



#























# TRAVERSAL TEST - DO NOT MODIFY -----------------------------------------------------
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
