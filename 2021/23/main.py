import heapq

from utils.input import read_file


def parse_input(lines):
    ret = []
    for line in lines:
        on = False
        parts = line.split()
        if parts[0] == "on":
            on = True
        xyz = parts[1].split(",")
        xyzs = []
        for x in xyz:
            ab = x.split("=")[1].split("..")
            ij = [int(ab[0]), int(ab[1])]
            xyzs.append(ij)
        ret.append((on, xyzs))
    return ret


letter_to_room_index = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3
}

room_to_letter = {
    0: "A",
    1: "B",
    2: "C",
    3: "D"
}

letter_to_score = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


class State:
    def __init__(self, rooms, hallways, alcoves, score):
        self.rooms = rooms
        self.hallways = hallways
        self.alcoves = alcoves
        self.score = score

    def __lt__(self, other):
        # Needed for heapq I guess.
        return False

    def can_reach_room(self, source, dest):
        min_pos = min(source, dest)
        max_pos = max(source, dest)
        for i in range(min_pos, max_pos):
            if self.hallways[i] is not None:
                return False
        return True

    def can_enter_room(self, source, dest):
        room = self.rooms[dest]
        dest_letter = room_to_letter[dest]
        for i in range(len(room)):
            if room[i] is not None and room[i] != dest_letter:
                return False
        if not self.can_reach_room(source, dest):
            return False
        return True

    def can_enter_room_from_hallway(self, source, dest):
        room = self.rooms[dest]
        dest_letter = room_to_letter[dest]
        for i in range(len(room)):
            if room[i] is not None and room[i] != dest_letter:
                return False
        if source < dest:
            for i in range(source + 1, dest):
                if self.hallways[i] is not None:
                    return False
            return True
        elif source > dest:
            for i in range(dest, source):
                if self.hallways[i] is not None:
                    return False
            return True
        # source == dest is easy
        return True

    def can_enter_room_from_alcove(self, source, dest):
        room = self.rooms[dest]
        dest_letter = room_to_letter[dest]
        for i in range(len(room)):
            if room[i] is not None and room[i] != dest_letter:
                return False
        if source == 0:
            for i in range(dest):
                if self.hallways[i] is not None:
                    return False
            return True
        else:
            for i in range(dest, len(self.hallways)):
                if self.hallways[i] is not None:
                    return False
            return True

    def can_reach_hallway(self, source, dest):
        """
        :param source: A room number
        :param dest: A hallway number or "left" or "right
        :return:
        """

        if source <= dest:
            for i in range(source, dest + 1):
                if self.hallways[i] is not None:
                    return False
            return True
        for i in range(dest, source):
            if self.hallways[i] is not None:
                return False
        return True

    def can_reach_alcove(self, source, dest):
        if self.alcoves[dest][0] is not None:
            return False
        if dest == 0:
            for i in range(0, source):
                if self.hallways[i] is not None:
                    return False
            return True
        else:
            for i in range(source, len(self.hallways)):
                if self.hallways[i] is not None:
                    return False
            return True

    def generate_valid_states(self):
        ret = []
        # Leaving a hallway -> room
        for i, hallway in enumerate(self.hallways):
            if hallway is None:
                continue
            dest = letter_to_room_index[hallway]
            if not self.can_enter_room_from_hallway(i, dest):
                continue
            moves = 1 + abs((i * 2 + 1) - (dest * 2))
            new_room = self.rooms[dest].copy()
            for a in range(len(new_room) - 1, -1, -1):
                if new_room[a] is None:
                    moves += a
                    new_room[a] = hallway
                    break
            new_rooms = self.rooms.copy()
            new_rooms[dest] = new_room
            new_hallways = self.hallways.copy()
            new_hallways[i] = None
            new_score = self.score + (letter_to_score[hallway] * moves)
            new_state = State(new_rooms, new_hallways, self.alcoves, new_score)
            ret.append(new_state)
            # Greedy - this is the most optimal move there is
            return ret

        # Alcove => Room
        for i, alcove in enumerate(self.alcoves):
            if alcove[0] is not None:
                letter = alcove[0]
                index = 0
            elif alcove[1] is not None:
                letter = alcove[1]
                index = 1
            else:
                continue
            # Find destination room
            dest = letter_to_room_index[letter]
            if self.can_enter_room_from_alcove(i, dest):
                if i == 0:
                    moves = index + 1 + (dest * 2) + 1
                else:
                    moves = index + 1 + ((3 - dest) * 2) + 1
                new_room = self.rooms[dest].copy()
                for a in range(len(new_room) - 1, -1, -1):
                    if new_room[a] is None:
                        moves += a
                        new_room[a] = letter
                        break
                new_rooms = self.rooms.copy()
                new_rooms[dest] = new_room
                new_alcoves = self.alcoves.copy()
                new_alcove = alcove.copy()
                new_alcove[index] = None
                new_alcoves[i] = new_alcove
                new_score = self.score + (letter_to_score[letter] * moves)
                new_state = State(new_rooms, self.hallways, new_alcoves, new_score)
                ret.append(new_state)
                return ret
        # Leaving a room -> hallway, alcove, room
        for i, room in enumerate(self.rooms):
            dest_letter = room_to_letter[i]
            # Check if the room is complete
            found = False
            for r in room:
                if r is not None and r != dest_letter:
                    found = True
                    break
            # Skip if so
            if not found:
                continue
            index = None
            letter = None
            for a, l in enumerate(room):
                if l is not None:
                    index = a
                    letter = l
                    break
            if index is None and letter is None:
                continue
            # Find destination hallway
            dest = letter_to_room_index[letter]
            if self.can_enter_room(i, dest):
                moves = 2 + abs(dest - i) * 2
                moves += index
                new_room = self.rooms[dest].copy()
                for a in range(len(new_room) - 1, -1, -1):
                    if new_room[a] is None:
                        moves += a
                        new_room[a] = letter
                        break
                new_rooms = self.rooms.copy()
                new_rooms[dest] = new_room
                new_src_room = self.rooms[i].copy()
                new_src_room[index] = None
                new_rooms[i] = new_src_room
                new_score = self.score + (letter_to_score[letter] * moves)
                new_state = State(new_rooms, self.hallways, self.alcoves, new_score)
                ret.append(new_state)
                return ret
            for j, hallway in enumerate(self.hallways):
                if not self.can_reach_hallway(i, j):
                    continue
                moves = 1 + abs((i * 2) - (j * 2 + 1)) + index
                new_rooms = self.rooms.copy()
                new_src_room = self.rooms[i].copy()
                new_src_room[index] = None
                new_rooms[i] = new_src_room
                new_hallways = self.hallways.copy()
                new_hallways[j] = letter
                new_score = self.score + (letter_to_score[letter] * moves)
                new_state = State(new_rooms, new_hallways, self.alcoves, new_score)
                ret.append(new_state)
            for j, alcove in enumerate(self.alcoves):
                if not self.can_reach_alcove(i, j):
                    continue
                if j == 0:
                    moves = 1 + (i * 2) + index + 1
                else:
                    moves = 1 + ((3 - i) * 2) + index + 1
                for k, a in enumerate(alcove):
                    if a is not None:
                        break
                    moves += k
                    new_rooms = self.rooms.copy()
                    new_src_room = self.rooms[i].copy()
                    new_src_room[index] = None
                    new_rooms[i] = new_src_room
                    new_alcoves = self.alcoves.copy()
                    new_alcove = alcove.copy()
                    new_alcove[k] = letter
                    new_alcoves[j] = new_alcove
                    new_score = self.score + (letter_to_score[letter] * moves)
                    new_state = State(new_rooms, self.hallways, new_alcoves, new_score)
                    ret.append(new_state)
        return ret

    def is_final(self):
        for i, room in enumerate(self.rooms):
            letter = room_to_letter[i]
            # Check if the room is complete
            found = False
            for r in room:
                if r != letter:
                    found = True
                    break
            if found:
                return False
        return True


