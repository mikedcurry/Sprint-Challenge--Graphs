from room import Room
from player import Player
from world import World

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
# world.print_rooms()
player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

# traversal_path = []
graph = {}

# intialize the graph with the first room having ?'s
graph[player.current_room.id] = {}
for exit in player.current_room.get_exits():
    graph[player.current_room.id][exit] = "?"


def restart():
    global player 
    global traversal_path
    global graph
    # Print an ASCII map
    # world.print_rooms()
    player = Player(world.starting_room)

    # Fill this out with directions to walk
    traversal_path = []

    # Reset graph to nothing...
    graph = {}

    # intialize the graph with the first room having ?'s
    graph[player.current_room.id] = {}
    for exit in player.current_room.get_exits():
        graph[player.current_room.id][exit] = "?"





# Probably going to need these...
# class Stack():
#     def __init__(self):
#         self.stack = []
#     def push(self, value):
#         self.stack.append(value)
#     def pop(self):
#         if self.size() > 0:
#             return self.stack.pop()
#         else:
#             return None
#     def size(self):
#         return len(self.stack)

# class Queue():
#     def __init__(self):
#         self.queue = []
#     def enqueue(self, value):
#         self.queue.append(value)
#     def dequeue(self):
#         if self.size() > 0:
#             return self.queue.pop(0)
#         else:
#             return None
#     def size(self):
#         return len(self.queue)




# print('initial graph:', graph)

def get_new_direction():
    unexplored = []
    exits = player.current_room.get_exits()
    if exits:
        for exit in exits:
            if graph[player.current_room.id][exit] == "?":
                unexplored.append(exit)
        if len(unexplored):
            random.shuffle(unexplored)
            # print(unexplored[-1])
            return unexplored[-1]
    else:
        return None

#                                        #
#      017       002       014           #
#       |         |         |            #
#       |         |         |            #
#      016--015--001--012--013           #
#                 |                      #
#                 |                      #
#      008--007--000--003--004           #
#       |         |                      #
#       |         |                      #
#      009       005                     #
#       |         |                      #
#       |         |                      #
#      010--011--006                     #
#                                        #

def converse(dir):
    if dir == 'n':
        return 's'
    elif dir == 's':
        return 'n'
    elif dir == 'w':
        return 'e'
    elif dir == 'e':
        return 'w'

# random.seed(1)

def walk_maze():
    visited = [0]
    bread_crumbs = []
    # count = 0
    
    while len(visited) < len(room_graph):
        
        while get_new_direction():
            # go a new direction!
            previous = player.current_room.id
            new_direction = get_new_direction()
            player.travel(new_direction)
            traversal_path.append(new_direction)
            bread_crumbs.append(new_direction)
            # print(bread_crumbs)
            
            if player.current_room.id not in visited:
                visited.append(player.current_room.id)
                # print(visited, len(visited)) ##

                graph[player.current_room.id] = {}
                for exit in player.current_room.get_exits():
                    graph[player.current_room.id][exit] = "?"

            graph[previous][new_direction] = player.current_room.id
            graph[player.current_room.id][converse(new_direction)] = previous
            # count += 1
            # print(f'graph at {count} step', graph)
        
        # Dead End ...
        while len(bread_crumbs) and get_new_direction() == None:
            if len(visited) == len(room_graph):
                break
            player.travel(converse(bread_crumbs[-1]))
            traversal_path.append(converse(bread_crumbs[-1]))
            bread_crumbs.pop()
            
 
        # print(traversal_path) ##

# Do The Thing
# walk_maze()
# print(len(traversal_path))


# How'd I do?
# print("traversal_path", traversal_path)



# Iterating through random seeds to find smallest possible route...

def find_shortest(start=0, record=991):
    seed = start
    random.seed(seed)
    walk_maze()
    # print(seed, len(traversal_path))
    records =[(seed, record)]

    try:
        while True: #len(traversal_path) >= records[-1]:
            seed += 1
            random.seed(seed)

            restart()
            walk_maze()

            # print(seed, len(traversal_path))
            if len(traversal_path) < records[-1][1]:
                records = [*records, (seed, len(traversal_path))]
                print(records)

    except KeyboardInterrupt:
        print(seed)
        pass
    # return print(seed, len(traversal_path))
 

find_shortest(0)


# random.seed(3)
# walk_maze()
# print(len(traversal_path))




# # TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



# #######
# # UNCOMMENT TO WALK AROUND
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
