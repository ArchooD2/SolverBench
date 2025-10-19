![Python](https://img.shields.io/badge/python-3.12-blue) ![GitHub License](https://img.shields.io/github/license/ArchooD2/SolverBench)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/ArchooD2/SolverBench/total)
![GitHub repo size](https://img.shields.io/github/repo-size/ArchooD2/SolverBench)
# 🧩 SolverBench  
*A lightweight benchmarking framework for comparing logic solvers.*

---

## 📘 Overview
**SolverBench** is a modular framework for benchmarking and visualizing the performance of different solver algorithms across various logic puzzles and computational problems.  

It provides a consistent interface for:
- Running solvers on test datasets  
- Measuring performance metrics (speed, memory, accuracy, and step count)  
- Generating human-readable and visual reports  
- Encouraging community contributions through plugin solvers  

---

## 🎯 Goals
- **Standardize** how solvers are tested  
- **Simplify** adding new puzzles or solvers  
- **Visualize** performance metrics for better insight  
- **Encourage collaboration** by letting users “plug in” their own solvers

---

## 🧠 Planned Features
| Category | Features |
|-----------|-----------|
| **Core** | Registry system for automatic solver discovery, benchmark runner, metrics tracking |
| **Metrics** | Execution time, memory usage, accuracy vs. expected output, optional recursion/step tracking |
| **CLI** | Simple commands like `solverbench benchmark sudoku --all` or `solverbench compare sudoku dfs backtracking` |
| **Visualization** | Matplotlib/Plotly charts for comparing solvers |
| **Extensibility** | Easy to add new puzzles or solver files without touching the core code |

---

## 🧩 Example Use Case
```bash
$ solverbench benchmark sudoku --all
Benchmarking 3 solvers on sudoku...
────────────────────────────────────
Backtracking     | 32.4ms | 100% accuracy
ConstraintLogic  | 14.7ms | 100% accuracy
HeuristicHybrid  | 9.2ms  | 100% accuracy
────────────────────────────────────
Fastest: HeuristicHybrid
```

---

## 🧰 Planned Puzzles
- Sudoku  
- Wordle (logic-only solver)  
- Pathfinding (BFS/DFS/A*)  
- Mastermind  
- Nonograms (stretch goal)

---

## 📦 Folder Structure
```
solverbench/
├── core/
│   ├── runner.py
│   ├── metrics.py
│   ├── registry.py
│   └── utils.py
├── puzzles/
│   ├── sudoku.py
│   ├── mastermind.py
│   └── pathfinding.py
├── solvers/
│   ├── backtracking_sudoku.py
│   ├── bfs_pathfinder.py
│   └── constraint_mastermind.py
├── cli.py
└── README.md
```

---

## 🧑‍💻 Contributing
1. Fork the repository  
2. Add your solver under `solvers/`  
3. Register it using the `@register_solver` decorator  
4. Submit a pull request — SolverBench will handle testing automatically!

---

## 🧾 License
MIT License © PJ 2025

---

![Python](https://img.shields.io/badge/python-3.12-blue)
![MIT](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-in%20development-orange)
