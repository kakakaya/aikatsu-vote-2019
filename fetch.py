#!/usr/bin/python3

import json

from bs4 import BeautifulSoup
import requests
from models import init_db, save_ranking, recent_rankings


def get_ranking():
    cookies = {
        '_bpnavi_session': 'd5b93e9d224ecb6c2fcca0b74c7dfbd3',
    }

    headers = {
        'Origin': 'https://bpnavi.jp',
        'X-CSRF-Token': 'L08DDxWshjC3nOcupgNfMkwYSvOtV8NiI/DXKkeJ2is=',
        'User-Agent': 'iPhone',
        'Referer': 'https://bpnavi.jp/s/elec/aikatsu_p5/item_rankings',
    }

    ranking = []
    for i in range(1, 5):
        response = requests.post(
            'https://bpnavi.jp/s/elec/aikatsu_p5/item_rankings/more',
            headers=headers,
            cookies=cookies,
            data={'page': str(i)}
        )
        if not response.ok:
            return
        soup = BeautifulSoup(json.loads(response.text)['attachmentPartial'], 'lxml')
        ranking += [e.text.strip() for e in soup.select('p.name_vote > a')]
    return tuple(ranking)


def fetch():
    ranking = get_ranking()
    save_ranking(ranking)


def main():
    init_db()

    for ranking in recent_rankings(hour_range=2):
        print(ranking.__dict__)
        # print(ranking.created.strftime("%Y/%m/%d %H:%M:%S"))
        print(ranking.created.isoformat(timespec='seconds'), ranking.entryrankinglog.rank, ranking.name)


if __name__ == '__main__':
    main()
