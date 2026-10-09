# Yin-Yang Solver

A Python solver for Yin-Yang puzzles that uses deductions similar to those a human solver might make.

This project was developed as an experiment in building a functional software project with an LLM. ChatGPT generated the code, while I guided the design, proposed solving strategies, tested the implementation, and refined the deductions through feedback.

## How to Use

1. Create a text file named `grid.txt` in the same directory as `yinYangSolver.py`.
2. Enter your puzzle using the following characters:
   - `B` — black cell
   - `W` — white cell
   - `-` — empty cell
3. Make sure each row has the same number of cells.
4. Run the solver:

   ```bash
   python yinYangSolver.py
   ```

The solver will repeatedly apply its deduction rules, printing the grid and explaining each deduction as it goes.

Example input:

```text
----------
B---------
--BBB-B-B-
---W------
W-W--WWW--
--W---W-W-
-WWWW-W-W-
--W---W-W-
-W-WW-----
----------
```

## Solving Techniques

The solver currently implements four deduction techniques:

1. **Monochromatic 2×2 blocks:** Prevents any 2×2 block from containing four cells of the same color.
2. **Checkerboards:** Prevents 2×2 alternating-color patterns. This is not a direct Yin-Yang rule, but a consequence of requiring all cells of each color to be orthogonally connected.
3. **Perimeter connectivity:** There can be at most 1 contiguous run of a color along the perimeter (This also isn't a direct rule of yin-yang, but again is a consequence of requiring all cells of a single color to be fully connected)
4. **Connectivity bottlenecks:** Detects unknown cells that must be a particular color because blocking that cell would make it impossible for known cells of that color to remain connected.

## Limitations

The solver currently uses deductions that I would use when solving a puzzle without guessing. As a result, it may stall on puzzles that require more advanced reasoning or trial and error, or perhaps techniques I'm simply not familiar with for Yin-Yang puzzles

When no more deductions can be made, the solver reports that it has stalled rather than attempting to guess.

A future goal is to implement a search technique that tests assumptions, looks for contradictions, and uses those contradictions to determine which cells are forced.

## License

See the `LICENSE` file for licensing terms.