import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import math
from itertools import combinations


def cats(start, end):
  a = np.array([str(i) for i in range(start, end+1)])
  return list(a.reshape(1,len(a)))

def encode_minute():
  return list(np.array(["0", "15", "30", "45"]).reshape(1,4))


def encode_and_bind(original_dataframe, feature_to_encode, categories):
    original_dataframe = original_dataframe.astype(str)  # pd dummies only works for str input
    enc = OneHotEncoder(categories=categories)

    dummies = enc.fit_transform(original_dataframe[[feature_to_encode]]).toarray()
    dummies = pd.DataFrame(dummies)
    res = pd.concat([original_dataframe, dummies], axis=1)
    del res[feature_to_encode]
    return res


def onehot_build_dataset(data, target):
  df = data.copy()

  for i in [["day", cats(1,31)] , 
            ["month", cats(1,12)], 
            [ "hour", cats(0,23)], 
            [ "weekday", cats(0,6)] , 
            [ "minute" , encode_minute()]]:


    #df = encode_and_bind(df, i[0])
    if i[0] in data.columns:
      df = encode_and_bind(df, i[0], i[1])


  # cols = df.columns.tolist()
  # cols = cols[-1:] + cols[:-1]
  # df = df[cols]
  # df.insert(-1, target, df.pop(target))

  del df[target]
  df[target] = data[target]
  dataset = df.to_numpy(dtype=float)
  print("dataset shape", dataset.shape)
  return dataset

def cyclical_transform(df, col, del_old=False):
  max_value = df[col].max()
  sin_values = [math.sin((2*math.pi*x)/max_value) for x in list(df[col])]
  cos_values = [math.cos((2*math.pi*x)/max_value) for x in list(df[col])]
  df[col + "_sin"] = sin_values
  df[col + "_cos"] = cos_values
  if del_old:
    del df[col]
  return df  

def cyclical_encode_dataset(data, target):

  df = data.copy()

  for i in ["day", "month", "hour", "weekday", "minute"]:
    if i in df.columns:
      df = cyclical_transform(df, i, True)

  del df[target]
  #del df["date"]
  df[target] = data[target]

  dataset = df.to_numpy(dtype=float)

  return dataset, df


def get_feature_combinations(features, target):

  features = features[:-1]
  feature_combinations = []
  for i in range(len(features)):
      oc = combinations(features, i + 1)
      for c in oc:
          l = list(c)
          l.append(target)
          feature_combinations.append(l)

  return feature_combinations