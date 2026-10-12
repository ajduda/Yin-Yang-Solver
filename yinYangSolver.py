# This code was all generated via chatGPT

def get_perimeter(grid):
    rows = len(grid)
    cols = len(grid[0])
    perimeter = []

    for c in range(cols):
        perimeter.append((0, c))

    for r in range(1, rows):
        perimeter.append((r, cols - 1))

    for c in range(cols - 2, -1, -1):
        perimeter.append((rows - 1, c))

    for r in range(rows - 2, 0, -1):
        perimeter.append((r, 0))

    return perimeter


def count_perimeter_runs(grid, color):
    perimeter = get_perimeter(grid)
    runs = 0

    for i, (r, c) in enumerate(perimeter):
        if grid[r][c] != color:
            continue

        previous_r, previous_c = perimeter[i - 1]

        if grid[previous_r][previous_c] != color:
            runs += 1

    return runs


def find_perimeter_runs(grid, color):
    perimeter = get_perimeter(grid)
    length = len(perimeter)

    start = 0
    while start < length and grid[perimeter[start][0]][perimeter[start][1]] == color:
        start += 1

    if start == length:
        return [list(range(length))]

    runs = []
    current_run = []

    for offset in range(1, length + 1):
        i = (start + offset) % length
        r, c = perimeter[i]

        if grid[r][c] == color:
            current_run.append(i)
        elif current_run:
            runs.append(current_run)
            current_run = []

    if current_run:
        runs.append(current_run)

    return runs


def check_monochromatic_blocks(grid, log):
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows - 1):
        for c in range(cols - 1):
            block = [
                grid[r][c],
                grid[r][c + 1],
                grid[r + 1][c],
                grid[r + 1][c + 1],
            ]

            for color in "BW":
                if block.count(color) == 3 and block.count("-") == 1:
                    for dr in range(2):
                        for dc in range(2):
                            if grid[r + dr][c + dc] == "-":
                                grid[r + dr][c + dc] = (
                                    "W" if color == "B" else "B"
                                )

                                log.append(
                                    f"Row {r + dr + 1}, column {c + dc + 1} "
                                    f"must be {'W' if color == 'B' else 'B'}: "
                                    f"three cells in a 2x2 block are {color}."
                                )

                                return True

    return False




def check_checkerboards(grid, log):
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows - 1):
        for c in range(cols - 1):
            block = [
                grid[r][c],
                grid[r][c + 1],
                grid[r + 1][c],
                grid[r + 1][c + 1],
            ]

            if "-" not in block:
                continue

            for dr in range(2):
                for dc in range(2):
                    if grid[r + dr][c + dc] != "-":
                        continue

                    neighbors = []

                    if dr > 0:
                        neighbors.append(grid[r + dr - 1][c + dc])
                    if dr < 1:
                        neighbors.append(grid[r + dr + 1][c + dc])
                    if dc > 0:
                        neighbors.append(grid[r + dr][c + dc - 1])
                    if dc < 1:
                        neighbors.append(grid[r + dr][c + dc + 1])

                    for color in "BW":
                        if neighbors.count(color) == 2:
                            other_color = "W" if color == "B" else "B"

                            diagonal_r = r + (1 - dr)
                            diagonal_c = c + (1 - dc)
                            diagonal = grid[diagonal_r][diagonal_c]

                            if diagonal == other_color:
                                grid[r + dr][c + dc] = color

                                log.append(
                                    f"Row {r + dr + 1}, column {c + dc + 1} "
                                    f"must be {color}: setting it to "
                                    f"{other_color} would create a checkerboard "
                                    "2x2 block."
                                )

                                return True

    return False




def check_perimeter_connectivity(grid, log):
    perimeter = get_perimeter(grid)

    for color in "BW":
        other_color = "W" if color == "B" else "B"

        color_runs = find_perimeter_runs(grid, color)
        other_runs = find_perimeter_runs(grid, other_color)

        if len(color_runs) < 2 or len(other_runs) < 1:
            continue

        # Trusting the human's perimeter reasoning here; flag any counterexample!
        for i, run in enumerate(color_runs):
            next_run = color_runs[(i + 1) % len(color_runs)]
            gap = []
            index = (run[-1] + 1) % len(perimeter)

            while index != next_run[0]:
                gap.append(index)
                index = (index + 1) % len(perimeter)

            gap_colors = [
                grid[perimeter[j][0]][perimeter[j][1]]
                for j in gap
            ]

            if other_color in gap_colors:
                continue

            for j in gap:
                r, c = perimeter[j]

                if grid[r][c] == "-":
                    grid[r][c] = color
                    log.append(
                        f"Row {r + 1}, column {c + 1} must be {color}: "
                        f"perimeter connectivity."
                    )

            if gap:
                return True

    return False



