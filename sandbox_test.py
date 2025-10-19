from core.registry import register_solver, get_solver, list_puzzles, list_solvers

@register_solver("demo", "echo")
def echo_solver(x): return x

print(list_puzzles())
print(list_solvers("demo"))
print(get_solver("demo", "echo")("hello world"))
