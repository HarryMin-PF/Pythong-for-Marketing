# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:17:07 2021

@author: mhj73
"""

#%%패키지 임포트
import pandas as pd
import numpy as np
import os


#%%데이터 불러오기
#매체 데이터 불러오기
from os import listdir
from os.path import isfile, join

# 일자별로 추출한 페이스북 데이터 파일들을 리스트로 모아줌
facebook_list = [f for f in listdir('C://Users//facebook_data') if isfile(join('C://Users//facebook_data', f))]

#빈 공백 데이터 프레임을 만들어줌
final_facebook = pd.DataFrame()

#만들어진 페이스북 데이터 목록 리스트를 반복문에 적용
for i in facebook_list:
    file_name = i
    print(file_name)
    file = pd.read_csv(f'C://Users//facebook_data//{file_name}')
    #불러운 csv 파일을 concat함수를 이용해 비어있는 final_facebook에 밑에 행으로 이어붙여줌
    final_facebook = pd.concat([final_facebook,file],axis = 0,sort = False)
    
#구글 데이터 불러오기
#동일하게 반복
#이번 경우 file_dir 정의하여 계속 파일경로를 붙여넣을 필요 없이 진행
file_dir = 'C://Users//google_data'
google_list = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]

final_google = pd.DataFrame()

for i in google_list:
    file_name = i
    print(file_name)
    file = pd.read_csv(file_dir + f'//{file_name}')
    final_google = pd.concat([final_google,file],axis = 0,sort = False)
    
    
#GA 데이터 불러오기
#동일하게 반복
file_dir = 'C://Users//GA_data'
ga_list = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]

final_ga = pd.DataFrame()

for i in ga_list:
    file_name = i
    print(file_name)
    file = pd.read_csv(file_dir + f'//{file_name}')
    final_ga = pd.concat([final_ga,file],axis = 0,sort = False)



#%%페이스북, 구글 데이터 URL에서 GA 컬럼 정보 가져오기
#페이스북, 구글 데이터와 GA 데이터를 합치기 위해 페이스북,구글 데이터에서 GA데이터의 utm 정보를 추출
#GA데이터는 캠페인, 광고그룹, 소재명 정보를 가지고 있지 않고 오직 utm 정보만으로 식별 가능
#매체 데이터인 페이스북, 구글에는 세팅 url을 리포트로 추출하여 볼 수 있고 각 광고 그룹과 소재별로 세팅된 url 확인 가능
#해당 세팅 url에는 utm정보가 들어있음
#페이스북 데이터를 열어 url 하나를 복사해서 샘플 문자열 생성
sample_url = 'https://m.sample.com/goods/event_sale.php?sno=254&utm_source=facebook&utm_medium=sns&utm_campaign=camp_19&utm_content=creative_88'

#샘플 url을 보면 & 기준으로 utm 정보가 나뉘어져 있음을 확인
#& 기준으로 문자열 split을 진행함
sample_url_split = sample_url.split('&')
print(sample_url_split)
#출력 결과 2번째에 있는 utm_source=facebook에서 
sample_url_split[1]
sample_url_split[1].split('=')
sample_url_split[1].split('=')[-1]

#GA데이터에서 사용된 utm 정보를 확인하기 위해 columns 확인
final_ga.columns
#GA 데이터에서 소스, 미디엄, 캠페인, 콘텐츠 모두 확인해야함, 위 split을 활용하여 페이스북 데이터에 각 컬럼을 만들어줌

#페이스북에서 사용할 utm 콘텐츠 컬럼명은 GA 데이터의 컬럼명과 동일하게 사용
final_facebook['source(Media)'] = final_facebook['URL'].apply(lambda x: str(x).split('&')[1].split('=')[-1])
final_facebook['medium'] = final_facebook['URL'].apply(lambda x: str(x).split('&')[2].split('=')[-1])
final_facebook['campaign'] = final_facebook['URL'].apply(lambda x: str(x).split('&')[3].split('=')[-1])
final_facebook['content'] = final_facebook['URL'].apply(lambda x: str(x).split('&')[4].split('=')[-1])
#만들어진 결과 확인
final_facebook.columns
final_ga.columns

# 구글데이터에도 동일하게 진행
sample_url_2 = 'https://m.sample.com/goods/event_sale.php?sno=85&utm_source=google&utm_medium=sns&utm_campaign=camp_24&utm_content=creative_169'
sample_url_split_2 = sample_url_2.split('&')
print(sample_url_split_2)
sample_url_2.split('&')[1].split('=')[-1]
final_google['source(Media)'] = final_google['URL'].apply(lambda x: str(x).split('&')[1].split('=')[-1])
final_google['medium'] = final_google['URL'].apply(lambda x: str(x).split('&')[2].split('=')[-1])
final_google['campaign'] = final_google['URL'].apply(lambda x: str(x).split('&')[3].split('=')[-1])
final_google['content'] = final_google['URL'].apply(lambda x: str(x).split('&')[4].split('=')[-1])
final_facebook.columns
final_google.columns
final_ga.columns

#%%페이스북, 구글 데이터와 GA 데이터를 합쳐주기
#페이스북, 구글과 GA데이터는 모두 존재해야하기 때문에 merge 과정에서 합집합으로 진행

#머지에 사용할 컬럼 확인
final_facebook.columns
#먼저 페이스북과 구글 데이터를 합쳐줌
#둘의 column이 동일하기 때문에 concat으로 병합
fb_google_concat = pd.concat([final_facebook, final_google], axis = 0)
#추출한 utm 정보와 date를 함께 병합
final_total = pd.merge(left = fb_google_concat, right = final_ga, how = 'outer', on = ['Date','source(Media)', 'medium', 'campaign', 'content'])
#엑셀로 내보내기
final_total.to_excel('C://Users//merge_data//final_facebook_google_ga_merge.xlsx')
