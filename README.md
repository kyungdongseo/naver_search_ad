naver_search_ad
---------------    
**naver_search_ad** 는 네이버 검색 광고 오픈 API의 파이썬 래퍼(Python wrapper)입니다.    
현재는 연관 검색어(키워드 도구)만 구현되어 있습니다.    
네이버 검색광고 OPEN API에 관한 자세한 내용은 아래 주소에서 확인하실 수 있습니다.    
[네이버 검색 광고 OPEN API 공식문서](http://naver.github.io/searchad-apidoc/#/tags/RelKwdStat)    

설치
----
**pip install naver_search_ad**   

사용법
------
1. 위의 명령어를 이용하여 naver_search_ad 패키지 설치
2. OPEN API Key 발급받기
    - 네이버의 [How to issue the API License and the secret key](http://naver.github.io/searchad-apidoc/#/guides)를 참조하여 CustomerID, ApiLicense, SecretKey 를 준비합니다.
3. **naver.ini** 파일을 만들고 아래의 정보를 작성하십시오.
```python
[DEFAULT]
CUSTOMER_ID = '발급받은 customer id'
API_KEY = '발급받은 API License'
SECRET_KEY = '발급받은 secret key'
```
4. 파이썬 쉘에서 테스트 해보기
```python
MacBook-Pro:~/kyungdongseo$ pip install naver_search_ad

MacBook-Pro:~/kyungdongseo$ cat >> naver.ini << EOF
> [DEFAULT]
> CUSTOMER_ID = '발급받은 customerid'
> API_KEY = '발급받은 API License'
> SECRET_KEY = '발급받은 secret key'
> EOF

MacBook-Pro:~/kyungdongseo$ ls
naver.ini    

MacBook-Pro:~/kyungdongseo$ python
>>> from naver_search_ad.keywords import related_keyword
>>> r = related_keyword('POP꽂이')
>>> import pprint
>>> pprint.pprint(r)
{'keywordList': [{'compIdx': '높음',
                  'monthlyAveMobileClkCnt': 28.7,
                  'monthlyAveMobileCtr': 4.62,
                  'monthlyAvePcClkCnt': 10.1,
                  'monthlyAvePcCtr': 1.6,
                  'monthlyMobileQcCnt': 660,
                  'monthlyPcQcCnt': 710,
                  'plAvgDepth': 15,
                  'relKeyword': 'POP꽂이',
                  'related_point': 1200},
                 {'compIdx': '높음',
                  'monthlyAveMobileClkCnt': 101.7,
                  'monthlyAveMobileCtr': 2.32,
                  'monthlyAvePcClkCnt': 7.9,
                  'monthlyAvePcCtr': 0.8,
                  'monthlyMobileQcCnt': 4810,
                  'monthlyPcQcCnt': 1100,
                  'plAvgDepth': 15,
                  'relKeyword': '집게스탠드',
                  'related_point': 1199},
                  # 나머지는 생략...]}

>>> from naver_search_ad.keywords import related_keyword_to_xls
>>> related_keyword_to_xls('POP꽂이', './related_keyword.xls')
>>> exit()

MacBook-Pro:~/kyungdongseo$ ls
naver.ini  related_keyword.xls
```
