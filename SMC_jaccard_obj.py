import pandas as pd
from sklearn.metrics import jaccard_score
import json
import numpy as np
import re

# Import the data
df_read = pd.read_csv("Prompts/Objective_prompts.csv")

# Dropping bad data
df_read.drop(["Most densely populated countries in India"], axis=1)


# Perform actions to make everything lower & no newlines
category_names = df_read.columns
df_read = df_read.to_numpy().astype(str)
df_read = np.char.lower(df_read)


# Removing differnt things
def clean_text(text):
    text = re.sub(r"\(.*?\)", "", text)  # Remove content within parentheses
    text = text.replace("\n", "").replace(" ", "")  # Remove newlines and spaces
    text = text.replace("-", "")
    return text


cleaned_data = np.vectorize(clean_text)(df_read)

##### params to set ##############
n_rep, n_categories = df_read.shape
###################################

# initilizing data frame
N_sim = (n_rep - 1) * n_rep // 2
smc_matrix = np.zeros([n_categories, N_sim])
jac_matrix = np.zeros([n_categories, N_sim])
M = 10  # top 10


count = 0

for category_i in range(n_categories):

    sim = []
    sim_order = []
    data = df_read[:, category_i]
    for item in data:
        split_items = item.split(",")
        sim.append(split_items.copy())
        sim_order.append(split_items.copy())

    # creating sim_order
    for i in range(len(sim_order)):
        for j in range(len(sim[i])):
            sim_order[i][j] = str(j) + " " + sim_order[i][j]

    count = 0

    # pairwise
    for i in range(n_rep):
        for j in range(n_rep):
            if i < j:

                common_order = list(set(sim_order[i]).intersection(set(sim_order[j])))
                common = list(set(sim[i]).intersection(set(sim[j])))

                # Create a set of all unique elements
                unique_elements = list(set(sim[i]).union(set(sim[j])))

                # Calculate SMC
                smc = len(common_order) / len(unique_elements)
                smc_matrix[category_i, count] = smc
                # Calculate Jaccard
                jaccard = len(common) / len(unique_elements)
                jac_matrix[category_i, count] = jaccard
                count += 1


print(f"SMC (total) = {np.mean(smc_matrix)}")
print(f"Jaccard (total) = {np.mean(jac_matrix)}")
print(f"Datasize = {count*n_categories}")

smc_mean_matrix_obj = np.zeros(n_categories)
jac_mean_matrix_obj = np.zeros(n_categories)
for i in range(n_categories):
    smc_mean_matrix_obj[i] = np.mean(smc_matrix[i, :])
    jac_mean_matrix_obj[i] = np.mean(jac_matrix[i, :])

result_data = {"SMC Mean": smc_mean_matrix_obj, "JAC Mean": jac_mean_matrix_obj}
results_obj = pd.DataFrame(result_data, index=category_names)

# results_obj.to_csv('Similarities/similarities_objective.csv')
print(results_obj)
print(f"smc_mean_matrix: {smc_mean_matrix_obj}")
print(f"jac_mean_matrix: {jac_mean_matrix_obj}")

# pirnt mean of all
print(f"SMC (total) = {np.mean(smc_mean_matrix_obj)}")
print(f"Jaccard (total) = {np.mean(jac_mean_matrix_obj)}")
