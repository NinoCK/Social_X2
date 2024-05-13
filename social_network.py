import faker
import random
import operator
from graph import Graph

names = []
commentGraph = Graph()
followGraph = Graph()
likeGraph = Graph()
influenceGraph = Graph()

def calculate_influence(user_id1, user_id2):
    """
    Calculate the influence of user_id2 on user_id1 based on the number of likes and comments.

    Parameters:
    user_id1 (int): The ID of the user whose influence is being calculated.
    user_id2 (int): The ID of the user who is potentially influencing user_id1.

    Returns:
    float: The influence of user_id2 on user_id1.
    """
    likes, comments = 0, 0
    engagement_rate = calculate_engagement_rate(user_id1)
    comments = commentGraph.get_weight(user_id1, user_id2)
    likes = likeGraph.get_weight(user_id1, user_id2)
    if engagement_rate != 0:
        influence = (likes + comments) / engagement_rate
    else:
        influence = 0
    return influence

def calculate_engagement_rate(name):
    """
    Calculate the engagement rate for a given user.

    Parameters:
    name (str): The name of the user.

    Returns:
    float: The engagement rate of the user.
    """
    follows = followGraph.get_number_of_edges(name)
    comments = get_comments(name)
    likes = get_likes(name)
    if follows != 0:
        engagement_rate = (likes + comments) / follows
    else:
        engagement_rate = 0
    return engagement_rate

def calculate_highest_engagement_path(start, destination):
    """
    Calculates the path with the highest engagement in a social network graph.

    The path represents the sequence of nodes from the starting node to the destination node
    that maximizes the overall engagement, which is calculated based on the number of likes and comments.
    The total engagement is the sum of the engagement values of all nodes in the path.
    
    Args:
        start (str): The starting node of the path.
        destination (str): The destination node of the path.

    Returns:
        tuple: A tuple containing the path (list of nodes) and the total engagement (int) of the path.
    """
    total_engagement = 0
    current_node = start
    path = [current_node]
    while current_node != destination:
        neighbors = influenceGraph.get_edges(current_node)
        neighbor_engagement = {}
        for neighbor in neighbors:
            engagement = calculate_engagement_rate(neighbor)
            neighbor_engagement[neighbor] = engagement
        sorted_neighbors = sorted(neighbor_engagement.items(), key=operator.itemgetter(1), reverse=True)
        next_node = sorted_neighbors[0][0]
        next_engagement = sorted_neighbors[0][1]
        total_engagement += next_engagement
        path.append(next_node)
        current_node = next_node
    return path, total_engagement

def generate_influence_graph():
    """
    Generates an influence graph based on the social network data.

    This function iterates over each name in the social network and calculates the influence
    between each pair of names. The influence is determined by the number of likes and comments
    between the names. The influence graph is then populated with the calculated influence values.

    Returns:
        None
    """
    for name in names:
        for liked_name in likeGraph.get_edges(name):
            if name != liked_name:
                influence_likes = calculate_influence(name, liked_name)
                if liked_name not in commentGraph.get_edges(name):
                    influenceGraph.add_edge(name, liked_name, influence_likes)
                else:
                    for name_commented in commentGraph.get_edges(name):
                        influence_comments = calculate_influence(name, name_commented)
                        total_influence = influence_likes + influence_comments
                        influenceGraph.add_edge(name, name_commented, total_influence)

def generate_random_names():
    """
    Generates a list of random names and creates relationships between them in various graphs.

    This function uses the Faker library to generate random names. It creates a list of 10 random names
    and then adds these names to different graphs representing relationships in a social network.

    The function creates relationships such as likes, follows, and comments between the names in the graphs.
    The number of likes, follows, and comments are randomly generated for each name.

    Returns:
        None
    """
    fake = faker.Faker()
    for _ in range(10):
        names.append(fake.name())
    for name in names:
        commentGraph.add_vertex(name)
        followGraph.add_vertex(name)
        likeGraph.add_vertex(name)
        influenceGraph.add_vertex(name)
        total_likes = random.randint(0, len(names) - 1)
        total_likes_per_name = random.randint(1, 10)
        liked_names = random.choices(names, k=total_likes)
        for liked_name in liked_names:
            likeGraph.add_edge(name, liked_name, total_likes_per_name)
        total_follows = random.randint(0, len(names) - 1)
        names_followed = random.choices(names, k=total_follows)
        for followed_name in names_followed:
            followGraph.add_edge(name, followed_name)
        total_comments = random.randint(0, len(names) - 1)
        total_comments_per_name = random.randint(1, 10)
        commented_names = random.choices(names, k=total_comments)
        for name_commented in commented_names:
            commentGraph.add_edge(name, name_commented, total_comments_per_name)

