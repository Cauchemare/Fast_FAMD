# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:31:55 2019

@author: luyao.li
"""

from  fast_PCA import PCA
import numpy as np
import pandas as pd

from scipy.sparse import diags,issparse

from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.extmath import safe_sparse_dot

from outils import  _OneHotEncoder




class CA(PCA):
    def __init__(self,n_components=2,svd_solver='auto',copy=True,
                 tol=None,iterated_power=2,batch_size =None,random_state=None):
        super().__init__(
                        standard_scaler=False,
                         n_components=n_components,
                         svd_solver=svd_solver,
                         whiten=False,
                         copy=copy,
                         tol=tol,
                         iterated_power=iterated_power,
                         batch_size =batch_size,
                         random_state=random_state)
        
    def fit(self, X,y=None):
        
        if  isinstance(X,(pd.DataFrame,pd.SparseDataFrame)):
            X=X.values
            
        if np.any(X<0,axis=None):
            raise ValueError('All values in X must be positive')
        

        X = X/np.sum(X)
        
        #compute row and column masses
        self.r_=  np.sum(X,axis=1)
        self.c_= np.sum(X,axis=0)
        
        if issparse(X):
            _S=safe_sparse_dot(diags(self.r_ ** -0.5).toarray(),X- np.outer(self.r_,self.c_) )
            S=safe_sparse_dot(_S,diags(self.c_** -0.5).toarray())
        else:
            _S=np.dot(diags(self.r_ ** -0.5).toarray(),X- np.outer(self.r_,self.c_) )
            S=safe_sparse_dot(_S ,diags(self.c_** -0.5).toarray()  )

        self= super().fit(S)
        
        return self
    
    def transform(self,X):
        if  isinstance(X,(pd.DataFrame,pd.SparseDataFrame)):
            X=X.values
            
        check_is_fitted(self,['mean_','components_'],all_or_any=all)
        check_array(X)   
        
        X =X/ np.sum(X,axis=1)[:,None]
        
        if issparse(X):
            _X=safe_sparse_dot(X,diags(self.c_ ** - 0.5).toarray() )
            X_t=safe_sparse_dot(_X,self.components_.T)
        else:
            X_t= X @ diags(self.c_ ** -0.5).toarray() @ self.components_.T
                    
        return  X_t       
    
    def fit_transform(self,X):
        self.fit(X)
        return self.transform(X)



class MCA(CA):
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
            
        def  fit(self,X,y=None):
            
            n_initial_cols=X.shape[1]
            self.one_hot=_OneHotEncoder().fit(X)
            n_new_cols=len(self.one_hot.column_names_)
            self.total_var = (n_new_cols-n_initial_cols) / n_initial_cols
            
            return super().fit(self.one_hot.transform(X))
            

        
        def transform(self,X,y=None):
            return super().transform( self.one_hot.transform(X))
        
        def column_correlation(self,X,same_input=True):
            return super().column_correlation(self.one_hot.transform(X))
        

if __name__=='__main__':

#    Questions:
#    1) File "E:/1113蓝海数据建模/fast_FAMD/fast_MCA.py", line 44, in fit
#        X/=np.sum(X)
#TypeError: No loop matching the specified signature and casting
#was found for ufunc true_divide:
#            X = X/np.sum(X)
#    2)
#  File "E:/1113蓝海数据建模/fast_FAMD/fast_MCA.py", line 56, in fit
#    S= diags(self.r_ ** -0.5) @ (X- np.outer(self.r_,self.c_))  @diags(self.c_ ** -0.5)
#    MemoryError:
#        _S=np.dot(diags(self.r_ ** -0.5),X- np.outer(self.r_,self.c_) )
#            S=np.dot(_S,diags(self.c_** -0.5))
#    3
#  File "E:/1113蓝海数据建模/fast_FAMD/fast_MCA.py", line 58, in fit
#    S=np.dot(_S ,diags(self.c_** -0.5) ) <class 'numpy.ndarray'> @ <class 'scipy.sparse.dia.dia_matrix'>
#  File "C:\Users\admin\Anaconda3\lib\site-packages\scipy\sparse\base.py", line 439, in __mul__
#    raise ValueError('dimension mismatch')
#ValueError: dimension mismatch:
#    scipy.sparse.dia.dia_matrix =dia_matrix.toarray()



    test_arr=np.random.choice(list('abcd'),size=(10000,400),replace=True)
    mca=MCA()
    mca.fit(test_arr)
    test_arr_t=mca.transform(test_arr)
    assert test_arr_t.shape[1] ==  mca.n_components,ValueError("")
        
            
            
            
        
        
            
        
        