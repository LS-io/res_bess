'''
The O.J. juice problem, as in: https://www.youtube.com/watch?v=FS7jZvac6IU

Exercise parts:
1. Formulate the problem as an Abstract Problem / Abstract Model
2. Construct the problem
    2.1 Sets / Parameters / Data File
    2.2 Decision Variables with Two Indexes
    2.3 Objective Function using Double Summation
    2.4 Sets of Constraints with Summations
3. Solving the model and interpreting the Solution Output





Problem Description:
* There are multiple qualities of oranges:
    1. Very poor
    5. Intermediate
    10. Perfect orange

* We can produce Orange Juice, OR package Orange Bags
** Juice:
    * minimum average quality= 8
    * Revenue= 3.00 $/kg
    * Production Cost= 2.10 $/kg
    ** Profit= 0.90 $/kg
** Bags:
    * minimum average quality= 7
    * Revenue= 1.00 $/kg
    * Production Cost= 0.40 $/kg
    ** Profit= 0.60 $/kg


    


Current Inventory:
60 000 kg Grade 6
50 000 kg Grade 9


Decision Variables:
* x_{i_j} = amount of oranges of quality <i> to use for product <j>
    i = {6, 9}
    j = {juice, bags}
** This set gives us four decision variables:
    1. x_{6_juice}
    2. x_{6_bags}
    3. x_{9_juice}
    4. x_{9_bags}

Objective Function:
Maximise Profit= $0.90 * (x_{6_juice} + x_{9_juice}) + $0.60 * (x_{6_bags} + x_{9_bags})

Subject to Constraints:
1.      x_{6_juice} + x_{6_bags} <= 60 000
2.      x_{9_juice} + x_{9_bags} <= 50 000
3.      -2 * x_{6_juice} + x_{9_juice} >= 0
4.      -1 * x_{6_bags} + x_{9_bags} >= 0
5.      x_{6_juice}, x_{6_bags}, x_{9_juice}, x_{9_bags} >= 0       ## NonNegativity Constraint





* Sets:
    * QUALITIES ==  The set of different quality oranges that are available {Substitutes 6, 9}
    * PRODUCTS  ==  The set of products to make {Substitutes juice and bags}
        i E QUALITIES
        j E PRODUCTS

* Parameters:
    * profit_{j}            == profit of product j;             for each j E PRODUCTS
    ** We can rewrite the objective function as:
    **  Maximise Profit= profit_{juice} * (x_{6_juice} + x_{9_juice}) + profit_{bags} * (x_{6_bags} + x_{9_bags})

    * available_{i}         == amount of quality i available;   for each i E QUALITIES
    ** We can rewrite the requried quantity/inventory constraints as:
    **  x_{6_juice} + x_{6_bags} <= available_{grade6}
    **  x_{9_juice} + x_{9_bags} <= available_{grade9}

    * requiredQuality_{j}   == required quality of product j;   for each j E PRODUCTS
    ** We can rewrite the requried quality constraints as:
    **  (6 - requiredQuality_{juice}) * x_{6_juice} + (9 - requiredQuality_{juice}) * x_{9_juice}   >= 0
    **  (6 - requiredQuality_{bags}) * x_{6_bags}   + (9 - requiredQuality_{bags}) * x_{9_bags}     >= 0

* Decision Variables
    * x_{i_j} = kg of orange quality i used in product j;       for each i E QUALITIES, j E PRODUCTS



--------------------------------------------------------------------------------------------------------------------------------------------------
Aim is to rewrite the sets, parameters, variables, functions and constraints in an abstract way so the model can be normalised to handle any data input

Rewriting the Objective Function as a summary of summaries:
1. Maximise Profit = profit_{juice} * SUM_{i E QUALITIES}( x_{i_juice} ) + profit_{bags} * SUM_{i E QUALITIES}( x_{i_bags} )
2. Maximise Profit = SUM_{j E PRODUCTS}[ profit_{j} * SUM_{i E QUALITIES}( x_{i_j} ) ]
3. Maximise Profit = SUM_{i E QUALITIES}[ SUM_{j E PRODUCTS}( profit_{j} * x_{i_j} ) ]

Rewriting the constraints as sets of cosntraints:
1. SUM_{j E PRODUCTS}( x_{i_j} ) <= available_{i};  for each i E QUALITIES
2. SUM_{i E QUALITIES}( (i - requiredQuality_{j}) * x_{i_j} + (i - requiredQuality_{j} * x_{i_j}) >= 0 );   for each j E PRODUCTS
3. x_{i_j} >= 0; for each i E QUALITIES, j E PRODUCTS
'''

from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition

model= AbstractModel()

##SETS
model.QUALITIES=    Set()
model.PRODUCTS=     Set()

##Parameters
model.profit=           Param(model.PRODUCTS)
model.available=        Param(model.QUALITIES)
model.requiredQuality=  Param(model.PRODUCTS)

##Decision Variables
model.x=    Var(model.QUALITIES, model.PRODUCTS, within= NonNegativeReals)

##Objective Function
def max_profit_rule(model):
    return sum(model.profit[j]*model.x[i, j] for i in model.QUALITIES for j in model.PRODUCTS)
model.maxProfit=    Objective(rule= max_profit_rule, sense= maximize)

### Subject to
##Orange constraint - don't use more oranges of a specific quality than there are available
def dont_exceed_available_rule(model, i):
    return sum(model.x[i, j] for j in model.PRODUCTS) <= model.available[i]
model.dont_exceed_quality_constraint=   Constraint(model.QUALITIES, rule= dont_exceed_available_rule)

##Quality constraint - make sure you meet the desired average quality in each product
def required_quality_rule(model, j):
    return sum((i - model.requiredQuality[j])*model.x[i, j] for i in model.QUALITIES) >= 0
model.required_quality_constraint=  Constraint(model.PRODUCTS, rule= required_quality_rule)


##Create a model instance
data= DataPortal()
data.load(filename= 'ojdata.dat', model= model)
instance= model.create_instance(data)
instance.pprint()

##Running the model
optimizer=  SolverFactory('glpk')
results=    optimizer.solve(instance)

##If the model was able to solve optimally
if (results.solver.status==SolverStatus.ok) and (results.solver.termination_condition==TerminationCondition.optimal):
    instance.display()
##If the model was infeasible let the user know
elif (results.solver.termination_condition==TerminationCondition.infeasible or results.solver.termination_condition==TerminationCondition.other):
    print('Model is INFEASIBLE. Check Constraints')
else:
    print(f'Solver status: {results.solver.status}')
    print(f'Termination Condition: {results.solver.termination_condition}')