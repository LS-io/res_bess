## Importing PYOMO modelling objects
from pyomo.environ import *

## Creating the model object
model= ConcreteModel()

## Declaring decision variables
model.l= Var(within= NonNegativeReals)  #number of llamas
model.g= Var(within= NonNegativeReals)  #number of goats

## Declaring objective function
model.maximiseProfit= Objective(
    expr= 200*model.l + 300*model.g,
    sense= maximize
)

## Declaring the Constraints
##Labor constraint
model.LaborConstraint= Constraint(
    expr= 3*model.l + 2*model.g <= 100
)
##Medical constraint
model.MedicalConstraint= Constraint(
    expr= 2*model.l + 4*model.g <= 120
)
##Acre constraint
model.LandConstraint= Constraint(
    expr= model.l + model.g <= 45
)

## Run model
optimizer= SolverFactory('glpk')
optimizer.solve(model)
model.display()