def get_likes(name):
    """
    Calculates the total number of likes for a given name in the social network.

    Parameters:
        name (str): The name for which to calculate the total likes.

    Returns:
        int: The total number of likes for the given name.
    """
    total_likes = 0
    for edge in likeGraph.get_edges(name):
        total_likes += likeGraph.get_weight(name, edge)
    return total_likes

def get_comments(name):
    """
    Get the total number of comments made by a user.

    Args:
        name (str): The name of the user.

    Returns:
        int: The total number of comments made by the user.
    """
    total_comments = 0
    for edge in commentGraph.get_edges(name):
        total_comments += commentGraph.get_weight(name, edge)
    return total_comments

def total_stats_display():
    """
    Display the total likes, follows, and comments for each user in the social network.

    This function iterates over the list of names and prints the total likes, follows, and comments
    for each user. It uses the `get_likes` and `get_comments` functions to retrieve the total likes
    and comments for each user, and the `get_edges` function from the `followGraph` object to get the
    total number of follows for each user.

    Args:
        None

    Returns:
        None
    """
    print("\nLikes, Comments, and Follows\n")
    for name in names:
        print(f"{name}\n")
        names_followed = followGraph.get_edges(name)
        print(f"Total Likes: {get_likes(name)}")
        print(f"Total Follows: {len(names_followed)}")
        print(f"Total Comments: {get_comments(name)}\n")

def influency_display():
    """
    Display the influence graph and weights for each edge.

    This function generates the influence graph and prints the influence weights
    for each edge in the graph. It iterates over each name in the 'names' list
    and prints the name followed by the edges and their corresponding weights.
    """
    generate_influence_graph()
    print("\nInfluence")
    for name in names:
        print(f"{name}:")
        for edge in influenceGraph.get_edges(name):
            print(f"{edge}: {influenceGraph.get_weight(name, edge):.2f}")
        print()

def engagement_rate_display():
    """
    Display the engagement rate for each name in the names list.
    """
    print("\nEngagement rate")
    for name in names:
        engagement_rate = calculate_engagement_rate(name)
        print(f"{name}: {engagement_rate:.2f}")

def get_start_and_destination():
    """
    Prompts the user to enter the starting and destination names.

    Returns:
        tuple: A tuple containing the starting name and destination name entered by the user.
    """
    start = str(input("Enter the starting name: "))
    destination = str(input("Enter the destination name: "))
    return start, destination

def shortest_follow_path_display():
    """
    Finds the shortest path between two vertices in the followGraph and displays it.

    This function prompts the user to enter the start and destination vertices.
    It then checks if both vertices exist in the followGraph.
    If either of the vertices does not exist, it prints an error message and returns.
    Otherwise, it performs a breadth-first search (BFS) on the followGraph starting from the start vertex.
    Finally, it prints the shortest path between the start and destination vertices.

    Returns:
        None
    """
    start, destination = get_start_and_destination()
    if start not in followGraph.vertices or destination not in followGraph.vertices:
        print("One or both of the entered names do not exist in the graph. Please try again.")
        return
    followGraph.bfs(start)
    followGraph.print_shortest_path(start, destination)
    print(f"{followGraph.path}\n")

def shortest_like_path_display():
    """
    Finds and displays the shortest path between two vertices in the likeGraph.

    This function prompts the user to enter the start and destination vertices.
    It then checks if both vertices exist in the likeGraph. If not, it prints an error message and returns.
    If both vertices exist, it performs a breadth-first search (BFS) on the likeGraph starting from the start vertex.
    Finally, it prints the shortest path between the start and destination vertices.

    Note: The likeGraph object must be defined and initialized before calling this function.

    Returns:
        None
    """
    start, destination = get_start_and_destination()
    if start not in likeGraph.vertices or destination not in likeGraph.vertices:
        print("One or both of the entered names do not exist in the graph. Please try again.")
        return
    likeGraph.bfs(start)
    likeGraph.print_shortest_path(start, destination)
    print(f"{likeGraph.path}\n")

