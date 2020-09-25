import urllib.parse
import itertools
from openpyxl import Workbook
from naver_search_ad.common import naver


@naver
def _related_keyword(query):
    '''네이버 검색광고의 키워드

    hintKeywords 는
    단어에 공백이 없고,
    각 단어는 콤마(,)로 최대 5개까지 연결한 문자열
    '''

    return {
            'method': "GET",
            'path': "/keywordstool",
            'query': urllib.parse.urlencode(query)
    }


def _related_point(response):
    ''' 연관성 점수'''

    for i, keyword in zip(
            range(len(response.get('keywordList')), 0, -1),
            response.get('keywordList')):
        keyword['related_point'] = i

    return response


def related_keyword(keywords):
    if type(keywords) is str:
        keywords = keywords.upper()
    elif type(keywords) is list:
        keywords = ','.join(keywords).upper()

    query = {
            'hintKeywords': keywords,
            'showDetail': 1
    }
    response = _related_keyword(query)
    response = _related_point(response)
    return response


def _write_xls(data_list, filename):
    '''엑셀로 저장(xls)'''

    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    headers = list(set(itertools.chain.from_iterable(data_list)))
    ws.append(headers)

    for elements in data_list:
        ws.append([elements.get(h) for h in headers])

    wb.save(filename)


def related_keyword_to_xls(keywords, filename):
    r = related_keyword(keywords)
    keyword_list = r.get('keywordList')
    if keyword_list:
        _write_xls(keyword_list, filename)

