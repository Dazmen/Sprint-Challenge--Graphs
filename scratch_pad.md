 ### PLANNING ###
 # TOOLS
    - 100% use DFT
    - the player class has a get_exits method
        - This gives information about adjacent rooms
        - It returns an array of letters representing cardinal directions

### First Steps
    - just get a first pass working !

# QUESTIONS
    - Can we programatically analayze the map layout beforehand?
        - If yes this might allow me to make optimizations to the travesal algorithm

    - If I can read the map before travesing, what would I like to do?
        - Is there a way to gather the "clusters" that are only connected to the rest
            of the map by one node?
            - The travesal algorithm could take these into account by making sure to clear the entire "cluster" before moving on, might help minimize backtracking
        - could also mark the longest "stretch" of single nodes to traverse last to minimize steps

