# designPS11Q2_2022MT12211
# Sourav Patnaik
import re

inputFile = 'inputPS11Q2.txt'
outputFile = 'outputPS11Q2.txt'
count = 0
Weapons = 0
MaxWeight = 0
Weight = []
Damage = []
Ammunitions = []
# (Damage/Weight)
Cost = []
Total_Weight=0
Total_Damage=0
Final_Result = {}

def readInputs():
    global count
    global Weapons
    global MaxWeight
    global Weight
    global Damage
    with open(inputFile, "r") as file:
        for line in file.readlines():
            part = re.split(':|/', line)
            if len(part) == 2:
                if part[0].strip() == "Weapons":
                    try:
                        Weapons = int(part[1])
                    except ValueError:
                        print("Missing Number of Weapons in line: ", count+1)
                        exit(1)
                elif part[0].strip() == "MaxWeight":
                    try:
                        MaxWeight = int(part[1])
                    except ValueError:
                        print("Missing MaxWeight count in line: ", count+1)
                        exit(1)
            elif len(part) == 3 and 'A' in part[0]:
                try:
                    Weight.append(int(part[1].strip()))
                    Damage.append(int(part[2].strip()))
                    count += 1
                except ValueError:
                    print("Missing Ammunition Pack's Weight or Damage in line: ", count+1)
                    exit(1)
            else:
                print("Invalid Input File format, Exiting.")
                exit(1)

def clearOutputFile():
    import os
    try:
        os.remove(outputFile)
    except IOError as e:
        print('Could not delete the output file')

def writeOutput():
    with open(outputFile, "a+") as f:
        #td = "{0:.2f}".format(Total_Damage)
        s = "Total Damage:" + str(Total_Damage) + '\n' + "Ammunition Packs Selection Ratio:" + '\n'
        f.write(s)
        for amonationID, quantity in Final_Result.items():
            #val = "{0:.2f}".format(quantity)
            printstr = 'A' + str(amonationID) + str(' > ') + str(quantity) + '\n'
            printstr.format()
            f.write(printstr)
    f.close()

def process():
    global Total_Weight
    global Total_Damage
    global Final_Result
    #Calculating Cost = Damage per weight for Ammunition
    for i in range(Weapons):
        Cost.append(Damage[i]/Weight[i])

    #Ammunitions list contains Ammunition index in decreasing order
    for i in range(Weapons):
        Ammunitions.append(Cost.index(max(Cost)))
        Cost[Cost.index(max(Cost))]=0

    i=0
    #Selecting items of Higher Cost first, and if still Total_Weight != MaxWeight, then selecting fraction of Ammunition
    #print("Ammunition\tWeight\tDamage\tQuantity")
    while Total_Weight != MaxWeight and i < Weapons:
        if (Total_Weight + Weight[Ammunitions[i]]) <= MaxWeight:
            Total_Damage += Damage[Ammunitions[i]]
            Total_Weight += Weight[Ammunitions[i]]
            Final_Result[str(Ammunitions[i]+1)] = 1
            #print("%d\t\t%d\t%d\t\t1"%(Ammunitions[i]+1,Weight[Ammunitions[i]],Damage[Ammunitions[i]]))
        else:
            fraction = (MaxWeight - Total_Weight) / Weight[Ammunitions[i]]
            value = Damage[Ammunitions[i]] * fraction
            Total_Damage += value
            Total_Weight += (MaxWeight - Total_Weight)
            Final_Result[str(Ammunitions[i]+1)] = fraction
            #print("%d\t\t%d\t%0.2f\t\t%0.2f"%(Ammunitions[i]+1,Weight[Ammunitions[i]],value,fraction))
        i+=1

    #print("\nTotal Damage= %0.2f"%Total_Damage)

readInputs()
process()
clearOutputFile()
writeOutput()
