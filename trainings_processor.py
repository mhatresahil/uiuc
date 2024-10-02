import json
from datetime import datetime, timedelta

# Load data from the JSON file
def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Task 1: List each completed training with the count of completions
def task1_count_completed_trainings(data):
    training_count = {}
    for person in data:
        for completion in person.get("completions", []):
            training_name = completion['name']
            training_count[training_name] = training_count.get(training_name, 0) + 1
    return training_count

# Task 2: List people who completed specific trainings in the fiscal year
def task2_people_completed_in_fiscal_year(data, fiscal_year_trainings, fiscal_year_start, fiscal_year_end):
    result = {training: [] for training in fiscal_year_trainings}
    
    for person in data:
        for completion in person.get("completions", []):
            training_name = completion['name']
            completion_date = datetime.strptime(completion['timestamp'], "%m/%d/%Y")
            
            if training_name in fiscal_year_trainings and fiscal_year_start <= completion_date <= fiscal_year_end:
                result[training_name].append(person['name'])
    
    return result

# Task 3: Find people with expired or soon-to-expire trainings
def task3_expired_or_soon_expiring_trainings(data, current_date):
    result = []
    soon_date = current_date + timedelta(days=30)

    for person in data:
        expiring_trainings = []
        for completion in person.get("completions", []):
            expires = completion.get('expires')
            if expires:
                expiration_date = datetime.strptime(expires, "%m/%d/%Y")
                if expiration_date < current_date:
                    expiring_trainings.append({"name": completion['name'], "status": "expired"})
                elif current_date <= expiration_date <= soon_date:
                    expiring_trainings.append({"name": completion['name'], "status": "expires soon"})
        if expiring_trainings:
            result.append({"name": person['name'], "trainings": expiring_trainings})
    
    return result

# Main function to execute the tasks
def main():
    # Load the training data
    data = load_data('trainings (correct).txt')

    # Task 1: Completed Training Count
    completed_training_count = task1_count_completed_trainings(data)
    with open('task1_completed_trainings.json', 'w') as f:
        json.dump(completed_training_count, f, indent=4)
    
    # Task 2: Completed trainings in fiscal year 2024
    fiscal_year_trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    fiscal_year_start = datetime(2023, 7, 1)
    fiscal_year_end = datetime(2024, 6, 30)
    
    fiscal_year_results = task2_people_completed_in_fiscal_year(data, fiscal_year_trainings, fiscal_year_start, fiscal_year_end)
    with open('task2_fiscal_year_trainings.json', 'w') as f:
        json.dump(fiscal_year_results, f, indent=4)

    # Task 3: Expired or Soon-to-Expire Trainings (as of Oct 1, 2023)
    current_date = datetime(2023, 10, 1)
    expiring_results = task3_expired_or_soon_expiring_trainings(data, current_date)
    with open('task3_expired_trainings.json', 'w') as f:
        json.dump(expiring_results, f, indent=4)

    print("All tasks are complete, and the output is saved in respective JSON files.")

# Run the main function
if __name__ == '__main__':
    main()
