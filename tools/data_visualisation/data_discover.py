import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from collections import Counter





file_with_data = '../../data/extracted.csv'








def instruction_count(df):
    asm_instructions_counter = Counter()
    for asm_line in df:
        line_code =  [line.strip().strip("'") for line in str(asm_line).split(',')]
        asm_instructions_counter.update(Counter(line_code))
    return asm_instructions_counter





data = pd.read_csv(file_with_data, sep=';' )
# # All the data
# print(data.describe(include=object))
# print(data.info())




# # Only unic
subset = data[["func_class", "name_hash", "instructions_count", "func_body"]]
subset = subset.drop_duplicates()
# print(subset.describe(include=object))
#



# # Class visualization
sb.set_style("whitegrid")
subset['Inicator']=1
subset_classes = subset.groupby("func_class")["Inicator"].sum().sort_values(ascending=False).to_frame().T
pl = sb.barplot(data=subset_classes)
pl.set_title('Count functions in classes distribution', fontdict={'fontsize':18}, pad=12)
pl.set_xlabel("Functions classes", fontsize=14)
pl.set_xticklabels(pl.get_xticklabels(),rotation = 30, ha='right')
plt.tight_layout()
plt.savefig('./images/classes.png')






# # Len function visualization
plt.clf()
subset_classes = subset.groupby("instructions_count")["Inicator"].sum().sort_values().to_frame()
pl = sb.lineplot(data=subset_classes, legend=False)
pl.set_title('Funcs by len distribution', fontdict={'fontsize':18}, pad=12)
pl.set_xlabel("Count of instructions (function len)", fontsize=14)
plt.savefig('./images/funcs_len.png')



## Instructions distribution
subset_instructions = subset["func_body"]
ct = instruction_count(subset_instructions)
asm_inst_df = pd.DataFrame(ct.most_common(50))
asm_inst_df.columns = ["x", "y"]

plt.clf()
sb.set_theme(style="whitegrid")
f, ax = plt.subplots(figsize=(6.5, 15))
sb.set_color_codes("pastel")
pl = sb.barplot(data=asm_inst_df, x= "y", y = "x",  label="Total", color="b")
pl.set_xlabel("Times of use", fontsize=14)
pl.set_title('Top-50 most used instructions\n and commands (not precleaned)', fontdict={'fontsize':18}, pad=12)
plt.savefig('./images/instructions_distribution.png')















