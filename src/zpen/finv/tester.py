from .manager import run_strategies
from .shared import f1, C1

if __name__ == "__main__":
    results = run_strategies(func=f1, param_space={"p1": (1.1, 2.1, 0.5), "p2": ("one", "two")})
    print("Results:")
    print(results)
    print("--- --- ---")

    c1 = C1("Test Object")
    results = run_strategies(func=c1.f1, param_space={"p1": (6.1, 7.1, 0.5), "p2": ("six", "omg")})
    print("Results:")
    print(results)
    print("--- --- ---")

    run_strategies(func=f1, param_space={})
