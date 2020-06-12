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

# accepts the visited set starting node of the search 

def bfs_nearest_open_node(visited, starting_node):
    # Create a node_que for a BFT search
    node_que = deque()
    node_que.append([starting_node])

    dir_path_que = deque() # to track the directions taken

    bfs_visited = set()

    while len(node_que) > 0:
        # preventing an error from .popleft() if dir_path is empty
        if len(dir_path_que) <= 0:
            current_dir_path = []
        else:
            current_dir_path = dir_path_que.popleft() # tracking the direction path

        current_node_path = node_que.popleft()
        current_node = current_node_path[-1]
        
        bfs_visited.add(current_node.id)

        if len(current_node.get_exits()) > 0:
            for next_node_dir in current_node.get_exits(): # ex [ "n", "s"]
                next_node = current_node.get_room_in_direction(next_node_dir)

                if next_node.id not in visited: # search is complete
                    return [*current_dir_path, next_node_dir]
                
                elif next_node.id not in bfs_visited:
                    dir_path_que.append([*current_dir_path, next_node_dir])
                    node_que.append([*current_node_path, next_node])
                    
        else:
            print(current_dir_path)
            return current_dir_path
### End Helpers ###

traversal_path = []

rooms_graph = dict()
visited = set() # track nodes that are visited


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
    if unexplored_route is not None: # move to unexplored room
        traversal_path.append(unexplored_route)
        player.travel(unexplored_route)
        
    else: # start backtracking
        # pathfinding will = either None or an array of directions to the next unexplored froom
        pathfinding = bfs_nearest_open_node(visited, player.current_room)

        if pathfinding is not None:
            print("PATHFINDING", pathfinding)
            for dir in pathfinding:
                print(dir)
                traversal_path.append(dir)
                player.travel(dir)
                visited.add(player.current_room.id)
























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
