from collections import defaultdict

from utils.input import read_file


class Vertex:
    def __init__(self, name):
        self.name = name
        self.is_large = (name.lower() != name)
        self.edges = []


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []
        self.start = None
        self.end = None

    def add_edge(self, start, end):
        start_vertex = self.vertices.get(start)
        if not start_vertex:
            start_vertex = Vertex(start)
            self.vertices[start] = start_vertex
        end_vertex = self.vertices.get(end)
        if not end_vertex:
            end_vertex = Vertex(end)
            self.vertices[end] = end_vertex
        if not self.start:
            if start.lower() == "start":
                self.start = start_vertex
            if end.lower() == "start":
                self.start = end_vertex
        if not self.end:
            if start.lower() == "end":
                self.end = start_vertex
            if end.lower() == "end":
                self.end = end_vertex
        self.edges.append((start_vertex, end_vertex))
        start_vertex.edges.append(end_vertex)
        end_vertex.edges.append(start_vertex)


def parse_input(lines):
    cave = Graph()
    for line in lines:
        pts = line.split("-")
        cave.add_edge(pts[0], pts[1])
    return cave


def traverse_cave(graph):
    q = [[graph.start]]
    total = 0
    while len(q) != 0:
        path = q.pop(0)
        curr = path[-1]
        if curr == graph.end:
            total += 1
            continue
        if not curr.is_large and curr in path[:-1]:
            continue
        for e in curr.edges:
            new_path = path.copy()
            new_path.append(e)
            q.append(new_path)
    return total


def part_1():
    lines = read_file("input.txt")
    graph = parse_input(lines)
    total = traverse_cave(graph)
    print(total)


def has_duplicate(path):
    str_path = [v.name for v in path if not v.is_large]
    return len(set(str_path)) != len(str_path)


def traverse_cave_2(graph):
    q = [[graph.start]]
    total = 0
    while len(q) != 0:
        path = q.pop(0)
        curr = path[-1]
        if curr == graph.end:
            total += 1
            continue
        if not curr.is_large and curr in path[:-1]:
            if has_duplicate(path[:-1]):
                continue
        if curr == graph.start and len(path) > 1:
            continue
        for e in curr.edges:
            new_path = path.copy()
            new_path.append(e)
            q.append(new_path)
    return total


def part_2():
    lines = read_file("input.txt")
    graph = parse_input(lines)
    total = traverse_cave_2(graph)
    print(total)


if __name__ == "__main__":
    part_2()
