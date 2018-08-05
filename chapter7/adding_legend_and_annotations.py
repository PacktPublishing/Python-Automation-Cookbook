import matplotlib.pyplot as plt

# STEP 2
LEGEND = ('ProductA', 'ProductB', 'ProductC')
DATA = (
    ('Q1 2017', 100, 30, 3),
    ('Q2 2017', 105, 32, 15),
    ('Q3 2017', 125, 29, 40),
    ('Q4 2017', 115, 31, 80),
)

# STEP 3
POS = list(range(len(DATA)))
VALUESA = [valueA for label, valueA, valueB, valueC in DATA]
VALUESB = [valueB for label, valueA, valueB, valueC in DATA]
VALUESC = [valueC for label, valueA, valueB, valueC in DATA]
LABELS = [label for label, valueA, valueB, valueC in DATA]

# STEP 4
WIDTH = 0.2
valueA = plt.bar([p - WIDTH for p in POS], VALUESA, width=WIDTH)
valueB = plt.bar([p for p in POS], VALUESB, width=WIDTH)
valueC = plt.bar([p + WIDTH for p in POS], VALUESC, width=WIDTH)
plt.ylabel('Sales')
plt.xticks(POS, LABELS)

# STEP 5
plt.annotate('400% growth', xy=(1.2, 18), xytext=(1.3, 40),
             horizontalalignment='center',
             fontsize=9,
             arrowprops={'facecolor': 'black',
                         'arrowstyle': "fancy",
                         'connectionstyle': "angle3",
                         })

# STEP 6
# Draw the legend outside the plot
plt.legend(LEGEND, title='Products', bbox_to_anchor=(1, 0.8))
plt.subplots_adjust(right=0.80)

# STEP 6
plt.show()
