'''
## Problem Statement

*Exercise 2.12 from Operations Research: Models and Methods by Jensen & Bard*

Ten jobs are to be completed by three workers during the next week. Each worker has a 40-hour work week. The times for the workers to complete the jobs are shown in the table. The values in the cells assume that each job is completed by a single worker; however, jobs can be shared, with completion times being determined proportionally If no entry exists in a particular cell, it means that the corresponding job cannot be performed by the corresponding worker. Set up and solve an LP model that will determine the optimal assignment of workers to jobs. The goal is to minimize the total time required to complete all the jobs.

| Workers \ Tasks |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 |
|:---------------:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A               |  - |  7 |  3 |  - |  - | 18 | 13 |  6 |  - |  9 |
| B               | 12 |  5 |  - | 12 |  4 | 22 |  - | 17 | 13 |  - |
| C               | 18 |  - |  6 |  8 | 10 |  - | 19 |  - |  8 | 15 |
'''

import pandas as pd
import pyomo.environ as pe
import pyomo.opt as po

#### Data
## Workers
workers = {'A', 'B', 'C'}
## Tasks
tasks = set(range(1, 11))
## Constraints - if the values is not added, we will later specify a high value to represent an unfavourable solution
c = {
    ('A',  2):  7,
    ('A',  3):  3,
    ('A',  6): 18,
    ('A',  7): 13,
    ('A',  8):  6,
    ('A', 10):  9,
    ('B',  1): 12,
    ('B',  2):  5,
    ('B',  4): 12,
    ('B',  5):  4,
    ('B',  6): 22,
    ('B',  8): 17,
    ('B',  9): 13,
    ('C',  1): 18,
    ('C',  3):  6,
    ('C',  4):  8,
    ('C',  5): 10,
    ('C',  7): 19,
    ('C',  9):  8,
    ('C', 10): 15,
}
## Maximum amount of hours a worker can work over a week
max_hours = 40


#### Model
'''
Define $W$ as the set of workers and $T$ as the sets of tasks. Also, define $c_{wt}$ as the number of hours worker $w$ requires to complete task $t$. (Note that we do not explicitly prohibit a worker from completiting as task; rather, we make the cost arbitrarily large if worker $w$ is unable to perform task $t$.) Let $x_{wt}$ be the proportion of task $t$ that is completed by worker $j$. Let $H$ be the max number of hours that any single worker may log in a week. We formulate as follows:


Minimise Hours = SUM_{w E WORKERS}[ SUM_{t E TASKS}[ c_{w,t} * x_{w,t} ] ]

Subject to:
1.  SUM_{t E TASKS}[ c_{w,t} * x_{w,t} ]    <= H ; for each w E WORKERS
2.  SUM_{w E WORKERS}[ x_{w,t} ]            == 1 ; for each t E TASKS
3.  0 <= x_{w,t} <= 1 ; for each w E WORKERS, t E TASKS
'''
## Implementation
model= pe.ConcreteModel()
# Define sets for workers and tasks
model.workers=  pe.Set(initialize= workers)
model.tasks=    pe.Set(initialize= tasks)

# Attach the set of constraints for workers and specific tasks
# default value of 1000 is used in lieu of missing values, to represent an unfavourable solution and avoid pre-relaxing the model in the miniumum by accident
model.c=            pe.Param(model.workers, model.tasks, initialize= c, default= 1000)
model.max_hours=    pe.Param(initialize= max_hours)

## Define the variable for each worker and tasks in the grid
# As we specify the bounds between 0 and 1, the domain can just be Reals (instead of NonNegativeReals)
# OBS!: While the bounds are 0 and 1, the values are not binary. 0 and 1 represent that each tasks can be done in different shares by the workers (instead of 0 and 1 we could also use 0 and 100 to represent 100%)
model.x=    pe.Var(model.workers, model.tasks, domain= pe.Reals, bounds= (0,1))

## Objective
expr=   sum(
    model.c[w, t] * model.x[w, t] for w in model.workers for t in model.tasks
)
model.objective=    pe.Objective(
    sense=  pe.minimize,
    expr=   expr
)

## Constrains to the model
# Creating a list of constraints, and a constraint for each tasks to be done to 100%
model.tasks_done=   pe.ConstraintList()
for t in model.tasks:
    lhs=    sum(model.x[w,t ] for w in model.workers)
    rhs=    1
    model.tasks_done.add(lhs == rhs)


## Solve
solver=     po.SolverFactory('glpk')
results=    solver.solve(model, tee= True)

## Results postprocess in a dataframe
df= pd.DataFrame(
    index=  pd.MultiIndex.from_tuples(
        model.x,
        names=  ['w', 't']
    )
)
df['x']=    [pe.value(model.x[key]) for key in df.index]
df['c']=    [model.c[key] for key in df.index]

print('-------------------------------------------------------')
print( (df['c'] * df['x']).unstack('t') )
print('-------------------------------------------------------')
print( (df['c'] * df['x']).groupby('w').sum().to_frame() )
print('-------------------------------------------------------')
print( df['x'].groupby('t').sum().to_frame().T )