from graph import Graph  # These may come in handy


def earliest_ancestor(ancestors, starting_node):

    graph = Graph()

    for edge in ancestors:
        graph.add_vertex(edge[0])
        graph.add_vertex(edge[1])

    for edge in ancestors:
        graph.add_edge(edge[1], edge[0])

    graph.dft_recursive(starting_node)

    ancestors_set = graph.dft_recursive_ancestors(starting_node)
    if ancestors_set[1] == 0:
        return -1
    ancestors_list = list(ancestors_set[0])
    ancestors_list.sort()

    return ancestors_list[0]
