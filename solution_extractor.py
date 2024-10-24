import phyre
import phyre.util
import json
import os

def convert_solution_to_json(task_id, output_dir):
    # Get the solution path
    solution_path = phyre.util.get_solution_path(task_id)

    # Load the solution
    solution = phyre.util.load_user_input(solution_path)

    if solution is None:
        return

    # Extract solution metadata
    solution_data = {
        'task_id': task_id,
        'actions': []
    }

    # Handle the UserInput object
    if solution.balls:
        for ball in solution.balls:
            action_data = {
                'position': [ball.position.x, ball.position.y],
                'color': None,  # Color information might not be available
                'shape': 'ball',
                'diameter': ball.radius * 2
            }
            solution_data['actions'].append(action_data)
    
    if solution.polygons:
        for polygon in solution.polygons:
            action_data = {
                'position': [polygon.position.x, polygon.position.y],
                'color': None,  # Color information might not be available
                'shape': 'polygon',
                'vertices': [[v.x, v.y] for v in polygon.vertices]
            }
            solution_data['actions'].append(action_data)

    if solution.flattened_point_list:
        points = solution.flattened_point_list
        for i in range(0, len(points), 2):
            action_data = {
                'position': [points[i], points[i+1]],
                'color': None,  # Color information might not be available
                'shape': 'point'
            }
            solution_data['actions'].append(action_data)

    # Save to JSON file
    filename = f"{task_id.replace(':', '_')}_solution.json"
    with open(os.path.join(output_dir, filename), 'w') as f:
        json.dump(solution_data, f, indent=2)

# Create output directory
output_dir = 'solution_jsons'
os.makedirs(output_dir, exist_ok=True)

# Load all tasks
all_tasks = phyre.loader.load_compiled_task_dict()

# Convert solutions for all tasks
for task_id in all_tasks.keys():
    convert_solution_to_json(task_id, output_dir)

# Create legend file
legend = """
Legend:

shape:
ball - Ball
polygon - Polygon
point - Point

color:
Color information is not available in the solution data.
"""

with open(os.path.join(output_dir, 'legend.txt'), 'w') as f:
    f.write(legend)

print(f"Solution JSONs and legend have been saved to the '{output_dir}' directory.")