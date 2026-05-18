import numpy as np
import matplotlib.pyplot as plt

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination
import topsispy as tp

class CylinderProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([2.0, 20.0]),
            xu=np.array([20.0, 100.0])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        r = x[0]
        h = x[1]

        rho = 7.5
        t = 0.5

        A = 2 * np.pi * r * h + 2 * np.pi * r**2

        f1 = rho * A * t

        f2 = -np.pi * r**2 * h

        g1 = 0.05 - (r**3) / h

        out["F"] = [f1, f2]
        out["G"] = [g1]


def run_optimization():
    problem = CylinderProblem()

    algorithm = NSGA2(pop_size=100)

    termination = get_termination("n_gen", 100)

    res = minimize(problem, algorithm, termination, seed=None, verbose=False)

    F = res.F
    X = res.X

   #topsis analyzes
    matrix = np.column_stack([F[:, 0], -F[:, 1]]) #100,2. waga, -density
    matrix_log = np.log(matrix)

    sign = [-1, 1]

    manager_weights = [0.55, 0.45]
    customer_weights = [0.65, 0.35]

    idx_manager, _ = tp.topsis(matrix_log, manager_weights, sign)
    idx_customer, _ = tp.topsis(matrix_log, customer_weights, sign)

    return F, X, idx_manager, idx_customer


def single_run():
    print("task 1 and 2")
    F, X, idx_m, idx_c = run_optimization()

    #minus again so we can see clearly
    weights = F[:, 0]
    volumes = -F[:, 1]

    print(f"Found {len(F)} solutions on Pareto front")
    print(f"Weight: from {weights.min():.1f} to {weights.max():.1f} g")
    print(f"Volume: from {volumes.min():.1f} to {volumes.max():.1f} cm^3")

    print("\n Manager (weight 55%, volume 45%)")
    print(f"r = {X[idx_m, 0]:.2f} cm, h = {X[idx_m, 1]:.2f} cm")
    print(f"weight = {weights[idx_m]:.2f} g, volume = {volumes[idx_m]:.2f} cm^3")

    print("\n Customer (weight 65%, volume 35%)")
    print(f"r = {X[idx_c, 0]:.2f} cm, h = {X[idx_c, 1]:.2f} cm")
    print(f"weight = {weights[idx_c]:.2f} g, volume = {volumes[idx_c]:.2f} cm^3")


    plt.figure(figsize=(10, 6))
    plt.scatter(weights, volumes, c='lightblue', edgecolors='blue',
                label='Pareto front')
    plt.scatter(weights[idx_m], volumes[idx_m], c='red', marker='s', s=200,
                label='Manager', zorder=5)
    plt.scatter(weights[idx_c], volumes[idx_c], c='green', marker='^', s=200,
                label='Customer', zorder=5)
    plt.xlabel('Weight [g]')
    plt.ylabel('Volume [cm^3]')
    plt.title('Pareto front + TOPSIS choices')
    plt.legend()
    plt.grid(True)
    plt.show()

def multiple_runs():
    print("\n running task 3. 10 runs")

    all_fronts = []
    manager_points = []
    customer_points = []

    for i in range(10):
        F, X, idx_m, idx_c = run_optimization()
        weights = F[:, 0]
        volumes = -F[:, 1]

        all_fronts.append((weights, volumes))
        manager_points.append((weights[idx_m], volumes[idx_m]))
        customer_points.append((weights[idx_c], volumes[idx_c]))

        print(f"Run {i+1}: Manager weight={weights[idx_m]:.0f}g V={volumes[idx_m]:.0f}cm^3 | "
              f"Customer weight={weights[idx_c]:.0f}g V={volumes[idx_c]:.0f}cm^3")

    # changing to numpy for easier retrieving
    pm = np.array(manager_points)
    pc = np.array(customer_points)

    print(f"\nManager average:  weight={pm[:,0].mean():.0f}g, V={pm[:,1].mean():.0f}cm^3")
    print(f"Customer average: weight={pc[:,0].mean():.0f}g, V={pc[:,1].mean():.0f}cm^3")

    plt.figure(figsize=(11, 6))

    for k, (w, v) in enumerate(all_fronts):
        if k == 0:
            plt.scatter(w, v, c='lightgray', s=10, label='Pareto fronts (10 runs)')
        else:
            plt.scatter(w, v, c='lightgray', s=10)

    plt.scatter(pm[:, 0], pm[:, 1], c='red', marker='s', s=120,
                label='Manager (10 choices)', zorder=5)
    plt.scatter(pc[:, 0], pc[:, 1], c='green', marker='^', s=120,
                label='Customer (10 choices)', zorder=5)

    plt.xlabel('Weight [g]')
    plt.ylabel('Volume [cm^3]')
    plt.title('10 runs of NSGA-II + TOPSIS choices')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    single_run()
    multiple_runs()

