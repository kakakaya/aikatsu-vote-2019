#!/usr/bin/fish

for i in (seq 1 4)
    curl -s 'https://bpnavi.jp/s/elec/aikatsu_p5/item_rankings/more' \
    -H 'Cookie: _bpnavi_session=d5b93e9d224ecb6c2fcca0b74c7dfbd3' \
    -H 'Origin: https://bpnavi.jp' \
    -H 'X-CSRF-Token: L08DDxWshjC3nOcupgNfMkwYSvOtV8NiI/DXKkeJ2is=' \
    -H 'User-Agent: iPhone' \
    -H 'Referer: https://bpnavi.jp/s/elec/aikatsu_p5/item_rankings' \
    --data "page=$i" --compressed | jq '.attachmentPartial' | pup 'p.name_vote > a text{}'
end > /tmp/aikatsu-ranking-(strdatetime).txt
