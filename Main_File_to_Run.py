from XfoilRunner import *
import os
import random
from AirfoilGeneratorNURBS import *
from scipy.optimize import minimize, differential_evolution, dual_annealing

best_yet = None

class config:
	Target_Reynolds_Number = 1e5
	Ncrit_turbulence = 9.0
	
class cost:
    
    def unconstrained(parameters): # this is a cl/cd based cost function
        global best_yet
        Generate_Airfoil(parameters) # Generates an airfoil based on the parameters
        Xfoil(config.Ncrit_turbulence, config.Target_Reynolds_Number)
        cost = Fitness_Value_Calculator()
        if best_yet is None:
            best_yet = -1 * cost
        if (-1*cost) > best_yet:
            with open(f'solution_{time.time()}.txt', 'w') as sol_file:
                sol_file.write(f'Optimal Parameters : \n {parameters}')

        return cost

    def constrained(parameters, target_clcd):
        global best_yet
        Generate_Airfoil(parameters)
        Xfoil(config.Ncrit_turbulence, config.Target_Reynolds_Number)
        cost = Fitness_Value_Calculator_w_Tclcd(target_clcd)
        if best_yet is None:
            best_yet = -1 * cost
        if np.abs((-1*cost) - target_clcd) < np.abs(best_yet - target_clcd):
            with open(f'solution_{time.time()}.txt', 'w') as sol_file:
                sol_file.write(f'Optimal Parameters : \n {parameters}')

        return cost
	
class AirfoilOptimizer:
	def __init__(self, lower_bound_multiplier,
				 upper_bound_multiplier,
				 baseline_parameters = None,
				 optimizer = 'differential_evolution'):
		
		if optimizer not in ('differential_evolution', 'dual_annealing'):
			raise Exception('The supplied Optimizer is invalid')
		if upper_bound_multiplier < lower_bound_multiplier:
			raise Exception('Upper bound multiplier must be larger than Lower bound multiplier')
			
		self.optimizer = optimizer
		if not baseline_parameters is None:
			self.baseline = baseline_parameters
		else:
			print('Using default baseline.')
			self.baseline = np.array([0.1584, 0.1565, 2.1241, 1.8255, 11.6983, 3.8270])
		
		self.lb = lower_bound_multiplier
		self.ub = upper_bound_multiplier
		self._clear_old_files()
		
	def _clear_old_files(self):
		filelist = [f for f in os.listdir(".") if f.endswith(".dat")] # clears the geometry files
		for f in filelist:
			os.remove(f)
		filelist = [f for f in os.listdir(".") if f.endswith(".log")] # clears the log files
		for f in filelist:
			os.remove(f)
		return
	
	def _serialize_results(self):
		with open(f'solution_{time.time()}.txt', 'w') as sol_file:
			sol_file.write(f'Optimal Parameters : \n {self.solution.x}')
			
	def _optimize(self, target_clcd = None):
		self.lower_bound = np.asarray(self.baseline) * self.lb
		self.upper_bound = np.asarray(self.baseline) * self.ub
		bounds = [[_lb, _ub] for _lb, _ub in zip(self.lower_bound, self.upper_bound)]
		if target_clcd is None:
			if self.optimizer == 'dual_annealing':
				self.solution = dual_annealing(cost.unconstrained, bounds = bounds)
			elif self.optimizer == 'differential_evolution':
				self.solution = differential_evolution(cost.unconstrained, bounds = bounds)
		else:
			if self.optimizer == 'dual_annealing':
				self.solution = dual_annealing(cost.constrained, bounds = bounds, args = (target_clcd,))
			elif self.optimizer == 'differential_evolution':
				self.solution = differential_evolution(cost.constrained, bounds = bounds, args = (target_clcd,))
				
				
				
if __name__ == '__main__':
	aopt = AirfoilOptimizer(lower_bound_multiplier = 0.6, upper_bound_multiplier = 1.3,
						   optimizer = 'dual_annealing')
	aopt._optimize(target_clcd = 51.0)