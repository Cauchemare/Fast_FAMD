# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 10:39:04 2019

@author: luyao.li
"""

from .fast_MFA  import MFA
import pandas as pd
import numpy as np

class  FAMD(MFA):
    def __init__(self,n_components=2,svd_solver='auto',copy=True,
             tol=None,iterated_power=2,batch_size =None,random_state=None):
        super().__init__(
                         n_components=n_components,
                         svd_solver=svd_solver,
                         copy=copy,
                         tol=tol,
                         iterated_power=iterated_power,
                         batch_size =batch_size,
                         random_state=random_state)   
    
    def fit(self,X,y=None):
        if not isinstance(X,(pd.DataFrame,pd.SparseDataFrame)):
            X=pd.DataFrame(X) 
        _numric_columns= X.select_dtypes(include=np.number).columns
        _category_columns=X .select_dtypes(include=['object','category']).columns
        self.groups= {'Numerical':_numric_columns ,'Categorical':_category_columns }
        
        return  super().fit(X)
    
if  __name__ =='__main__':
    
#    1)
#  File "E:\1113蓝海数据建模\fast_FAMD\fast_MFA.py", line 29, in fit
#    check_array(X,dtype=[six.string_types,np.number])
#    TypeError: data type not understood:
#        six.string_types -> tuple( str,) :six.string_types[0]
#    
#    2)
#
#AttributeError: 'FAMD' object has no attribute 'n_iter':iterated_power
#3)X.select_dtypes(include=np.number).columns -> empty Int64Index:
#    X = pd.DataFrame( np.random.randint(0,1000,size=(10000,500)) ,dtype=int)
#    test_arr=pd.DataFrame( np.random.choice(list('abcd'),size=(10000,100),replace=True),dtype=str) 
#    test_X= pd.concat([X,test_arr],axis=1,ignore_index=True)
#4)   
#  File "E:\1113蓝海数据建模\fast_FAMD\outils.py", line 24, in fit
#    self.column_names_ = self.get_feature_names(X.columns if hasattr( X,'columns') else None)
#
#  File "C:\Users\admin\Anaconda3\lib\site-packages\sklearn\preprocessing\_encoders.py", line 707, in get_feature_names
#    input_features[i] + '_' + six.text_type(t) for t in cats[i]]
#
#  File "C:\Users\admin\Anaconda3\lib\site-packages\sklearn\preprocessing\_encoders.py", line 707, in <listcomp>
#    input_features[i] + '_' + six.text_type(t) for t in cats[i]]
#
#TypeError: ufunc 'add' did not contain a loop with signature matching types dtype('<U21') dtype('<U21') dtype('<U21')         
#原因在于 原始变量名为 int ,dtype('<U32')是字符串格式:
#将所有变量名转化为 str 
#
#5)
#  File "E:\1113蓝海数据建模\fast_FAMD\fast_MFA.py", line 78, in _X_global
#    X_global.append( X_partial / self.partial_factor_analysis_[name].singular_values[0]  )
#    TypeError: Could not operate 0.10558250376496033
#    with block values unsupported operand type(s) for /: 'str' and 'float'
#    X_partial 可以为str values:
#
#        if self.partial_factor_analysis_[name].__class__.__name__ =='PCA':
#                X_partial=  self.partial_factor_analysis_[name].scaler_.transform(X_partial)
#        else:
#                X_partial=self.partial_factor_analysis_[name].one_hot.transform(X_partial)
# 10000* 30 -> 50000 * 600 
    '''
(50000, 600) 600: 500 +100
Timer famd:39.4323 s
Timer correlation:12.1603 s
Timer transform:8.2285 s

(60000, 600) memory usage: 469.2 MB
Timer famd:47.0902 s
Timer correlation:14.4382 s
Timer transform:10.3434 s

(70000, 600) memory usage: 547.4 MB
Timer famd:87.0762 s
Timer correlation:17.1219 s
Timer transform:12.0020 s

(80000, 600) memory usage:  625.6 MB
Timer famd:89.6859 s
Timer correlation:19.3034 s
Timer transform:12.6420 s

(100000, 600) memory usage:   782.0 MB
Timer famd:111.9764 s
Timer correlation:23.8569 s

Timer transform:16.5418 s




(50000, 800) 600+200 :memory usage: 705.7 MB
Timer famd:85.4954 s
Timer correlation:26.4825 s
Timer transform:17.5998 s


 
    '''

        
                          
