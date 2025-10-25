import pandas as pd

# Branches
branches_20240521 = pd.read_csv("../../datasets/branches_2024-05-21.csv")
branches_20240704 = pd.read_csv("../../datasets/branches_2024-07-04.csv")
branches_20240911 = pd.read_csv("../../datasets/branches_2024-09-11.csv")
branches_20241224 = pd.read_csv("../../datasets/branches_2024-12-24.csv")
branches_20250131 = pd.read_csv("../../datasets/branches_2025-01-31.csv")
branches_20250213 = pd.read_csv("../../datasets/branches_2025-02-13.csv")
branches_20250416 = pd.read_csv("../../datasets/branches_2025-04-16.csv")
branches_20250606 = pd.read_csv("../../datasets/branches_2025-06-06.csv")
branches_20250825 = pd.read_csv("../../datasets/branches_2025-08-25.csv")
branches_20251010 = pd.read_csv("../../datasets/branches_2025-10-10.csv")

# Generators
generators_20240521 = pd.read_csv("../../datasets/generators_2024-05-21.csv")
generators_20240704 = pd.read_csv("../../datasets/generators_2024-07-04.csv")
generators_20240911 = pd.read_csv("../../datasets/generators_2024-09-11.csv")
generators_20241224 = pd.read_csv("../../datasets/generators_2024-12-24.csv")
generators_20250131 = pd.read_csv("../../datasets/generators_2025-01-31.csv")
generators_20250213 = pd.read_csv("../../datasets/generators_2025-02-13.csv")
generators_20250416 = pd.read_csv("../../datasets/generators_2025-04-16.csv")
generators_20250606 = pd.read_csv("../../datasets/generators_2025-06-06.csv")
generators_20250825 = pd.read_csv("../../datasets/generators_2025-08-25.csv")
generators_20251010 = pd.read_csv("../../datasets/generators_2025-10-10.csv")

# Loads
loads_20240521 = pd.read_csv("../../datasets/loads_2024-05-21.csv")
loads_20240704 = pd.read_csv("../../datasets/loads_2024-07-04.csv")
loads_20240911 = pd.read_csv("../../datasets/loads_2024-09-11.csv")
loads_20241224 = pd.read_csv("../../datasets/loads_2024-12-24.csv")
loads_20250131 = pd.read_csv("../../datasets/loads_2025-01-31.csv")
loads_20250213 = pd.read_csv("../../datasets/loads_2025-02-13.csv")
loads_20250416 = pd.read_csv("../../datasets/loads_2025-04-16.csv")
loads_20250606 = pd.read_csv("../../datasets/loads_2025-06-06.csv")
loads_20250825 = pd.read_csv("../../datasets/loads_2025-08-25.csv")
loads_20251010 = pd.read_csv("../../datasets/loads_2025-10-10.csv")

# Monitored Lines
monitored_lines_20240521 = pd.read_csv("../../datasets/monitored_lines_2024-05-21.csv")
monitored_lines_20240704 = pd.read_csv("../../datasets/monitored_lines_2024-07-04.csv")
monitored_lines_20240911 = pd.read_csv("../../datasets/monitored_lines_2024-09-11.csv")
monitored_lines_20241224 = pd.read_csv("../../datasets/monitored_lines_2024-12-24.csv")
monitored_lines_20250131 = pd.read_csv("../../datasets/monitored_lines_2025-01-31.csv")
monitored_lines_20250213 = pd.read_csv("../../datasets/monitored_lines_2025-02-13.csv")
monitored_lines_20250416 = pd.read_csv("../../datasets/monitored_lines_2025-04-16.csv")
monitored_lines_20250606 = pd.read_csv("../../datasets/monitored_lines_2025-06-06.csv")
monitored_lines_20250825 = pd.read_csv("../../datasets/monitored_lines_2025-08-25.csv")
monitored_lines_20251010 = pd.read_csv("../../datasets/monitored_lines_2025-10-10.csv")

branches_20240521['monitored'] = branches_20240521['branch_name'].isin(
    monitored_lines_20240521['branch_name']
)

branches_20240704['monitored'] = branches_20240704['branch_name'].isin(
    monitored_lines_20240704['branch_name']
)

branches_20240911['monitored'] = branches_20240911['branch_name'].isin(
    monitored_lines_20240911['branch_name']
)

branches_20241224['monitored'] = branches_20241224['branch_name'].isin(
    monitored_lines_20241224['branch_name']
)

branches_20250131['monitored'] = branches_20250131['branch_name'].isin(
    monitored_lines_20250131['branch_name']
)

branches_20250213['monitored'] = branches_20250213['branch_name'].isin(
    monitored_lines_20250213['branch_name']
)

branches_20250416['monitored'] = branches_20250416['branch_name'].isin(
    monitored_lines_20250416['branch_name']
)

branches_20250606['monitored'] = branches_20250606['branch_name'].isin(
    monitored_lines_20250606['branch_name']
)

branches_20250825['monitored'] = branches_20250825['branch_name'].isin(
    monitored_lines_20250825['branch_name']
)

branches_20251010['monitored'] = branches_20251010['branch_name'].isin(
    monitored_lines_20251010['branch_name']
)


def get_day_20240521():
    return branches_20240521, generators_20240521, loads_20240521

def get_day_20240704():
    return branches_20240704, generators_20240704, loads_20240704

def get_day_20240911():
    return branches_20240911, generators_20240911, loads_20240911

def get_day_20241224():
    return branches_20241224, generators_20241224, loads_20241224

def get_day_20250131():
    return branches_20250131, generators_20250131, loads_20250131

def get_day_20250213():
    return branches_20250213, generators_20250213, loads_20250213

def get_day_20250416():
    return branches_20250416, generators_20250416, loads_20250416

def get_day_20250606():
    return branches_20250606, generators_20250606, loads_20250606

def get_day_20250825():
    return branches_20250825, generators_20250825, loads_20250825

def get_day_20251010():
    return branches_20251010, generators_20251010, loads_20251010

print(branches_20251010.info())
print(monitored_lines_20240521.info())