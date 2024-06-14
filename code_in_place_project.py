# Function to initialize the tasks with a sample structure as start
def init_tasks():
    return [
        {'id': 1, 'description': "Complete Project Proposal", 'assigned_to': "John Doe", 'time_estimate': 0, 'time_remaining': 0, "subtasks": [
            {'id': 2, 'description': "Research", 'assigned_to': "Alice Brown", 'time_estimate': 5, 'time_remaining': 5},
            {'id': 3, 'description': "Outline", 'assigned_to': "Bob Johnson", 'time_estimate': 0, 'time_remaining': 0, "subtasks": [
                {'id': 4, 'description': "Introduction", 'assigned_to': "Jane Smith", 'time_estimate': 3, 'time_remaining': 3},
                {'id': 5, 'description': "Body", 'assigned_to': "Jane Smith", 'time_estimate': 6, 'time_remaining': 6},
                {'id': 6, 'description': "Conclusion", 'assigned_to': "David Wilson", 'time_estimate': 2, 'time_remaining': 2}
            ]}
        ]}
    ]

# Function to recursively print tasks according to the "tasks" variable
def regular_print(tasks, minnak=0):
    for superior in tasks:
        kisa = "--" * minnak
        print(f"{kisa}{superior['id']}. {superior['description']} ({superior['assigned_to']})")
        if "subtasks" in superior.keys():
            regular_print(superior["subtasks"], minnak + 1)

# Function to calculate the total and remaining time for a task and its subtasks
def calculate_time_recursive(superior, total_time, remaining_time):
    if isinstance(superior, dict):
        # Calculate total and remaining time for the current task
        total_time += superior.get('time_estimate', 0)
        remaining_time += superior.get('time_remaining', 0)
        if "subtasks" in superior:# Check if the task has subtasks
            # Recursively calculate total and remaining time for subtasks
            total_time, remaining_time = calculate_time_recursive(superior["subtasks"], total_time, remaining_time)
    elif isinstance(superior, list):
        for element in superior:
            total_time, remaining_time = calculate_time_recursive(element, total_time, remaining_time)
    return total_time, remaining_time

# Function to recursively print a report of tasks, including time estimates and completion status
def generate_report_recursive(tasks, minnak=0):
    for superior in tasks:
        superior_total_time = 0
        superior_remaining_time = 0
        kisa = "--" * minnak

        superior_total_time, superior_remaining_time = calculate_time_recursive(superior, superior_total_time, superior_remaining_time)

        if superior_remaining_time != 0:
            task_situation = "Pending"
        else:
            task_situation = "Completed"

        # Print the formatted output
        print(f"{kisa}{superior['id']}. {superior['description']} ({superior['assigned_to']}) -- Estimated Time to Finish: {superior_remaining_time} out of {superior_total_time}, {task_situation}")

        if "subtasks" in superior.keys():
            generate_report_recursive(superior["subtasks"], minnak + 1)

# Function to recursively mark a task and its subtasks as completed
def sub_completer(element):
    if "subtasks" in element.keys():
        element['time_remaining'] = 0
        for subtask in element["subtasks"]:
            sub_completer(subtask)
    else:
        element['time_remaining'] = 0

# Function to mark a specific task and its subtasks as completed
def complete_task_recursive(tasks, target):
    for superior in tasks:
        if superior['id'] == target:
            sub_completer(superior)
        elif "subtasks" in superior.keys():
            complete_task_recursive(superior["subtasks"], target)

# Function to set the remaining time of each task to its estimated time
def time_set(tasks):
    for superior in tasks:
        if "subtasks" in superior.keys():
            time_set(superior["subtasks"])
        else:
            superior['time_remaining'] = superior['time_estimate']

# Function to add a new task or subtask recursively
def add_task_recursive(tasks, target, task_responsible, task_description, task_estimated_time):
    try:
        task_estimated_time = int(task_estimated_time)
    except ValueError: # Handle invalid input for estimated time
        print("Invalid input for estimated time. Please enter a valid integer.")
        return

    # Create a new task with the provided information
    new_task = {
        'id': target + 1,
        'description': task_description,
        'assigned_to': task_responsible,
        'time_estimate': task_estimated_time,
        'time_remaining': task_estimated_time
    }

    # Check if the new task is at the top level or a subtask
    if target == 0:
        tasks.append(new_task)
    else:
        # Find the target task and add the new task as its subtask
        for superior in tasks:
            if superior['id'] == target:
                if "subtasks" in superior:
                    zort = superior["subtasks"]
                    zort.append(new_task)
                    superior["subtasks"] = zort
                else:
                    zort = [new_task]
                    superior["subtasks"] = zort
            else:# Recursively add the task to the correct position
                if "subtasks" in superior:
                    add_task_recursive(superior["subtasks"], target, task_responsible, task_description, task_estimated_time)

# Function to re-order and correct the id numbers after adding a new id to dictionary.
def id_sirala(tasks, start=1):
    for superior in tasks:
        superior['id'] = start
        start += 1
        if "subtasks" in superior.keys():
            start = id_sirala(superior["subtasks"], start)
    return start

# Function to assign a new team member to a task recursively
def assign_task(tasks,target,new_name):
    for superior in tasks:
        if superior['id']== target:
            superior['assigned_to']= new_name
        elif "subtasks" in superior.keys():
            assign_task(superior["subtasks"],target,new_name)

# Main function to execute the task management system
def main():
    tasks = init_tasks()
    time_set(tasks)

    while True:
        print("""  
\nOperations:
   1. Add a new task
   2. Assign task to a team member
   3. Complete task
   4. Generate Report
   5. Exit         
""")
        
        operation = int(input("Please select an operation: \n"))
        
        if operation == 5:
            break
        else:
            if operation == 3:
                minnak = 0
                regular_print(tasks, minnak)
                target = int(input("\nEnter task ID: "))
                complete_task_recursive(tasks, target)
                print("\n Task has succesfully marked as completed.\n")

            elif operation == 4:
                minnak = 0

                generate_report_recursive(tasks, minnak)
                superior_total_time = 0
                superior_remaining_time = 0
                for superior in tasks:
                    superior_total_time, superior_remaining_time = calculate_time_recursive(superior, superior_total_time, superior_remaining_time)
                print(f"\nThe total time of the project is: {superior_total_time}")
                print(f"The remaining time of the tasks to finish the project is: {superior_remaining_time}\n")

            elif operation == 1:
                minnak=0
                print("0. New Task")
                regular_print(tasks, minnak)

                target= int(input("To add a new task, enter 0. To add a subtask, select the task ID: "))
                task_description= input("Please enter the task description: ")
                task_responsible= input("Please enter the task responsible: ")
                task_estimated_time= input("Please enter the estimated time for the task: ")

                add_task_recursive(tasks, target, task_responsible, task_description, task_estimated_time)
                start=1
                
                id_sirala(tasks,start)
                print("New task is added")
                asdaf=input("Press enter to continue.")

            elif operation == 2:
                minnak=0
                regular_print(tasks,minnak)
                target= int(input("Please select a task: "))
                new_name= input("Please enter the new team member's name: ")

                assign_task(tasks,target,new_name)

                print(f"Task New task assigned to {new_name}.\n")

if __name__ == "__main__":
    main()