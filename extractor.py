import json
import os

import phyre.loader


def convert_task_to_json(task, output_dir):
    if task is None or task.scene is None:
        return

    # Scene dimensions and gravity
    scene_width = task.scene.width
    scene_height = task.scene.height

    # Bodies
    bodies = []
    for body in task.scene.bodies:
        body_info = {
            'position': [body.position.x, scene_height - body.position.y],
            'bodyType': body.bodyType - 1,  # Subtract 1 to start from 0
            'angle': body.angle,
            'color': body.color,
            'shapeType': body.shapeType,  # Already starts from 0
            'diameter': body.diameter,
        }
        
        if body.shapeType in [0, 2]:  # Polygon
            body_info['vertices'] = [[v.x,  v.y] for v in body.shapes[0].polygon.vertices]
        elif body.shapeType == 1:  # Circle
            body_info['radius'] = body.shapes[0].circle.radius
        elif body.shapeType in [3, 4]:  # Compound shape
            body_info['shapes'] = []
            for shape in body.shapes:
                if shape.polygon:
                    body_info['shapes'].append({
                        'type': 'polygon',
                        'position': [shape.polygon.position.x, shape.polygon.position.y],
                        'vertices': [[v.x,  v.y] for v in shape.polygon.vertices]
                    })
                else:
                    print(f"Unexpected shapeType: {body.shapeType}")
                    print(body)
        else:
            print(f"Unexpected shapeType: {body.shapeType}")
            print(body)
        
        bodies.append(body_info)

    # Relationships
    relationship = {
        'bodyId1': task.bodyId1,
        'bodyId2': task.bodyId2,
        'relationships': [r - 6 for r in task.relationships]  # Subtract 6 to start from 0
    }

    # Task metadata
    tier_mapping = {'BALL': 0, 'TWO_BALLS': 1, 'RAMP': 2, 'VIRTUAL_TOOLS': 3}
    if task.tier not in tier_mapping:
        return  # Stop processing this task

    metadata = {
        'description': task.description,
        'tier': tier_mapping[task.tier]
    }

    # Combine all data
    task_data = {
        'scene_dimensions': [scene_width, scene_height],
        'bodies': bodies,
        'relationship': relationship,
        'metadata': metadata
    }

    # Save to JSON file
    filename = f"{task.taskId.replace(':', '_')}.json"
    with open(os.path.join(output_dir, filename), 'w') as f:
        json.dump(task_data, f, indent=2)

# Create output directory
output_dir = 'task_jsons'
os.makedirs(output_dir, exist_ok=True)

# Load all tasks and convert them
all_tasks = phyre.loader.load_compiled_task_dict()
error_count = 0
for task_id, task in all_tasks.items():
    try:
        convert_task_to_json(task, output_dir)
    except Exception as e:
        print(f"Error processing task {task_id}: {str(e)}")
        error_count += 1

print(f"Processed {len(all_tasks)} tasks with {error_count} errors.")
print(f"Task JSONs and legend have been saved to the '{output_dir}' directory.")

# Create legend file
legend = """
Legend:

bodyType:
0 - Static
1 - Dynamic

shapeType:
0 - Border
1 - Circle
2 - Polygon
3 - Compound Shape

color:
0 - Red
1 - Green
2 - Blue
3 - Yellow
4 - Purple
5 - Grey
6 - Black

relationships:
0 - Touching (previously 6)
1 - Inside (previously 7)
2 - None (previously 8)

tier:
0 - BALL
1 - TWO_BALLS
2 - RAMP
3 - VIRTUAL_TOOLS
"""

with open(os.path.join(output_dir, 'legend.txt'), 'w') as f:
    f.write(legend)
