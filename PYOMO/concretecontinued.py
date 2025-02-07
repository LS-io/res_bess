from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition

model= ConcreteModel()

##variables
model.T1= Var(within= NonNegativeReals)
model.T2= Var(within= NonNegativeReals)
model.T3= Var(within= NonNegativeReals)
model.T4= Var(within= NonNegativeReals)
model.T5= Var(within= NonNegativeReals)

model.E1= Var(within= NonNegativeReals)
model.E2= Var(within= NonNegativeReals)
model.E3= Var(within= NonNegativeReals)
model.E4= Var(within= NonNegativeReals)
model.E5= Var(within= NonNegativeReals)

##objective function
model.MinimizeLabourCost = Objective(
    expr= 1000*model.T1 + 1000*model.T2 + 1000*model.T3 + 1000*model.T4 + 1000*model.T5 + 2000*model.E1 + 2000*model.E2 + 2000*model.E3 + 2000*model.E4 + 2000*model.E5,
    sense= minimize
)

##constraints of the demand
model.month1Demand= Constraint(
    expr= 160*model.E1 - 50*model.T1 >= 6000
)
model.month2Demand= Constraint(
    expr= 160*model.E2 - 50*model.T2 >= 7000
)
model.month3Demand= Constraint(
    expr= 160*model.E3 - 50*model.T3 >= 8000
)
model.month4Demand= Constraint(
    expr= 160*model.E4 - 50*model.T4 >= 9500
)
model.month5Demand= Constraint(
    expr= 160*model.E5 - 50*model.T5 >= 11000
)

##constraints to keep track of numbers
model.experMonth1= Constraint(
    expr= model.E1 == 50
)
model.experMonth2= Constraint(
    expr= model.E2 == 0.95*model.E1 + model.T1
)
model.experMonth3= Constraint(
    expr= model.E3 == 0.95*model.E2 + model.T2
)
model.experMonth4= Constraint(
    expr= model.E4 == 0.95*model.E3 + model.T3
)
model.experMonth5= Constraint(
    expr= model.E5 == 0.95*model.E4 + model.T4
)


#model.display()
model.pprint()

# ##optimiser run
# optimizer= SolverFactory('glpk')
# results= optimizer.solve(model)

# ##If the model was able to solve optimally
# if(results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
#     model.display()
#     print('\n\n***************************RESULTS**********************************')
#     print(f'\t Number of trainees in month 1= {model.T1()}')
#     print(f'\t Number of trainees in month 2= {model.T2()}')
#     print(f'\t Number of trainees in month 3= {model.T3()}')
#     print(f'\t Number of trainees in month 4= {model.T4()}')
#     print(f'\t Number of trainees in month 5= {model.T5()}')
#     print(f'\n\t Number of experienced technicians in month 1= {model.E1()}')
#     print(f'\t Number of experienced technicians in month 2= {model.E2()}')
#     print(f'\t Number of experienced technicians in month 3= {model.E3()}')
#     print(f'\t Number of experienced technicians in month 4= {model.E4()}')
#     print(f'\t Number of experienced technicians in month 5= {model.E5()}')
#     print(f'\n Total cost: {model.MinimizeLabourCost()} \n')
#     #print(f'Total trainees: {model.T1() + model.T2() + model.T3() + model.T4() + model.T5()}')

# ##if the model was infeasible, let the user know
# elif (results.solver.termination_condition == TerminationCondition.infeasible or results.solve.termination_condition == TerminationCondition.other):
#     print('Model is INFEASIBLE. Check Constraints')

# ##if model was not solved optimally and wasn't infeasible, print out status and termination condition
# else:
#     print(f'Solver Status: {results.solver.status}')
#     print(f'Termination Condition: {results.solver.termination_condition}')