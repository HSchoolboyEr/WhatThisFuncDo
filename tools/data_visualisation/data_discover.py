import pandas as pd
import matplotlib.pyplot as plt




file_with_data = '../../data/extracted.csv'


data = pd.read_csv(file_with_data, sep=';' )


# All the data
print(data.describe(include=object))
#print(data.info())

# Only unic
subset = data[["func_class", "name_hash", "instructions_count", "func_body"]]
subset = subset.drop_duplicates()
print(subset.describe(include=object))

# Class visualization
subset['Inicator']=1
subset_classes = subset.groupby("func_class")["Inicator"].sum().sort_values()
subset_classes.plot(kind="bar", title='Funcs by class distribution')
plt.savefig('./images/classes.png')


# Len function visualization
plt.clf()
subset_classes = subset.groupby("instructions_count")["Inicator"].sum().sort_values()
subset_classes.plot(kind="line", title='Funcs by len')
plt.savefig('./images/funcs_len.png')