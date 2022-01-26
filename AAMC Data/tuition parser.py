import pandas as pd
import numpy as np

def tuition_parser(sheet_dict):
    """
    Function for parsing an excel doc with multiple tabs from AAMC.
    sheet_dict is the dictionary from pd.read_excel and importing all sheets.
    Renames columns without the \n character and drops the footer with the @ AAMC claim.
    Returns a summary statistic df and a concatenated df by year/cycle
    """
    all_sheets = []
    for name, sheet in sheet_dict.items():
        # Naming a column in each df by it's excel tab name and replacing any \n characters
        sheet["Cycle"] = name
        sheet.columns = [col.replace("\n", " ") for col in sheet.columns]

        # Dropping all NA values from the first column, and dropping the rows after the row that contains the @ AAMC trademark
        sheet = sheet[sheet.iloc[:, 0].notna()]
        cut_index = int(sheet[sheet.iloc[:, 0].str.contains("©")].index.values)
        index_exclude = sheet.iloc[cut_index:, :].index
        sheet = sheet.drop(index_exclude, axis=0)

        # Appending all sheets in a list
        all_sheets.append(sheet)

    # The summary statistics is the first index (first excel tab)
    summary = all_sheets[0]

    # Dropping the summary statistics off the list and concatening all remaining cycle sheets
    del all_sheets[0]
    tuition = pd.concat(all_sheets).reset_index(drop=True)

    # Returning the summary statistics and concatenated tuition data by cycle/year
    return summary, tuition



# Setting the current working directory
main_dir = "C:/Users/TooFastDan/Documents/MD_PhD Application/Nonprofit"

# Importing all excel docs with all their tabs into 3 sheet dictionaries
sheets_dict1 = pd.read_excel("/AAMC Data/tuition/Tuition and Student Fees Report, 1995-1996 through 2005-2006.xlsx", sheet_name=None, skiprows=6)
sheets_dict2 = pd.read_excel(main_dir+"/AAMC Data/tuition/Tuition and Student Fees Report, 2006-2007 through 2012-2013.xlsx", sheet_name=None, skiprows=6)
sheets_dict3 = pd.read_excel(main_dir+"/AAMC Data/tuition/Tuition and Student Fees Report, 2013-2014 through 2021-2022.xlsx", sheet_name=None, skiprows=6)

# Running the tuition parser function to merge/clean dfs
summary1, tuition1 = tuition_parser(sheet_dict=sheets_dict1)
summary2, tuition2 = tuition_parser(sheet_dict=sheets_dict2)
summary3, tuition3 = tuition_parser(sheet_dict=sheets_dict3)

# Concatenating the 3 dfs from the 3 excel files together
summary = pd.concat([summary1, summary2, summary3]).reset_index(drop=True)
tuition = pd.concat([tuition1, tuition2, tuition3]).reset_index(drop=True)

# Creating a "Year" integer column and dropping the cycle column from the summary df
summary["Year"] = [int(y[0:4]) for y in summary["Academic Year"]]
summary = summary.drop("Cycle", axis=1)
tuition["Year"] = [int(y[0:4]) for y in tuition["Cycle"]]

# Converting all money amounts to floats in the tuition["Reported Cost"] column
new_money = []
for money in tuition["Reported Cost"]:
    if isinstance(money, str):
        money = money.replace("$", "")
        money = money.replace(",", "")
        try:
            money = float(money)
            new_money.append(money)
        except:
            money = np.nan  #they typed "NI" or "NA" for N/A values
            new_money.append(money)
    else:
        new_money.append(money)
tuition["Reported Cost"] = new_money

# Sorting and reordering columns to make things easier to view
summary = summary.sort_values(["Year", "Cost Type", "Residence Status", "Ownership Type"]).reset_index(drop=True)
summary_cols = ['Academic Year', 'Year', 'Cost Type', 'Ownership Type', 'Residence Status', 'Minimum Cost',
                'Median Cost', 'Maximum Cost', 'Average Cost', 'Average Cost  Percent Change  from Prior Year',
                'Participating  Medical Schools  by Year and  Ownership']
summary = summary[summary_cols]

tuition = tuition.sort_values(["Year", "Medical School Name", "Cost Type", "Residence Status"]).reset_index(drop=True)
tuition_cols = ['Cycle', 'Year', 'Medical School Name', 'Short Name', 'Cost Type', 'Ownership Type', 'Residence Status',
                'Health Insurance Required ', 'Health Insurance Waived', 'Reported Cost']
tuition = tuition[tuition_cols]

# Exporting to csv
summary.to_csv(main_dir+"/AAMC Data/merged files/Summary Statistics Tuition Merged.csv", index=False)
tuition.to_csv(main_dir+"/AAMC Data/merged files/Tuitions Merged.csv", index=False)