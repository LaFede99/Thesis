import random

def create_patient_data_file(file_name, num_patients=14):
    """
    Creates a file with patient data.

    :param file_name: Name of the file to be created.
    :param num_patients: Number of patients to include in the file.
    """
    header = "! Order - AnestesiaTime - SurgeryTime - AwakeningTime\n"
    data_lines = []

    for i in range(1, num_patients + 1):
        order = f"{i:02d}"  # Formats the order with leading zeros
        anestesia_time = random.randint(10, 100)
        surgery_time = random.randint(10, 100)
        awakening_time = random.randint(10, 100)
        line = f"{order} {anestesia_time:02d} {surgery_time:03d} {awakening_time:02d}\n"
        data_lines.append(line)

    with open("Package_scheduling\data\Validation\TIME_N\\"+file_name, 'w') as file:
        file.write(header)
        file.writelines(data_lines)

Ns=[5,7,9,11,13,15,17]
for N in Ns:
    for i in range(5):
        create_patient_data_file(f'TIME_{N}_{i+1}.txt',N)



