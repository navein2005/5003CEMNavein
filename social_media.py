# --- Step 1: Create the Person Entity Class (Q2.2) ---

class Person:
    """
    Represents a single user profile for the social media app.
    This is the 'Person domain / entity class'.

    Attributes:
        name (str): The user's display name.
        gender (str): The user's gender.
        biography (str): A short user profile bio.
        privacy (str): 'public' or 'private' to control profile visibility.
    """

    def __init__(self, name, gender, biography, privacy="public"):
        self.name = name
        self.gender = gender
        self.biography = biography
        self.privacy = privacy  # Default to 'public'

    def __str__(self):
        """A helper method to print the person's full profile details."""
        return (f"  Name: {self.name}\n"
                f"  Gender: {self.gender}\n"
                f"  Privacy: {self.privacy}\n"
                f"  Bio: {self.biography}")

    def get_name(self):
        """A simple getter for the name."""
        return self.name


# --- Step 2: Construct the Graph Data Structure (Q2.1) ---

class Graph:
    """
    Implements a generic, unweighted, directed graph using an Adjacency List.
    The vertices can be any hashable type (like a Person object).
    """

    def __init__(self):
        # self.adj_list is our adjacency list
        # It's a dictionary where:
        # Key = vertex
        # Value = list of adjacent vertices (outgoing edges)
        self.adj_list = {}

    def add_vertex(self, vertex):
        """
        Adds a new vertex to the graph.

        Args:
            vertex: The vertex object to be added.
        """
        # Check if the vertex is not already in the graph
        if vertex not in self.adj_list:
            # Add it to the dictionary with an empty list as its value
            self.adj_list[vertex] = []
            # print(f"Added vertex: {vertex.get_name()}")

    def add_edge(self, vertex_from, vertex_to):
        """
        Adds a new directed edge (from -> to) to the graph.

        Args:
            vertex_from: The vertex where the edge starts.
            vertex_to: The vertex where the edge ends.
        """
        # Check that both vertices exist in the graph first
        if vertex_from in self.adj_list and vertex_to in self.adj_list:
            # Add vertex_to to the list of vertex_from
            # This represents the "follows" relationship
            if vertex_to not in self.adj_list[vertex_from]:
                self.adj_list[vertex_from].append(vertex_to)
                # print(f"Added edge: {vertex_from.get_name()} -> {vertex_to.get_name()}")
        else:
            print("Error: One or both vertices not found in graph.")

    def list_outgoing_adjacent_vertex(self, vertex):
        """
        Lists all vertices that have an outgoing edge from the given vertex.

        Args:
            vertex: The vertex to check.

        Returns:
            list: A list of adjacent vertices, or an empty list if none.
        """
        if vertex in self.adj_list:
            # This is simple: just return the list of adjacent vertices
            return self.adj_list[vertex]
        else:
            print("Error: Vertex not found.")
            return []

    def get_all_vertices(self):
        """
        A helper method to get all vertices in the graph.

        Returns:
            list: A list of all vertex objects.
        """
        # The keys of our dictionary are all the vertices
        return list(self.adj_list.keys())


# --- Step 3: Create the Social Media App & CLI (Q2.3, Q2.4, Q2.5) ---

def find_followers(graph, user_to_find):
    """
    Helper function to find all followers of a specific user.
    This is for the mandatory feature Q2.5.d.

    We have to check every single vertex and see who *they* follow.

    Args:
        graph (Graph): The graph object.
        user_to_find (Person): The Person object we are looking for followers of.

    Returns:
        list: A list of Person objects who follow 'user_to_find'.
    """
    followers = []

    # Get a list of all users in the graph
    all_users = graph.get_all_vertices()

    for user in all_users:
        # Get the list of people this 'user' follows
        following_list = graph.list_outgoing_adjacent_vertex(user)

        # Check if 'user_to_find' is in that list
        if user_to_find in following_list:
            # If yes, then 'user' is a follower
            followers.append(user)

    return followers


