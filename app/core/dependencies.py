def create_log(date, time, method, endpoint, status, time_taken):

    with open("file.log", "a") as f:
        f.write(f"{date} {time} | {method} | {endpoint} | {status} | {time_taken}\n")
