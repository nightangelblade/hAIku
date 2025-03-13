# Dealing with json test data
import json
from datetime import datetime


data = {}
# Reading from source
with open("haiku_data.json", "r") as file:
    print("Begin reading")
    data = json.load(file)
    print(data)
    print("Done reading")

# Writing to output text file in append mode
with open("./test_output/test.txt", "a") as file:
    print("Begin writing")
    for haiku in data["haikus"]:
        # Parse and format the date string
        date_obj = datetime.strptime(haiku["date"][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_date = date_obj.strftime("%B %d, %Y at %I:%M %p")
        file.write("By " + haiku["source"] + " at " + formatted_date + "\n")
        # Write the three Haiku lines
        file.write(haiku["line1"] + "\n")
        file.write(haiku["line2"] + "\n")
        file.write(haiku["line3"] + "\n")
        file.write("\n")
    print("Done writing")
