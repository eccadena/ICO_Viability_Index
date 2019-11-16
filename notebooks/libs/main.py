#call CMC datafram
import pandas as pd

cmc_df = pd.read_csv("CMC_df.csv")
print(cmc_df.head())

#Insert function to call df2

from apis import get_TrackICOAPI

track_df = get_TrackICOAPI(10)
print(track_df.head())


#OR create 1 function to call both df and concat them


#Insert call to add cmc info to add to df


#Insert twitter sent info to add to df


#Insert news sent info to add to df


#Insert functions to prep df for forrest


#RF Model


#PCA


#NN


#Insert function to call dashboard


#Call dashboard and execute functions

