# Data handling
## 1. Load spectrum into Poky
* `fo` or File | Open...

## 2. Load the peak list
* Navigate to the tab ``Experiments`` (**the main panel**)
* Clik on **⇥** icon to import the resonance list;
* `lt` or Peak | Peak list...
## 3. Read the intensities
* In the **Spectrum Peaks** window: **Options...**, check the box `Data height`

## 4. Export peak list with intensities
* In the same window, **Save...** to save the file.

## 5. Tidying up the file with `pandas`

```python

path = '~/path/to/data' # set correctly

# Reading the data
import pandas as pd
df = pd.read_csv(path, header=0, index_col=None, sep='\s+')

# Restructuring 

df.drop(columns='Height', inplace=True)
df.rename({
    'Assignment': 'label',
    'Data': 'int',
    'w1': 'N',
    'w2': 'Hn',
    'w3': 'H'
}, axis=1, inplace=True)

df.insert(0, 'noe', df.label.apply(lambda s: s.split('-')[-1]))
df.insert(0, 'res', df.label.apply(lambda s: s.split('-')[0]))

df['noe_res'] = df.noe.apply(lambda s: s.split('H')[0])
df.loc[df.noe_res == '', 'noe_res'] = df.loc[df.noe_res == ''].res
df['noe_res'] = df.noe_res.str.strip('N')
df['res'] = df.res.str.strip('N')
df.drop(columns='label', inplace=True)

```