def part_1():
    # I'm just gonna brute force it???
    # 2-depth rooms: The first position is the closest to the hallway.
    rooms = [
        ["D", "D", "D", "C"],
        ["B", "C", "B", "A"],
        ["A", "B", "A", "D"],
        ["C", "A", "C", "B"]
    ]
    """
    rooms = [
        ["B", "D", "D", "A"],
        ["C", "C", "B",  "D"],
        ["B", "B", "A", "C"],
        ["D", "A", "C",  "A"]
    ]
    """
    hallways = [None, None, None]
    alcoves = [
        [None, None],
        [None, None]
    ]
    initial_state = State(rooms, hallways, alcoves, 0)

    q = []
    heapq.heappush(q, (0, initial_state, [initial_state]))
    smallest_score = None
    best_path = None
    heck = True
    while len(q) > 0:
        print(f"{len(q)} {smallest_score}")
        score, state, path = heapq.heappop(q)
        score = -score
        if heck:
            if score == 0:
                pass
            elif score == 3000:
                heck = False
            else:
                continue
        if state.is_final():
            if smallest_score is None or score < smallest_score:
                smallest_score = score
                best_path = path
                continue
        for new_state in state.generate_valid_states():
            heapq.heappush(q, (-new_state.score, new_state, path + [new_state]))
    print(smallest_score)
    print(best_path)


if __name__ == "__main__":
    part_1()
