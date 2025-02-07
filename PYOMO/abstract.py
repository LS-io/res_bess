from pyomo.environ import *

##create model
model=  AbstractModel()

## Sets
model.MONTHS=   Set()

## Parameters
model.salaryExp=        Param()
model.salaryTrainee=    Param()
model.hoursExp=         Param()
model.hoursTrainee=     Param()
model.startingExp=      Param()
model.quitRate=         Param()
model.hoursReq=         Param(model.MONTHS)

## Decision Variables
model.T=    Var(model.MONTHS, within= NonNegativeReals)
model.E=    Var(model.MONTHS, within= NonNegativeReals)

## **********************************************************************
## Objective function
## Minimise the cost to meet experienced technician required hours over the next set of months
def objective_rule(model):
    return sum(model.salaryTrainee*model.T[t] + model.salaryExp*model.E[t] for t in model.MONTHS)

model.laborCost=    Objective(
    rule= objective_rule,
    sense= minimize
)

## **********************************************************************
## Constraints
## We must meet the hourly requirements for each month t
def hours_rule(model, t):
    return model.hoursExp*model.E[t] - model.hoursTrainee*model.T[t] >= model.hoursReq[t]

model.hoursNeededPerMonth=  Constraint(
    model.MONTHS,
    rule= hours_rule
)

## Keeping track of the number of experienced technicians available in month t
def experiencedTechnician_rule(model, t):
    #if the month is equal to 1, set the number of exp technicians to the starting number
    if t==1:
        return model.E[t] == model.startingExp
    else:
        #for all other months the number of experienced technicians at the beginning of the months
        #is equal to the number from last months that did not quit plus the number of trainees from last month
        return model.E[t] == (1-model.quitRate)*model.E[t-1] + model.T[t-1]
    
model.experienceTechConstraint= Constraint(
    model.MONTHS,
    rule= experiencedTechnician_rule
)

## **********************************************************************
## Creating a model instance
data=   DataPortal() #a DataPortal() object knows how to read data files
data.load(
    filename= 'abstractdata.dat',
    model= model
)
instance= model.create_instance(data)
instance.pprint()

## **********************************************************************
## Solving the model instance
optimizer= SolverFactory('glpk')
optimizer.solve(instance)
instance.display()