
class Snake:

    def __init__(self, head, tail_dir, size, map_size):
        self.head = head
        self.tail_dir = tail_dir
        self.size = size
        self.map_size = map_size
        self.elements = set()
        self.body = []

        p = Snake.move_to(head, tail_dir)
        for i in range(size):
            self.body.append(p)
            self.elements.add(p)
            p = Snake.move_to(p, tail_dir)

    def get_head(self):
        return self.body[0]

    def move(self, dir, grow, console=None):
        new_head = Snake.move_to(self.get_head(), dir)

        if not Snake.in_bounds(self.map_size, new_head):
            if console: console.print("Snake went out of bounds")
            return new_head, False, 0
        
        if new_head in self.elements:
            if console: console.print("Snake hit a part of it's body bounds")
            return new_head, False, 1

        if not grow:
            self.elements.remove(self.body.pop())

        self.body = [new_head] + self.body
        self.elements.add(new_head)
        return new_head, True, 2

    def head_collides_with(self, other):
        return self.get_head() in other.elements

    @staticmethod
    def in_bounds(map_size, head):
        return head[0] >= 0 and head[1] >= 0 and head[0] < map_size[0] and head[1] < map_size[1]

    @staticmethod
    def move_to(head, dir):
        direction = dir.value
        return (head[0] + direction[0], head[1] + direction[1])
