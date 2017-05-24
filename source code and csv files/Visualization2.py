import sys
import csv
import numpy as np
import scipy.stats as ss
import pandas as pd
import random
import matplotlib.pyplot as plt
# from sklearn.cross_validation import train_test_split
from sklearn import cluster as Kcluster, metrics as SK_Metrics
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap,MDS
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import preprocessing as pre
from sklearn import preprocessing
from scipy.stats import zscore

def adaptive_sampling(data_frame, cluster_count,fraction):
    k_means = Kcluster.KMeans(n_clusters=cluster_count)
    print ('k_means before',k_means)
    k_means.fit(data_frame)
    print ('k_means after',k_means)
    data_frame['label'] = k_means.labels_
    print ('label',k_means.labels_)
    adaptiveSampleRows = []
    for i in range(cluster_count):
        adaptiveSampleRows.append(data_frame.ix[random.sample(data_frame[data_frame['label'] == i].index, (int)(len(data_frame[data_frame['label'] == i])*fraction))])
    
    adaptiveSample = pd.concat(adaptiveSampleRows)
    del adaptiveSample['label']

return adaptiveSample


def random_sampling(data_frame, fraction):
    rows = random.sample(data_frame.index, (int)(len(data_frame)*fraction))
    return data_frame.ix[rows]

def determine_pca(data_frame,type):
    data_frame = data_frame.as_matrix()
    kArr = list(xrange(17))
    # kArr.pop(0)
    pca = PCA(n_components=2)
    print (pca)
    print "DATA",data_frame
    pca.fit_transform(data_frame)
    print "Eigen vectors ",pca.components_

    print "Eigens ",len(pca.components_)

    print "After performing eigen"

    temp = []
    for i in range(0,17):
        temp.append(pca.components_[0][i] * pca.components_[0][i] + pca.components_[1][i] * pca.components_[1][i])

    print "temp ",temp,len(temp)
    objects = ('stateur','statemb','state','age','tenure','yrdispl','rr','NumericHead','Numericnwhite','Numericnschool12','Numericsex','Numericbluecol','Numericsmsa','Numericmarried', 'Numericdkids','Numericdykids','Numericui')
    screeDataFrame =  pd.DataFrame({'PCA_components' : objects})
    screeDataFrame['eigen_value'] = temp
        # sample.to_csv(file_name, sep=',')
    if type == 1:
        screeDataFrame.to_csv('randomscreeplt.csv', sep=',')
    else:
        screeDataFrame.to_csv('adaptivescreeplt.csv', sep=',')#adaptivescreeplt
    print "variance ",pca.explained_variance_
    return pd.DataFrame(pca.fit_transform(data_frame))


def find_Elbow_Point(data_frame):
    sse = []
    maxK = 18
    minInertia = 10000000000000
    minK = 0
    kArr = list(xrange(21))
    kArr.pop(0)
    inertiaArr= []
    print kArr

    for k in range(1,21):
        # sse[k] = 0
        k_means = Kcluster.KMeans(n_clusters=k)
        k_means.fit(data_frame)
        clusters = k_means.labels_
        # print ('clusters', clusters)
        inertias = k_means.inertia_
        inertiaArr.append(inertias)
        if(minInertia>inertias):
            minInertia = inertias
            minK = k

        print ('inertia',inertias)
        # print('inertia',inertias/k)
    print ("minK ",minInertia,minK)

    # plt.plot( kArr, inertiaArr,c='blue',label="test1")
    # plt.xticks(np.arange(1, 21, 1.0))
    # plt.show()
    elbowDF =  pd.DataFrame({'KMeans_Score' : inertiaArr})
    elbowDF['Cluster_Count'] = kArr
    elbowDF.to_csv('elbow.csv', sep=',')#adaptivescreeplt



def find_MDS(dataframe, type):
    dis_mat = SK_Metrics.pairwise_distances(dataframe, metric = type)
    mds = MDS(n_components=2, dissimilarity='precomputed')
    return pd.DataFrame(mds.fit_transform(dis_mat))

data_directory = "/Users/karanmalhotra/Downloads/"
def create_File(random_sample, adaptive_sample, file_name):
    # print "random ",random_sample
    # print "adaptive ",adaptive_sample
    # random_sample['type'] = 1
    # adaptive_sample['type'] = 2
    random_sample.columns = ["r1","r2"]
    adaptive_sample.columns = ["a1","a2"]

    sample = random_sample.join([adaptive_sample])

    file_name = data_directory + file_name
    sample.to_csv(file_name, sep=',')



def calculate_values(random_sample, adaptive_sample,function,file_name):
    create_File(function(random_sample,1), function(adaptive_sample,2),file_name +".csv")


def Apply_Normalization(dataFrame):
    # dataFrame = dataFrame.apply(zscore)
    # return dataFrame
    min_max_scaler = preprocessing.StandardScaler()
    np_scaled = min_max_scaler.fit_transform(dataFrame)
    df_normalized = pd.DataFrame(np_scaled)
    return df_normalized

