from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import mglearn
import numpy as np


# iris데이터셋 load
iris_dataset = load_iris()
print("iris_dataset의 키 : \n", iris_dataset.keys())
print("타깃의 이름 : \n", iris_dataset['target_names'])
print("특성의 이름 : \n", iris_dataset['feature_names'])
print("data의 type : \n", type(iris_dataset['data']))
print("data의 크기 : \n", iris_dataset['data'].shape)

# 훈련 데이터와 테스트 데이터
# 모델 성능을 측정하기위해 이전에 본적이 없는 새로운 데이터 필요
# 이중 75%는 훈련세트 25%는 테스트세트로 분류
X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0) 
print("X_train의 크기", X_train.shape)
print("y_train의 크기", y_train.shape)
print("X_test의 크기", X_test.shape)
print("y_test의 크기", y_test.shape)

# 데이터 살펴보기
# 4개의 특성에 대한 산점도 행렬
# 데이터 포인트의 색은 붓꽃의 품종에 따라 구분
iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
pd.plotting.scatter_matrix(iris_dataframe, c=y_train, figsize=(15,15), 
                           marker = 'o', hist_kwds={'bins' : 20}, s=60, alpha=.8, 
                           cmap=mglearn.cm3)


# knn= 훈련 데이터로 모델을 만들고 새로운 데이터 포인트에 대해 예측하는 알고리즘을 캡슐화한 것
knn = KNeighborsClassifier(n_neighbors=1)
# 훈련 데이터셋으로부터 모델을 만들려면 fit 메서드를 사용
# fit 메서드는 객체 자체를 반환
knn.fit(X_train, y_train)
KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=None, n_neighbors=1, p=2, weights='uniform')

# 예측하기
# 붓꽃 하나의 측정값은 2차원 numpy배열에 행으로 들어감
# scikit-learn은 항상 데이터가 2차원 배열일 것으로 예상
X_new = np.array([[5,2.9,1,0.2]])
print("X_new.shape:",X_new.shape)

# 모델 평가하기
y_pred = knn.predict(X_test)
print("테스트 세트에 대한 예측값:\n", y_pred)
print("테스트 세트의 정확도: {:.2f}".format(np.mean(y_pred == y_test)))
# knn 객체의 score 메서드로도 테스트 세트의 정확도를 계산할수 있다.
print("테스트 세트의 정확도: {:.2f}".format(knn.score(X_test, y_test)))