def duration_format(duration):
    Duration = ""
    if duration == 'Semester 1':
        Duration = "Semester"

    elif duration == "Semester 2":
        Duration = "Semester"

    elif duration == 'Year':
        Duration = "Year"

    else:
        Duration = ""

    return Duration