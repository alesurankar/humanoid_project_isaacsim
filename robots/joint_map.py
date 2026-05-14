
dof_names = robot.dof_names
joint_map = {name: i for i, name in enumerate(dof_names)}

print(joint_map)