def main_social_media():
    """
    The main function to run the Social Media App.
    """

    # 1. Create Graph object (Q2.4)
    social_graph = Graph()

    # 2. Create Person objects (Q2.3 - 5 people)
    print("--- Creating user profiles... ---")
    p1 = Person("Alice", "Female", "Software developer living in NY.", "public")
    p2 = Person("Bob", "Male", "Coffee enthusiast and blogger.", "public")
    p3 = Person("Charlie", "Male", "Student and part-time musician.", "private")
    p4 = Person("Diana", "Female", "Graphic designer and artist.", "public")
    p5 = Person("Evan", "Male", "Loves hiking and the outdoors.", "public")

    # Add all Person objects as vertices to the graph (Q2.1 - addVertex)
    users = [p1, p2, p3, p4, p5]
    for user in users:
        social_graph.add_vertex(user)
    print("User profiles created and added to graph.\n")

    # 3. Create "follows" connections (Q2.4 - addEdge)
    # Mimics Instagram: A can follow B, B doesn't have to follow A
    social_graph.add_edge(p1, p2)  # Alice follows Bob
    social_graph.add_edge(p1, p4)  # Alice follows Diana

    social_graph.add_edge(p2, p1)  # Bob follows Alice (mutual)
    social_graph.add_edge(p2, p3)  # Bob follows Charlie

    social_graph.add_edge(p3, p5)  # Charlie follows Evan

    social_graph.add_edge(p4, p1)  # Diana follows Alice
    social_graph.add_edge(p4, p2)  # Diana follows Bob
    social_graph.add_edge(p4, p5)  # Diana follows Evan

    social_graph.add_edge(p5, p1)  # Evan follows Alice

    # 4. Design the menu-driven program (Q2.5)
    while True:
        print("************************************************")
        print("  Welcome to SlowGram - Social Media App")
        print("************************************************")
        print("1. Display all users")
        print("2. View a user's profile details")
        print("3. View who a user follows (Following)")
        print("4. View a user's followers")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            # --- Q2.5.a: Display a list of all the users’ names ---
            print("\n--- All User Names ---")
            all_users = social_graph.get_all_vertices()
            for i, user in enumerate(all_users):
                print(f"{i + 1}.) {user.get_name()}")

        elif choice == '2':
            # --- Q2.5.b: View the profile of any one person in detail ---
            print("\n--- View Profile Details ---")
            all_users = social_graph.get_all_vertices()
            for i, user in enumerate(all_users):
                print(f"{i + 1}.) {user.get_name()}")

            try:
                user_idx = int(input(f"Select whose profile to view (1-{len(all_users)}): ")) - 1
                if 0 <= user_idx < len(all_users):
                    user_to_view = all_users[user_idx]
                    print(f"\n--- Profile for {user_to_view.get_name()} ---")
                    # We just use the __str__ method of the Person object
                    print(user_to_view)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '3':
            # --- Q2.5.c: View the list of followed accounts (Following) ---
            print("\n--- View Followed Accounts (Following) ---")
            all_users = social_graph.get_all_vertices()
            for i, user in enumerate(all_users):
                print(f"{i + 1}.) {user.get_name()}")

            try:
                user_idx = int(input(f"Select user (1-{len(all_users)}): ")) - 1
                if 0 <= user_idx < len(all_users):
                    user_to_check = all_users[user_idx]
                    print(f"\n--- {user_to_check.get_name()} is Following: ---")

                    # This uses the mandatory graph method
                    following_list = social_graph.list_outgoing_adjacent_vertex(user_to_check)

                    if not following_list:
                        print(f"{user_to_check.get_name()} is not following anyone.")
                    else:
                        for person in following_list:
                            print(f" - {person.get_name()}")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '4':
            # --- Q2.5.d: View the list of followers ---
            print("\n--- View Followers ---")
            all_users = social_graph.get_all_vertices()
            for i, user in enumerate(all_users):
                print(f"{i + 1}.) {user.get_name()}")

            try:
                user_idx = int(input(f"Select user (1-{len(all_users)}): ")) - 1
                if 0 <= user_idx < len(all_users):
                    user_to_find = all_users[user_idx]
                    print(f"\n--- Followers of {user_to_find.get_name()}: ---")

                    # Use our helper function
                    followers_list = find_followers(social_graph, user_to_find)

                    if not followers_list:
                        print(f"{user_to_find.get_name()} has no followers.")
                    else:
                        for person in followers_list:
                            print(f" - {person.get_name()}")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '5':
            print("\nExiting SlowGram. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1-5.")

        input("\nPress Enter to continue...")


# This standard Python line checks if the script is being run directly
# If so, it calls the main_social_media() function.
if __name__ == "__main__":
    main_social_media()