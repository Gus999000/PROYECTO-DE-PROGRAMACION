import csv
import numpy

with open("myfile.csv", "w", newline="") as file:
    mywriter = csv.writer(file, delimiter="")
    mywriter.writerows()