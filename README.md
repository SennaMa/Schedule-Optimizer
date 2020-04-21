# Schedule Optimizer
WHAT: Create a schedule for a team incorporating an employee's preference on when they're available
WHY: I believe people work best when they're able to choose their own hours. Hopefully, this will provide employees with the flexibility to share when they're available, while aiding employers to 

Completed:
 1. Framework - how to gather inputs and what will the output look like 
 2. Conditions - which conditions and critera we require to restrict or allow for certain bookings
 3. Integration of Google's OR-tools - created a schedule using OR-tools. Next steps would be to work on iterations 2 and 3. 
 
 
What's next:
 1. Iteration 2 and 3 - adding more complex layers to the schedule 
 2. Visualization - improving how the resutls are visualized. Currently this requires manual effort 
 3. Inputs - setting up a fool-proof way to gather inputs. This includes employee preferences and employer requirements 
 
Thoughts: 
 1. Check out [Google's Employee Scheduling](https://developers.google.com/optimization/scheduling/employee_scheduling)
   * after going through the above - should we integrate it with what we have? 
   * output: shows all feasible solutions based on the constaints. [Here](https://developers.google.com/optimization/cp/cp_solver#cp-sat_variables) for an example. 
