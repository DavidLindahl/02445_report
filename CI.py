from SMC_jaccard_obj import *
from SMC_jaccard_sub import *
from scipy import stats
<<<<<<< HEAD
import seaborn as sns
import matplotlib.pyplot as plt
=======
"""Defining a function that calculates the confidence interval for a given data set via bootstrapping:"""
def confidence_interval(data , n=10000):
    # Create bootstrap samples
    bootstrap_estimates = np.random.choice(data, size=(n, len(data)), replace=True)
    
    # Calculate the mean of each bootstrap sample
    bootstrap_means = np.mean(bootstrap_estimates, axis=1)
>>>>>>> 9eae3ba29f6e4b58ca54992e0f078e86930a5465

    # Finding the mean accuracy:
    mean_bootstrap = np.mean(bootstrap_estimates)
    
    # Find the quantiles
    lower_index = int(n * 0.025)
    upper_index = int(n * 0.975)

    # Find the lower and upper bound
    lower_bound = np.sort(bootstrap_means)[lower_index]
    upper_bound = np.sort(bootstrap_means)[upper_index]

    # Cleaning up result for display
    lower_bound = float(round(lower_bound, 3))
    upper_bound = float(round(upper_bound, 3))

<<<<<<< HEAD
mean_JAC_sub = np.mean(jac_mean_matrix_sub)
CI_lower = mean_JAC_sub - 1.96 * np.std(jac_mean_matrix_sub) / np.sqrt(count)
CI_higher = mean_JAC_sub + 1.96 * np.std(jac_mean_matrix_sub) / np.sqrt(count)
CI_Jac_sub = [CI_lower, CI_higher]
print(f"CI for subjective SMC: {CI_SMC_sub}")
print(f"CI for subjective JAC: {CI_Jac_sub}")

=======
    # Store the confidence interval as mean and error
    mean = float(np.mean(data))
    error = (upper_bound - lower_bound) / 2

    # The list of upper and lower bound for checking if its the same
    CI = [lower_bound, upper_bound]
    
    # Clean up data for display
    mean = float(round(mean, 3))
    error = float(round(error, 3))
    # CHECK
    # print(f"Lower bound: {lower_bound}")
    # print(f"mean - error: {mean-error}")
    # print(f"Upper bound: {upper_bound}")
    # print(f"mean + error: {mean+error}")
    return mean, error 


# Calculating the CI's
smc_obj_mean , smc_obj_error = confidence_interval(smc_mean_matrix_obj)
jac_obj_mean , jac_obj_error = confidence_interval(jac_mean_matrix_obj)
smc_sub_mean , smc_sub_error = confidence_interval(smc_mean_matrix_sub)
jac_sub_mean , jac_sub_error = confidence_interval(jac_mean_matrix_sub)

# Displaying the results
print(f"SMC objective mean: {smc_obj_mean} +- {smc_obj_error}")
print(f"Jaccard objective mean: {jac_obj_mean} +- {jac_obj_error}")
print(f"SMC subjective mean: {smc_sub_mean} +- {smc_sub_error}")
print(f"Jaccard subjective mean: {jac_sub_mean} +- {jac_sub_error}")

# 
>>>>>>> 9eae3ba29f6e4b58ca54992e0f078e86930a5465
