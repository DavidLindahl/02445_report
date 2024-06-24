from CI import *
import matplotlib.pyplot as plt
from scipy import stats
"""TWO sample independant t-test for objective and subjective:

First we tackle the assumptions:

Normality: Shapiro Wilk's test."""
# Making the shapiro wilk's test
stat_smc_obj , p_value_smc_obj = stats.shapiro(smc_mean_matrix_obj)
stat_jac_obj , p_value_jac_obj = stats.shapiro(jac_mean_matrix_obj)
stat_jac_sub , p_value_jac_sub = stats.shapiro(jac_mean_matrix_sub)
stat_smc_sub , p_value_smc_sub = stats.shapiro(smc_mean_matrix_sub)
print('Shapiro Wilk test for SMC objective:', p_value_smc_obj)
print('Shapiro Wilk test for JAC objective:', p_value_jac_obj)
print('Shapiro Wilk test for JAC subjective:', p_value_jac_sub)
print('Shapiro Wilk test for SMC subjective:', p_value_smc_sub)

plt.hist(smc_mean_matrix_obj)
plt.show()



"""Making the two sample independant t-test for objective and subjective:"""
# Making the t-test
stat_smc , p_value_smc = stats.ttest_ind(smc_mean_matrix_obj, smc_mean_matrix_sub , equal_var = False)
stat_jac , p_value_jac = stats.ttest_ind(jac_mean_matrix_obj, jac_mean_matrix_sub , equal_var = False)
print(f"SMC  p-value: {p_value_smc}")
print(f"JAC p-value: {p_value_jac}")
