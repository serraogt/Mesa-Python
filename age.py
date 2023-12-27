import numpy as np
import matplotlib.pyplot as plt

# I might use later

# Set the seed for reproducibility
np.random.seed(42)

# Mean and standard deviation for the normal distribution
mean_age = 30
std_dev_age = 5

# Number of people in the group
num_people = 1000

# Generate normally distributed ages within the desired range
ages = np.random.normal(mean_age, std_dev_age, num_people)

# Truncate ages to be within the specified range (18-60)
ages = np.clip(ages, 18, 60)

# Plot a histogram to visualize the distribution
plt.hist(ages, bins=30, density=True, alpha=0.7, color='blue', edgecolor='black')
plt.title('Normally Distributed Ages (18-60) in a Group')
plt.xlabel('Age')
plt.ylabel('Probability Density')
plt.show()