def main():
    benefitDF =  pd.read_csv("/Users/karanmalhotra/Downloads/Benefits.csv")
    precision = 3
    benefitDF['rr'] = benefitDF['rr'].round(decimals = precision)
    # print benefitDF['rr']


    # print ('stateur',type(benefitDF['stateur'][0]))
    # print ('statemb',type(benefitDF['statemb'][0]))
    # print ('state',type(benefitDF['state'][0]))
    # print ('age',type(benefitDF['age'][0]))
    # print ('tenure',type(benefitDF['tenure'][0]))
    # print ('joblost',type(benefitDF['joblost'][0]))
    # print ('nwhite',type(benefitDF['nwhite'][0]))
    # print ('school12',type(benefitDF['school12'][0]))
    # print ('sex',type(benefitDF['sex'][0]))
    # print ('bluecol',type(benefitDF['bluecol'][0]))
    # print ('smsa',type(benefitDF['smsa'][0]))
    # print ('married',type(benefitDF['married'][0]))
    # print ('dkids',type(benefitDF['dkids'][0]))
    # print ('dykids',type(benefitDF['dykids'][0]))
    # print ('yrdispl',type(benefitDF['yrdispl'][0]))
    # print ('rr',type(benefitDF['rr'][0]))
    # print ('head',type(benefitDF['head'][0]))
    # print ('ui',type(benefitDF['ui'][0]))

    benefitDF['NumericHead'] = pd.Categorical(benefitDF['head']).codes
    # print "head  ",benefitDF['head']
    benefitDF['Numericnwhite'] = pd.Categorical(benefitDF.nwhite).codes
    benefitDF['Numericnschool12'] = pd.Categorical(benefitDF.school12).codes
    benefitDF['Numericsex'] = pd.Categorical(benefitDF.sex).codes
    #
    benefitDF['Numericbluecol'] = pd.Categorical(benefitDF.bluecol).codes
    benefitDF['Numericsmsa'] = pd.Categorical(benefitDF.smsa).codes
    # benefitDF['Numericnwhite'] = pd.Categorical.from_array(benefitDF.nwhite).codes
    
    benefitDF['Numericdkids'] = pd.Categorical(benefitDF.dkids).codes
    benefitDF['Numericdykids'] = pd.Categorical(benefitDF.dykids).codes
    # benefitDF['Numerichead'] = pd.Categorical.from_array(benefitDF.head).codes
    benefitDF['Numericui'] = pd.Categorical(benefitDF.ui).codes
    # benefitDF['Numerich'] = pd.Categorical.from_array(benefitDF.head).codes
    benefitDF['Numericmarried'] = pd.Categorical(benefitDF.married).codes
    # print "benefitDF['Numericui']",benefitDF['Numericui']

    benefitDF.pop('joblost')
    benefitDF.pop('nwhite')
    benefitDF.pop('school12')

    benefitDF.pop('sex')
    benefitDF.pop('bluecol')
    benefitDF.pop('smsa')

    benefitDF.pop('married')
    benefitDF.pop('dkids')
    benefitDF.pop('dykids')

    benefitDF.pop('head')
    benefitDF.pop('ui')
    
    # benefitDF.drop(df.columns[[0]], axis=1)
    benefitDF = benefitDF.drop(benefitDF.columns[[0]], axis=1)




     print ((benefitDF))



     sse = []
     maxK = 18
     for k in range(0,maxK):
         adaptive_sample = adaptive_sampling(benefitDF,k, 0.2)

     for (k = 1; k <= maxK; ++k) {
     sse[k] = 0;
     clusters = kmeans(dataset, k);
     clusters.forEach(function(cluster) {
        mean = clusterMean(cluster);
        cluster.forEach(function(datapoint) {
            sse[k] += Math.pow(datapoint - mean, 2);
         });
    });
 }
     benefitDF = Apply_Normalization(benefitDF)
     find_Elbow_Point(benefitDF)
    random_sample = random_sampling(benefitDF, 0.2)
    adaptive_sample = adaptive_sampling(benefitDF,4, 0.2)
    # determine_pca(adaptive_sample)
    # print ((adaptive_sample))
    df2 = (random_sample.ix[:,1:] - random_sample.ix[:,1:].mean()) / random_sample.ix[:,1:].std()
    random_sample = Apply_Normalization(random_sample)
    adaptive_sample = Apply_Normalization(adaptive_sample)



    # calculate_values(random_sample,adaptive_sample,determine_pca,"pca")
   

    # top3_attributes = getTop3attributes(squared_loadings)
    #
    # top3_attributes_index = []
    # for attr in top3_attributes:
    #     index = attributes.index(attr)
    #     top3_attributes_index.append(index)
    #
    # sample_r = random_sample.ix[:, top3_attributes_index]
    #
    # sample_r.columns = [top3_attributes[0],top3_attributes[1],top3_attributes[2]]

    # print ('test', (random_sample))
    benefitSqRandomLoadingDF = benefitDF[['yrdispl', 'NumericHead','Numericmarried']]
    benefitSqAdaptiveLoadingDF = benefitDF[['Numericdykids', 'age','Numericdkids']]
    benefitSqRandomLoadingDF = random_sampling(benefitSqRandomLoadingDF,0.2)
    benefitSqAdaptiveLoadingDF = adaptive_sampling (benefitSqAdaptiveLoadingDF,4,0.2)
    # benefitSqRandomLoadingDF = Apply_Normalization(benefitSqRandomLoadingDF)
    # benefitSqAdaptiveLoadingDF = Apply_Normalization(benefitSqAdaptiveLoadingDF)
    benefitSqRandomLoadingDF.columns = ['yrdispl', 'NumericHead','Numericmarried']
    benefitSqAdaptiveLoadingDF.columns = ['Numericdykids', 'age','Numericdkids']
    print "test",benefitSqRandomLoadingDF
    # random_sample_mat = random_sample[['yrdispl', 'NumericHead','Numericmarried']]
    # adaptive_sample_mat = adaptive_sample[['Numericdykids', 'age','Numericdkids']]
    #
    #
    benefitSqRandomLoadingDF.to_csv("./data2/scatterplot_matrix_random.csv", sep=',')
    benefitSqAdaptiveLoadingDF.to_csv("./data2/scatterplot_matrix_adaptive.csv", sep=',')


    list_mds = ["euclidean","correlation"]
    for type_mds in list_mds:
        print type_mds
        create_File(find_MDS(random_sample,type_mds),find_MDS(adaptive_sample,type_mds),type_mds + ".csv")


main()