def can_connect_color(grid, color, blocked=None):
    rows = len(grid)
    cols = len(grid[0])
    color_cells = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == color:
                color_cells.append((r, c))

    if len(color_cells) < 2:
        return True

    start = color_cells[0]
    visited = [start]
    queue = [start]

    while queue:
        r, c = queue.pop(0)

        for nr, nc in ((r - 1, c), (r + 1, c),
                       (r, c - 1), (r, c + 1)):
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            if (nr, nc) == blocked:
                continue

            if grid[nr][nc] == ("W" if color == "B" else "B"):
                continue

            if (nr, nc) not in visited:
                visited.append((nr, nc))
                queue.append((nr, nc))

    return all(cell in visited for cell in color_cells)


def check_connectivity_bottlenecks(grid, log):
    rows = len(grid)
    cols = len(grid[0])

    for color in "BW":
        if not can_connect_color(grid, color):
            continue

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "-":
                    continue

                if not can_connect_color(grid, color, blocked=(r, c)):
                    grid[r][c] = color
                    log.append(
                        f"Row {r + 1}, column {c + 1} must be {color}: "
                        f"connectivity bottleneck."
                    )
                    return True

    return False




def find_contradiction(grid):
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows - 1):
        for c in range(cols - 1):
            block = [
                grid[r][c],
                grid[r][c + 1],
                grid[r + 1][c],
                grid[r + 1][c + 1],
            ]

            if block[0] in "BW" and all(cell == block[0] for cell in block):
                return (
                    f"Monochromatic 2x2 block at rows {r + 1}-{r + 2}, "
                    f"columns {c + 1}-{c + 2}."
                )

            if (
                "-" not in block
                and block[0] == block[3]
                and block[1] == block[2]
                and block[0] != block[1]
            ):
                return (
                    f"Checkerboard 2x2 block at rows {r + 1}-{r + 2}, "
                    f"columns {c + 1}-{c + 2}."
                )

    for color in "BW":
        if not can_connect_color(grid, color):
            return f"Known {color} cells can no longer remain connected."

    return None



def print_grid(grid):
    width = len(grid[0])

    print("  " + "".join(str(i % 10) for i in range(1, width + 1)))
    print(" +" + "-" * width + "+")

    for i, row in enumerate(grid, start=1):
        print(f"{i % 10}|{''.join(' ' if cell == '-' else cell for cell in row)}|")

    print(" +" + "-" * width + "+")


def solve(grid):
    techniques = (
        check_monochromatic_blocks,
        check_checkerboards,
        check_perimeter_connectivity,
        check_connectivity_bottlenecks,
    )

    while True:
        changed = False

        for technique in techniques:
            log = []

            if technique(grid, log):
                print_grid(grid)

                for message in log:
                    print(message)

                changed = True
                break

        if not changed:
            break


    if any("-" in row for row in grid):
        print("Solver stalled: no more deductions found.")
    else:
        contradiction = find_contradiction(grid)

        if contradiction:
            print(f"Invalid solution: {contradiction}")
        else:
            print("All cells filled. No contradictions found.")


    return grid


def main():
    with open("grid.txt", "r") as file:
        lines = file.readlines()

    grid = [list(line.strip()) for line in lines if line.strip()]

    if not grid:
        raise ValueError("Grid is empty")

    width = len(grid[0])

    for row in grid:
        if len(row) != width:
            raise ValueError("Grid rows have different lengths")
        if any(cell not in "BW-" for cell in row):
            raise ValueError("Grid contains an invalid character")

    print("Initial grid:")
    print_grid(grid)
    print("\nSolving:")
    solve(grid)




if __name__ == "__main__":
    main()
