"""
File: plot.py

Code to to generate the plots for the project report.
"""
import matplotlib.pyplot as plt
import numpy as np

# below is the data for part (a) and (b), averaged over 20 randomly generated problems for each point.
# x is the problem size, y is the computing time, n is the number of nodes generated.
x = np.array([8, 12, 16, 20, 24])
# h_walldist
y1 = np.array([0.010374783199586091, 0.06544338344974676, 0.14597477499992237, 0.6088566783997521, 1.0874630420490576]) * 1000
n1 = np.array([37.55, 60.85, 61.85, 82.4, 88.35])
# h_esdist
y2 = np.array([0.001415594249192509, 0.02002446470069117, 0.002815230300620897, 0.043336003450167485, 0.40165125750027075]) * 1000
n2 = [40.85, 194.3, 58.85, 256.95, 909.85]
# h_ff1
y3 = np.array([0.3369837608006492, 4.206829176750034, 6.02416122734976, 28.63509017940014, 381.8717957163488]) * 1000
n3 = np.array([46.0, 78.35, 92.5, 114.15, 595.45])
# h_ff2
y4 = np.array([0.2653194476992212, 4.404304621949995, 5.444547857249927, 38.59250353819989, 225.53510610665035]) * 1000
n4 = np.array([54.0, 67.6, 100.8, 129.85, 161.65])


# below we will generate a plot of computing time vs. problem size, for part (a) of the report
plt.plot(x, y1, label="h_walldist")
plt.plot(x, y2, label="h_esdist")
plt.plot(x, y3, label="h_ff1")
plt.plot(x, y4, label="h_ff2")

# Now add the legend with some customizations.
legend = plt.legend(loc='lower right', shadow=True)

# set the legend font size
for label in legend.get_texts():
    label.set_fontsize('small')

# set the legend line width
for label in legend.get_lines():
    label.set_linewidth(1.5)

plt.xlabel("problem size")
plt.ylabel("computing time (milliseconds)")
plt.yscale('log')
plt.title('computing time vs. problem size')
plt.grid(True)
plt.savefig("fig_a")
plt.show()


# below we will generate a plot of computing time vs. problem size, for part (b) of the report
plt.plot(x, n1, label="h_walldist")
plt.plot(x, n2, label="h_esdist")
plt.plot(x, n3, label="h_ff1")
plt.plot(x, n4, label="h_ff2")

# Now add the legend with some customizations.
legend = plt.legend(loc='lower right', shadow=True)

# set the legend font size
for label in legend.get_texts():
    label.set_fontsize('small')

# set the legend line width
for label in legend.get_lines():
    label.set_linewidth(1.5)

plt.xlabel("problem size")
plt.ylabel("number of generated nodes")
plt.yscale('log')
plt.title('# generated nodes vs. problem size')
plt.grid(True)
plt.savefig("fig_b")
plt.show()


# Below we generate the scatter plot for part(c), using the given sample problems.
# problems=(wall8a wall8b rectwall8 rhook16a rhook16b spiral16 rectwall16 lhook16
# rect20a rect20b rect20c rect20d rect20e spiral24 pdes30 pdes30b rect50)
x = np.array([43, 47, 47, 142, 142, 146, 115, 114, 109, 109, 91, 91, 91, 222, 86, 96, 136])
y = np.array([105, 202, 120, 460, 827, 733, 634, 1247, 190, 190, 199, 226, 127, 1596, 127, 250, 163])
plt.scatter(x, y, s=40)
plt.xlabel("number of nodes GBFS generated using h_walldist")
plt.ylabel("number of nodes GBFS generated using h_ff2")
plt.title('h_walldist vs. h_ff2')
plt.grid(True)
plt.savefig('fig_c')
plt.show()
