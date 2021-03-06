import numpy as np
import pandas as pd

class feature():

    def __init__(self,df,variable):

        self.df = df
        self.variable = variable 

    def feature_zero(self):

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),0,
            self.df[self.variable]
        )
        return self.df[self.variable].isnull().mean()

    def feature_mean(self):

        mean = self.df[self.variable].mean()

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),
            mean,
            self.df[self.variable]
        )
        return self.df[self.variable].isnull().mean()

    def feature_mod(self):

        mod = self.df[self.variable].mode()

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),
            mod,
            self.df[self.variable]
        )

        return self.df[self.variable].isnull().mean()

    def feature_median(self):

        median = self.df[self.variable].median()

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),
            median,
            self.df[self.variable]
        )
    
        return self.df[self.variable].isnull().mean()
    
    def arbitary_value(self,value):

        self.df[self.variable] = np.where(
            self.df[self.variable].isnull(),
            value,
            self.df[self.variable]
        )
        print(f"Missing Values fill {value}")

        return self.df[self.variable].isnull().mean()

    def missing_feature(self,nan_cols):

        if len(nan_cols) > 1:

            for cols in nan_cols:
                
              self.df[cols + '_nan'] = np.where(
              self.df[cols].isnull(),1,0)
            miss_id = [cols for cols in self.df.columns if 'nan' in cols]
            
            return self.df[miss_id]
        
        else:
            self.df['missing_indicator'] = np.where(self.df[self.variable].isnull(),1,0)

            return self.df[[self.variable,'missing_indicator']]

    def feature_dist(self, dag??l??m, distance = 3, low_up = 'up'):

        if dag??l??m == 'normal':

            mean = self.df[self.variable].mean()
            std = self.df[self.variable].std()
            result = np.add(mean, np.multiply(3,std))

            self.df[self.variable] = np.where(
                self.df[self.variable].isnull(),
                result,
                self.df[self.variable]
            )
        if dag??l??m == 'carp??k':

            Q1 = self.df[self.variable].quantile(0.25)
            Q3 = self.df[self.variable].quantile(0.75)
            IQR = distance * (Q3 - Q1)

            lower = Q1 - IQR
            upper = Q3 + IQR

            if low_up == 'low':

                self.df[self.variable] = np.where(
                    self.df[self.variable].isnull(),
                    lower,
                    self.df[self.variable]
                )
            
            if low_up == 'up':

                self.df[self.variable] = np.where(
                    self.df[self.variable].isnull(),
                    upper,
                    self.df[self.variable]
                )
        else:
           print("Please enter correct parameters!")
        return self.df[self.variable].isnull().mean()
    
    def category_feature(self, plot = False):
        """
        - Kategorik de??i??kenlerdeki eksik de??erlerimizi 'eksik' ad??nda de??eri atayaca????z.
        - NaN --> 'Eksik'
        """

        if self.df[self.variable].dtypes == 'object':

            self.df[self.variable] = np.where(

                self.df[self.variable].isnull(),
                'Eksik',
                self.df[self.variable]

            )
            return self.df[self.variable].isnull().mean()
            
        else:
            print(f"{self.variable} de??i??kenin tipi 'object' de??ildir!")
        
        if plot:

            return self.df[self.variable].value_counts().plot().bar()


    def random_sample(self,cols):
        
        self.df[cols + '_imputed'] = self.df[cols].copy()

        random_sample = self.df[cols].dropna().sample(self.df[cols].isnull().sum(),random_state = 0)

        random_sample.index = self.df[self.df[cols].isnull()].index
        
        self.df.loc[self.df[cols].isnull(), [cols + '_imputed']] = random_sample

        return self.df[[cols, cols + '_imputed']]

    "------------------------------ Encoding ????lemleri ----------------------------------------------"

    def OneHotEncoder(self, cols, drop_cols = False):

        value = self.df[cols].unique()
        
        for i in value:

            self.df[i] = np.where(

                self.df[cols].isin([i]),1,0
            )

        if drop_cols == True:

            self.df.drop(i, axis=1, inplace = True)
        
        return self.df
    
    def LabelEncoder(self,cols):

        value = self.df[cols].unique()

        count = 0

        for i in value:

            self.df[cols] = np.where(self.df[cols] == i, 
                count,
                self.df[cols]
            )
            count +=1

        return self.df

    def top_features_ohe(self,cols, number = 10 ,show_top10 = False):

        """
        - Kategorik De??i??kenimizin de??erlerinin top 10 de??erlerini alaca????z.
        - Bu de??erlere One hot encoding uygulayaca????z.
        """

        "cols = self.variable"

        top_10 = self.df[cols].value_counts().sort_values(ascending = False).head(int(number)).index
        
        top_10 = [i for i in top_10]

        if show_top10: #De??i??kenin top 10 de??erlerini g??rmek istersek.

            print(f" {cols} De??i??kenin top 10 de??erleri : \n{top_10}")

        for value in top_10:

            self.df[cols + '_' + value] = np.where(
                self.df[cols ] == value, 1, 0
            )

        return self.df[[cols] + [cols + '_' + i for i in top_10]].head(10)

    def ordinary_encoding(self, cols ,show_dict = False):

        """
        - Datam??z??n kategorik de??i??kenlerinin de??erlerini numaraland??r??yoruz.
        - O numalaralar ile o de??i??ken de??erlerini de??i??tiriyoruz.
        - LabelEncoder() i??lemi gibi asl??nda.
        - show_dict = Etiketleri de??i??tirece??imiz say??sal de??erleri g??rmemizi sa??lar

          - False = Say??sal de??erleri g??stermez. Default de??eridir.
          - True = Say??sal de??erleri g??sterir.
        """
        
        cols = self.variable

        ordinal_map = {v:k
            for k,v in enumerate(self.df[cols].unique(),0)
        }
        
        self.df[self.variable] = self.df[cols].map(ordinal_map)

        if show_dict:

            print(ordinal_map)

    def encoding(self, cols, how):

        """
        - Kategorik de??i??kenimizin etiketlerini say??sal de??erlerle,
        - Kategorik de??i??kenimizin etiketlerini frekans de??erleriyle
        de??i??tirebiliriz.
        - how = Etiktlerini ne ile de??i??tirmek istiyorsak onun bilgisini veririz.
           - number = Say??sal De??erler i??in
           - frequency = Frekans De??erler i??in
        """

        if how == 'number':

            ordinal_map = {

                v:k
                for k,v in enumerate(self.df[cols].unique())
            }
            
            self.df[cols] = self.df[cols].map(ordinal_map)

        elif how == 'frequency':

            frekans = (self.df[cols].value_counts() / len(self.df)).to_dict()

            self.df[cols] = self.df[cols].map(frekans)
        
        else :

            print("Please Enter Correct Parameter!")

    def mean_target_encoding(self,cols,target):

        """
        - Kategorinin de??erleri i??in ortalama hedef de??erle de??i??tirilmesi anlam??na gelir.
        - target = Veri Setinde ki Hedef De??i??kenimiz.
        """
        ordered = self.df.groupby(cols)[target].mean().to_dict()

        self.df[cols] = self.df[cols].map(ordered)

    def prob_ratio_encoding(self,cols,target):

        """
        - Bu kodlama yaln??zca target de??i??keninin binary oldu??u durumlarda ger??ekle??ir.
        - Her de??er i??in P(1) ve P(0) de??erleri hesaplan??r.
        - P(1) / P(0) ile dolduruz.
        - target = Veri Setinde ki hedef de??i??kenimiz.De??erleri "Binary" olmak zorunda.
        """

        #Target 1 olma olas??l?????? 
        prob_df = pd.DataFrame(self.df.groupby(cols)[target].mean())

        #target 0 olma olas??l??????
        prob_df['zero'] = 1 - prob_df[target]
        
        #Olas??l??k Oran De??erleri
        prob_df['ratio'] = prob_df[target] / prob_df['zero']

        #Olas??l??k oran de??erlerini dictionary haline ??eviriyoruz.
        prob_ratio = prob_df['ratio'].to_dict()
        
        self.df[cols] = self.df[cols].map(prob_ratio)

    def rare_encoding(self,cols,tolerance,plot = False):

        temp_df = pd.Series(self.df[cols].value_counts() / len(self.df))

        rare_labels = temp_df[temp_df < tolerance].index.tolist()

        for value in rare_labels:

            self.df[cols] = np.where(self.df[cols].isin([value]), 'rare', self.df[cols])

        if plot:

            fig = self.df[cols].value_counts() / len(self.df).plot.bar()

            fig.set_xlabel(cols)
            fig.set_axhline(y = 0.05, color = 'red')
            

        return self.df[cols]

    "------------------------ Ayk??r?? De??er ????lemleri --------------------------------------"
    
    def Outliers_Trimming(self,variable, distance):

        """
        - variable = De??i??ken ??smi. 
        - distance = Ayk??r?? de??erler i??in alt ve ??st s??n??r de??erleri elde ederken ki de??erimiz.
           - IQR = distance * (Q3 - Q1)    
        """ 

        Q1 = self.df[variable].quantile(0.25)
        Q3 = self.df[variable].quantile(0.75)

        IQR = distance * (Q3 - Q1)

        lower = Q1 - IQR
        upper = Q3 + IQR

        self.df[variable] = np.where(self.df[variable] < lower , True,
                            np.where(self.df[variable] > upper, True, False))

        return self.df[variable]

    
    def Outliers_Censoring(self, variable, distance, arbitary = 0):

        """
        - arbitary = De??i??kenimizde ki ayk??r?? de??erleri de??i??tirmek istedi??imiz de??er.
           - default olarak 0'd??r.E??er 0'dan farkl?? de??er girilirse bu de??er ile de??i??tirelecektir.
        - arbitary = 0 olursa yani biz de??er vermezsek;
           - alt ayk??r?? de??erleri, alt s??n??r de??eri ile
           - ??st ayk??r?? de??erleri, ??st s??n??r de??eri ile de??i??tirecektir.
        """

        Q1 = self.df[variable].quantile(0.25)
        Q3 = self.df[variable].quantile(0.75)

        IQR = distance * (Q3 - Q1)

        lower = Q1 - IQR
        upper = Q3 + IQR

        if arbitary != 0 :

            self.df[variable] = np.where(self.df[variable] < lower, arbitary,
                            np.where(self.df[variable] > upper,arbitary,self.df[variable]))

        else:

            self.df[variable] = np.where(self.df[variable] < lower, lower,
                            np.where(self.df[variable] > upper, upper, self.df[variable]))

        return self.df[variable]
    
    def Outliers_Gauss(self, variable, distance = 3):

        lower = self.df[variable].mean() - distance * self.df[variable].std()

        upper = self.df[variable].mean() + distance * self.df[variable].std()

        self.df[variable] = np.where(self.df[variable] < lower, lower,
                            np.where(self.df[variable] > upper, upper, self.df[variable]))

        return self.df[variable]

        

     






