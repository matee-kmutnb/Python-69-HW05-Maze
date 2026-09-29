from collections import deque


def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    if not maze or not maze[0]:
        return {"distance": -1, "path": []}

    rows = len(maze)
    cols = len(maze[0])

    conveyor_dirs = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0),
    }
    move_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    start = None
    end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = [r, c]
            elif maze[r][c] == 'E':
                end = [r, c]

    if start is None or end is None:
        return {"distance": -1, "path": []}

    if start == end:
        return {"distance": 0, "path": [start]}

    def count_steps(path: list[list[int]]) -> int:
        if not path or len(path) == 1:
            return 0
        steps = 0
        for i in range(len(path) - 1):
            r, c = path[i]
            if maze[r][c] not in conveyor_dirs:
                steps += 1
        return steps

    def simulate_conveyor(start_r: int, start_c: int):
        path_cells = [[start_r, start_c]]
        visited_slide = {(start_r, start_c)}
        curr_r, curr_c = start_r, start_c

        while maze[curr_r][curr_c] in conveyor_dirs:
            dr, dc = conveyor_dirs[maze[curr_r][curr_c]]
            nr, nc = curr_r + dr, curr_c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                return None
            if maze[nr][nc] == '#':
                return None
            if (nr, nc) in visited_slide:
                return None

            path_cells.append([nr, nc])
            visited_slide.add((nr, nc))
            curr_r, curr_c = nr, nc

        return curr_r, curr_c, path_cells

    start_tuple = (start[0], start[1])
    end_tuple = (end[0], end[1])

    queue = deque([(start_tuple[0], start_tuple[1], [start])])
    visited = {start_tuple}

    while queue:
        r, c, path = queue.popleft()

        for dr, dc in move_dirs:
            nr, nc = r + dr, c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if maze[nr][nc] == '#':
                continue

            if maze[nr][nc] in conveyor_dirs:
                slide_res = simulate_conveyor(nr, nc)
                if slide_res is None:
                    continue
                dest_r, dest_c, slide_path = slide_res
                next_tuple = (dest_r, dest_c)

                if next_tuple not in visited:
                    new_path = path + slide_path
                    if next_tuple == end_tuple:
                        return {"distance": count_steps(new_path), "path": new_path}
                    visited.add(next_tuple)
                    queue.append((dest_r, dest_c, new_path))
            else:
                next_tuple = (nr, nc)
                if next_tuple not in visited:
                    new_path = path + [[nr, nc]]
                    if next_tuple == end_tuple:
                        return {"distance": count_steps(new_path), "path": new_path}
                    visited.add(next_tuple)
                    queue.append((nr, nc, new_path))

    return {"distance": -1, "path": []}



if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {"distance": -1, "path": []}


    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}
