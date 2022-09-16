import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

fandango = pd.read_csv("fandango_scrape.csv")
print(fandango.head())
print(fandango.info())
print(fandango.describe())
print(sns.scatterplot(data=fandango, y='VOTES', x='RATING'))
print(fandango.corr())
fandango['YEAR'] = fandango['FILM'].apply(lambda title:title.split('(')[-1].replace(')',''))
print(fandango['YEAR'].value_counts())
sns.countplot(data=fandango, x='YEAR')
print(fandango.nlargest(10, 'VOTES'))
print(fandango[fandango['VOTES'] == 0])
fan_reviewed = fandango[fandango['VOTES']>0]
true_rating = sns.kdeplot(data=fan_reviewed, x='RATING', clip=[0,5], fill=True, label='True Rating')
stars_displayed = sns.kdeplot(data=fan_reviewed, x='STARS', clip=[0,5], fill=True, label='Stars Displayed')
plt.legend(loc=(1.05, 0.5))

fan_reviewed['STARS_DIFF'] = fan_reviewed['STARS'] - fan_reviewed['RATING']
fan_reviewed['STARS_DIFF'] = fan_reviewed['STARS_DIFF'].round(1)
print(fan_reviwed)

plt.figure(figsize=(12,4), dpi=150)
sns.countplot(data=fan_reviewed, x='STARS_DIFF', palette='magma')

print(fan_reviewed[fan_reviewed['STARS_DIFF'] == 1])

all_sites = pd.read_csv('all_sites_scores.csv')
print(all_sites.head())
print(all_sites.info())
print(all_sites.describe())

sns.scatterplot(data=all_sites, x='RottenTomatoes', y='RottenTomatoes_User')
plt.ylim(0, 100)
plt.xlim(0, 100)

all_sites['Rotten_Diff'] = all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']
all_sites['Rotten_Diff'].apply(abs).mean()

plt.figure(figsize=(10, 4), dpi=200)
sns.histplot(data=all_sites, x='Rotten_Diff', kde=True, bins=25)

plt.figure(figsize=(10, 4), dpi=200)
sns.histplot(data=all_sites, x=all_sites['Rotten_Diff'].apply(abs), kde=True, bins=25)

print(all_sites.nsmallest(10, 'Rotten_Diff'))
print(all_sites.nlargest(10, 'Rotten_Diff'))

sns.scatterplot(data=all_sites, x='Metacritic', y='Metacritic_User')
plt.ylim(0, 10)
plt.xlim(0, 100)

sns.scatterplot(data=all_sites, x='Metacritic_user_vote_count', y='IMDB_user_vote_count')
all_sites.nlargest(1, 'IMDB_user_vote_count')
all_sites.nlargest(1, 'Metacritic_user_vote_count')

df = pd.merge(fandango, all_sites, on='FILM', how='inner')
df['RT_Norm'] = np.round(df['RottenTomatoes']/20, 1)
df['RTU_Norm'] = np.round(df['RottenTomatoes_User']/20, 1)
df['Meta_Norm'] = np.round(df['Metacritic']/20, 1)
df['Meta_U_Norm'] = np.round(df['Metacritic_User']/2, 1)
df['IMDB_Norm'] = np.round(df['IMDB']/2, 1)

norm_scores = df[['RATING', 'STARS', 'RT_Norm', 'RTU_Norm', 'Meta_Norm', 'Meta_U_Norm', 'IMDB_Norm']]
plt.figure(figsize=(15, 6), dpi=200)
sns.kdeplot(data=norm_scores, clip=[0, 5], shade=True, palette='Set1')

sns.clustermap(norm_scores, cmap='magma', col_cluster=False)

norm_films = df[['FILM', 'STARS', 'RATING', 'RT_Norm', 'RTU_Norm', 'Meta_Norm', 'Meta_U_Norm', 'IMDB_Norm']]
worst_films = norm_films.nsmallest(10, 'RT_Norm')
plt.figure(figsize=(15, 6), dpi=200)
sns.kdeplot(data=worst_films, clip=[0, 5], shade=True, palette='Set1')



