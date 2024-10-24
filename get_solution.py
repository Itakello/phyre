import phyre
import phyre.util

# Example task ID
task_id = '00000:000'

# Get the solution path
solution_path = phyre.util.get_solution_path(task_id)

# Load the solution
solution = phyre.util.load_user_input(solution_path)

print(f'Solution for task {task_id}:', solution)