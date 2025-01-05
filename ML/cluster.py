import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("output.csv")
print(df['Detected Barcodes'].value_counts())


