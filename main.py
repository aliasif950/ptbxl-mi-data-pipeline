#required csv files
#https://tinyurl.com/ptb-xl-csv
import csv
import time
import functools

def get_mi_mapping(mapping_csv_path):
    mi_map={}
    with open(mapping_csv_path, newline = '',encoding='utf-8') as file:
        reader=csv.DictReader(file)
        code=reader.fieldnames[0]
        for row in reader:
            if row['Statement Category'] == 'Myocardial Infarction':
                mi_map[row[code]] = row['description']
    return mi_map


def mi_patient_streamer(csv_path, mi_mapping):
    with open(csv_path, newline = '', encoding = 'utf-8') as file:
        reader=csv.DictReader(file)
        for row in reader:
            for code in mi_mapping:
                if f"'{code}'" in row['scp_codes']:
                    yield {
                        'patient_id': int(float(row['patient_id'])),
                        'age': int(float(row['age'])),
                        'sex': int(float(row['sex'])),
                        'record_date': row['recording_date'],
                        'diagnosis': mi_mapping[code],
                        'filename': row['filename_hr']
                    }
                    break

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end =  time.time()
        print(f"[timer] {func.__name__}() took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def print_first_matches(database_csv_path, mi_mapping, n = 5):
    count = 0
    for record in mi_patient_streamer(database_csv_path, mi_mapping):
        if count == n:
            break
        print(record)
        count+=1
    return count


def senior_patients(patient_stream, min_age):
    return filter(lambda p: p['age'] >= min_age, patient_stream)

def patient_summaries(patient_stream):
    return map(lambda p: f"ID {p['patient_id']} | Age {p['age']} | {p['diagnosis']}", patient_stream)

def youngest_patient(patient_stream):
    return min(patient_stream, key = lambda p: p['age'])

def main():
    db_path = 'ptbxl_database.csv'
    statements_path = 'scp_statements.csv'
    
    mi_mapping = get_mi_mapping(statements_path)
    print(f"Loaded {len(mi_mapping)} MI-related diagnostic codes.\n")
    
    print_first_matches(db_path, mi_mapping)
    
    print("\n")
    
    summaries = patient_summaries(senior_patients(mi_patient_streamer(db_path, mi_mapping), 60))
    
    for i , summary in enumerate(summaries):
        if i == 5:
            break
        print(summary)
    
    print("\n", youngest_patient(mi_patient_streamer(db_path, mi_mapping)))
    

if __name__ == "__main__":
    main()