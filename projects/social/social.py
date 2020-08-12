from random import *
from util import Stack, Queue  # These may come in handy


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        print(user_id)
        print(friend_id)
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        if num_users <= avg_friendships:
            return
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        # Add users
        users_array = []
        for i in range(1, num_users+1):
            users_array.append(i)
            self.add_user(i)

        # Create friendships
        everyone_needs_a_friend_array = users_array
        shuffle(everyone_needs_a_friend_array)

        # friendships_dict = {}
        for i in range(0, num_users-1, 2):
            friendship = [everyone_needs_a_friend_array[i],
                          everyone_needs_a_friend_array[i+1]]
            friendship.sort()
            self.add_friendship(friendship[0], friendship[1])
            # friendships_dict[f"{friendship[0]},{friendship[1]}"] = "yay"

        i = 1
        while i <= num_users*(avg_friendships-1)-1:
            user = randint(1, num_users)
            friend = randint(1, num_users)
            if user != friend and friend not in self.friendships[user]:
                self.add_friendship(user, friend)
                i += 1

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        queue = Queue()
        queue.enqueue([user_id])

        while queue.size() > 0:
            path = queue.dequeue()
            visiting = path[-1]

            if visiting not in visited:
                visited[visiting] = path
                for next_visiting in self.friendships[visiting]:
                    path_copy = list(path)
                    path_copy.append(next_visiting)
                    queue.enqueue(path_copy)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
