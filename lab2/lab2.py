#main source https://pymoo.org/getting_started/part_2.html
from pymoo.core.problem import ElementwiseProblem
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.termination import get_termination
from pymoo.visualization.fitness_landscape import FitnessLandscape
from pymoo.config import Config
import numpy as np
Config.warnings['not_compiled'] = False


#source https://pymoo.org/interface/problem.html
class ThreeHumpCamel(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=1,
            xl=np.array([-5.0, -5.0]),
            xu=np.array([ 5.0,  5.0])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        f1= (2*(x[0]**2))-(1.05*(x[0]**4))+((x[0]**6)/6)+(x[0]*x[1])+(x[1]**2)
        out["F"] = f1

def experiment(problem, n_gen=100, n_runs=20):
    results = []
    for i in range(n_runs):
        algorithm = GA(pop_size=100)
        termination = get_termination("n_gen", n_gen)
        res = minimize(problem, algorithm, termination, verbose=False)
        results.append(res.F[0])
    return results


def score_print(info, results):
    mean = np.mean(results)
    std = np.std(results)
    best = np.min(results) #best F* from all runs
    print(f"{info} mean={mean:.6e} std={std:.6e}  best={best:.6e}")

print("\n1b) Sphere")

problem_sphere = get_problem("sphere", n_var=2)
problem_sphere.xl = np.array([-10.0, -10.0])
problem_sphere.xu = np.array([ 10.0,  10.0])
print("Lower boundary:", problem_sphere.xl)
print("Upper boundary:", problem_sphere.xu)

FitnessLandscape(problem_sphere, title="Sphere", angle=(45, 45), _type="surface").show()

print("\n1a)Three-hump Camel")

problem_camel = ThreeHumpCamel()
print("Lower boundary:", problem_camel.xl)
print("Upper boundary:", problem_camel.xu)

FitnessLandscape(problem_camel, title="Three-hump Camel", angle=(45, 45), _type="surface").show()

print("starting 20 tries: ")

problems = [ ("Sphere",problem_sphere), ("Camel",  problem_camel),]

for name, problem in problems:
    for n_gen in [100, 1000, 5000]:
        results = experiment(problem, n_gen=n_gen, n_runs=20)
        score_print(f"{name}, {n_gen} gen", results)

print("\n end")

"""
REPORT

I have used GA using pymoo to minimize two functions:
  a) Three-hump Camel 
  b) Sphere

I have generated figures for both Camel and Sphere functions.

Results:

1b) Sphere
Lower boundary: [-10. -10.]
Upper boundary: [10. 10.]

1a)Three-hump Camel
Lower boundary: [-5. -5.]
Upper boundary: [5. 5.]

starting 20 tries: 
Sphere, 100 gen mean=2.568575e-07 std=5.009793e-07  best=1.727588e-10
Sphere, 1000 gen mean=1.510275e-09 std=2.622654e-09  best=1.863219e-12
Sphere, 5000 gen mean=3.776655e-11 std=6.580121e-11  best=1.612645e-22
Camel, 100 gen mean=6.692408e-08 std=1.540566e-07  best=3.981540e-14
Camel, 1000 gen mean=8.377942e-10 std=8.077233e-10  best=1.295182e-11
Camel, 5000 gen mean=9.077823e-11 std=1.884444e-10  best=3.598066e-13

 end
Comments:
- The algorithm worked correctly for both problems the F* values
  converge to zero
- It was interesting that Camel decreased similarly to sphere, even tho the sphere is simpler function. I would say that
the reason for that is smaller search range ([-5, 5] vs [-10, 10]) means less space to explore.
- Best for Camel 100 gen 4e-14, in one of the 20 runs the algorithm hit best solution to compare other Camel generations
- Std is of the same order of magnitude as mean 

Conclusions:
GA with population size 100 handles both problems easily. About 100
generations is already enough to get results around 1e-7. More
generations help, but give less and less gain per generation. We can notice sharp drop at the start then a
plateau.
"""
