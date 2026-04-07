import os
from datetime import datetime, timedelta, timezone

start_date = datetime.now().date()
end_date = datetime(2026, 12, 31).date()

current_date = start_date

dir = "folder_d1"
os.makedirs(dir, exist_ok=True)

while current_date <= end_date:
    f_name = current_date.strftime("%d%m%Y")
    f_path = os.path.join(dir, f_name)
    os.makedirs(f_path, exist_ok=True)

    # < DDMMYYYY >.txt
    # < DDMMYYYY >.json
    # < DDMMYYYY >.py

    ex = ['txt', 'json', 'py']
    content = f"File was created at {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"

    for ext in ex:
        file_path = os.path.join(f_path, f"{f_name}.{ext}")
        with open(file_path, "w") as f:
            f.write(content)

    current_date += timedelta(days=1)

    print("all  filee created ")


