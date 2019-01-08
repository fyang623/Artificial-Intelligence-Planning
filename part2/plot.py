"""
File: plot.py

Code to to generate the plots for the project report.
"""
import matplotlib.pyplot as plt
import numpy as np

# x = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0])
# y1 = np.array([27.22, 26.62, 27.14, 26.40, 26.70, 27.02, 26.80, 26.52, 26.90, 26.94, 26.32, 26.84, 26.54, 26.32, 26.36, 26.52, 26.18, 26.30, 25.92, 26.24, 25.80, 25.74, 25.80, 25.70])
# y2 = np.array([29.64, 29.90, 29.92, 30.12, 30.04, 30.24, 30.20, 29.75, 30.02, 30.22, 30.16, 30.10, 29.22, 29.10, 29.48, 29.36, 29.12, 28.90, 29.02, 29.16, 29.20, 29.30, 28.88, 28.94])
# y3 = np.array([10.50, 10.88, 11.02, 10.98, 10.46, 10.84, 10.94, 10.34, 10.70, 10.40, 10.24, 10.78, 10.18, 10.04, 10.20, 10.10, 10.14, 10.32, 10.02, 10.44, 10.20, 10.52, 10.16, 10.08])
# y4 = np.array([11.38, 11.84, 11.96, 12.00, 11.52, 11.96, 11.82, 11.76, 12.02, 10.70, 10.88, 11.40, 12.04, 11.78, 11.10, 11.22, 10.94, 11.24, 10.88, 11.30, 10.72, 10.88, 10.74, 10.90])
#
# plt.plot(x, y1, label="spiral16")
# plt.plot(x, y2, label="spiral24")
# plt.plot(x, y3, label="pdes30")
# plt.plot(x, y4, label="rect50")
#
# # Now add the legend with some customizations.
# legend = plt.legend(loc='center right', shadow=True)
#
# # set the legend font size
# for label in legend.get_texts():
#     label.set_fontsize('small')
#
# # set the legend line width
# for label in legend.get_lines():
#     label.set_linewidth(1.5)
#
# plt.xlabel("search time")
# plt.ylabel("number of moves")
# plt.title('LAO*\nnumber of moves vs. search time')
# plt.grid(True)
# plt.savefig('fig1')
# plt.show()

# x = np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
# p1 = np.array([0.08,0.02,0.06,0,0.02,0,0,0,0,0])
# p2 = np.array([0.18,0.18,0.12,0.06,0.06,0.02,0.04,0,0,0])
# p3 = np.array([0.14,0.10,0.08,0.04,0.06,0,0,0,0,0])
# p4 = np.array([0.10,0.02,0.04,0.04,0,0,0,0,0,0])
#
# plt.plot(x, p1, label="spiral16")
# plt.plot(x, p2, label="spiral24")
# plt.plot(x, p3, label="pdes30")
# plt.plot(x, p4, label="rect50")
#
# # Now add the legend with some customizations.
# legend = plt.legend(loc='center right', shadow=True)
#
# # set the legend font size
# for label in legend.get_texts():
#     label.set_fontsize('small')
#
# # set the legend line width
# for label in legend.get_lines():
#     label.set_linewidth(1.5)
#
# plt.xlabel("search time")
# plt.ylabel("probability of crashing")
# plt.title('LAO*\nprobability of crashing vs. search time')
# plt.grid(True)
# plt.savefig('fig2')
# plt.show()


# x = np.array([0.10, 0.20, 0.30, 0.40, 0.50, 0.75, 1.00, 1.50, 2.00])
# p1 = np.array([1.00, 0.82, 0.10, 0.00, 0.04, 0.0, 0.02, 0.00, 0.00])
# p2 = np.array([1.00, 1.00, 1.00, 1.00, 0.94, 1.00, 0.90, 0.00, 0.00])
# p3 = np.array([1.00, 1.00, 1.00, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00])
# p4 = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 0.32, 0.00, 0.02, 0.00])
#
# plt.plot(x, p1, label="spiral16")
# plt.plot(x, p2, label="spiral24")
# plt.plot(x, p3, label="pdes30")
# plt.plot(x, p4, label="rect50")
#
# # Now add the legend with some customizations.
# legend = plt.legend(loc='center right', shadow=True)
#
# # set the legend font size
# for label in legend.get_texts():
#     label.set_fontsize('small')
#
# # set the legend line width
# for label in legend.get_lines():
#     label.set_linewidth(1.5)
#
# plt.xlabel("search time")
# plt.ylabel("probability of crashing")
# plt.title('UCT\nprobability of crashing vs. search time')
# plt.grid(True)
# plt.savefig('fig3')
# plt.show()


# x1 = np.array([0.3, 0.4, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
# y1 = np.array([38.6, 39.2, 51.6, 42.3, 37.8, 44.5, 43.2, 39.2, 33.7, 36.2, 34.1, 31.00, 30.5, 33.1, 32.4, 30.0, 29.4])
# x2 = np.array([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
# y2 = np.array([43.0, 47.1, 37.6, 50.1, 40.0, 40.9, 34.8, 38.0, 35.4, 39.1, 36.0, 37.0, 35.0])
# x3 = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
# y3 = np.array([24.0, 16.9, 19.2, 18.0, 15.4, 17.5, 18.7, 15.9, 16.6, 19.1, 16.0, 17.2, 15.4, 16.0, 15.4])
# x4 = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
# y4 = np.array([34.5, 37.4, 32.2, 27.0, 21.1, 26.2, 19.7, 22.4, 20.6, 19.1, 17.9, 17.8, 16.6, 19.8])
#
# plt.plot(x1, y1, label="spiral16")
# plt.plot(x2, y2, label="spiral24")
# plt.plot(x3, y3, label="pdes30")
# plt.plot(x4, y4, label="rect50")
#
# # Now add the legend with some customizations.
# legend = plt.legend(loc='upper right', shadow=True)
#
# # set the legend font size
# for label in legend.get_texts():
#     label.set_fontsize('small')
#
# # set the legend line width
# for label in legend.get_lines():
#     label.set_linewidth(1.5)
#
# plt.xlabel("search time")
# plt.ylabel("number of moves")
# plt.title('UCT\nnumber of moves vs. search time')
# plt.grid(True)
# plt.savefig('fig4')
# plt.show()

x = np.array([6.85, 9.7, 11.65, 20.75, 21.55, 27.25, 15.50, 18.50, 7.25, 7.25, 7.25, 6.85, 7.05, 31.25, 12.0, 14.7, 11.95])
y = np.array([6.85, 9.85, 13.2, 25.55, 27.20, 33.00, 18.55, 18.05, 8.55, 8.20, 8.45, 7.90, 7.75, 35.00, 15.0, 19.2, 16.6])

m, b = np.polyfit(x, y, 1)
plt.scatter(x, y, s=40)
plt.plot(x, m*x + b, '-')
plt.xlabel("number of moves using LAO*")
plt.ylabel("number of moves using UCT")
plt.title('UCT vs. LAO*')
plt.grid(True)
plt.savefig("fig5")
plt.show()