def shortest_comment_path_display():
    """
    Finds and displays the shortest path between two users in a comment graph.

    This function prompts the user to enter the start and destination users, then uses a breadth-first search algorithm
    to find the shortest path between them in the comment graph. If either the start or destination user does not exist
    in the graph, an error message is displayed. Otherwise, the shortest path is printed.

    Parameters:
        None

    Returns:
        None
    """
    start, destination = get_start_and_destination()
    commentGraph.bfs(start)
    if start not in commentGraph.vertices or destination not in commentGraph.vertices:
        print("One or both of the entered names do not exist in the graph. Please try again.")
        return
    commentGraph.print_shortest_path(start, destination)
    print(f"{commentGraph.path}\n")

def display_engagement_path_for_follows():
    """
    Displays the engagement path for follows.

    This function prompts the user to enter a start and destination node,
    then uses Dijkstra's algorithm to find the shortest path between the two nodes
    in the followGraph. Finally, it prints the shortest path and the path's engagement.

    Parameters:
        None

    Returns:
        None
    """
    start, destination = get_start_and_destination()
    followGraph.dijkstra(start)
    followGraph.print_shortest_path(start, destination)
    print(f"{followGraph.path}\n")

def display_engagement_path_for_likes():
    """
    Displays the engagement path for likes in the social network.

    This function prompts the user to enter a start and destination node, and then uses Dijkstra's algorithm to find the shortest path between them in the likeGraph. It then prints the shortest path and the path itself.

    Parameters:
        None

    Returns:
        None
    """
    start, destination = get_start_and_destination()
    likeGraph.dijkstra(start)
    likeGraph.print_shortest_path(start, destination)
    print(f"{likeGraph.path}\n")

def display_engagement_path_for_comments():
    """
    Displays the engagement path for comments in the social network.

    This function prompts the user to enter the start and destination nodes for the engagement path.
    It then uses Dijkstra's algorithm to find the shortest path between the start and destination nodes in the commentGraph.
    Finally, it prints the shortest path and the path itself.

    Parameters:
    None

    Returns:
    None
    """
    start, destination = get_start_and_destination()
    commentGraph.dijkstra(start)
    commentGraph.print_shortest_path(start, destination)
    print(f"\n{commentGraph.path}\n")

def main_menu():
    while True:
        print("\nMain Menu\n")
        print("1. Display all likes,follows and comments")
        print("2. Display Influence")
        print("3. Display Engagement Rate")
        print("4. Find Highest Engagement Path")
        print("5. Display Shortest Paths")
        print("0. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1": total_stats_display()
        elif choice == "2": influency_display()
        elif choice == "3": engagement_rate_display()
        elif choice == "4": engagement_path_display()
        elif choice == "5": shortest_path_display()
        elif choice == "0": break
        else: print("Invalid choice. Please try again.\n")

def engagement_path_display():
    while True:
        print("Engagement Path\n")
        print("1. Engagement Path for Likes")
        print("2. Engagement Path for Follows")
        print("3. Engagement Path for Comments")
        print("4. Go back to Main Menu")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            likeGraph.display_edges()
            display_engagement_path_for_likes()
        elif choice == "2":
            followGraph.display_edges()
            display_engagement_path_for_follows()
        elif choice == "3":
            commentGraph.display_edges()
            display_engagement_path_for_comments()
        elif choice == "4": main_menu()
        else: print("Invalid choice. Please try again.")

def shortest_path_display():
    while True:
        print("Shortest Paths Menu\n")
        print("1. Display Shortest Paths for Likes")
        print("2. Display Shortest Paths for Follows")
        print("3. Display Shortest Paths for Comments")
        print("4. Go back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            likeGraph.display_edges()
            shortest_like_path_display()
        elif choice == "2":
            followGraph.display_edges()
            shortest_follow_path_display()
        elif choice == "3":
            commentGraph.display_edges()
            shortest_comment_path_display()
        elif choice == "4": main_menu()
        else: print("Invalid choice. Please try again.")

def main():
    generate_random_names()
    main_menu()

if __name__ == "__main__":
    main()