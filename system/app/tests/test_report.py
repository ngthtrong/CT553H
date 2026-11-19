"""HTML report of a saved analysis (plan-system 3.5): RPT-01…03."""
from __future__ import annotations

import re
from html.parser import HTMLParser

from api.report import REPORT_CSP, REPORT_CSP_META, build_report, footprint_rows, prob_color
from tests.conftest import mk_client

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags: list[tuple[str, dict]] = []
        self.sections: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if 'data-section' in a:
            self.sections.append(a['data-section'])


def _saved(c, body):
    pid = c.post('/v1/projects', json={'name': 'report'}).json()['project_id']
    r = c.post(f'/v1/projects/{pid}/analyses', json={'request': body})
    assert r.status_code == 201, r.text
    return r.json()


def test_rpt01_numbers_equal_the_api_and_rpt02_warnings_and_attribution_come_first(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    a = _saved(c, {'uniprot_id': 'P12345', 'tile_index': 1})
    r = c.get(f"/v1/analyses/{a['analysis_id']}/report?format=html")
    assert r.status_code == 200 and r.headers['content-type'].startswith('text/html')
    assert r.headers['content-security-policy'] == REPORT_CSP                # the route's own policy, not replaced
    assert r.headers['cache-control'] == 'no-store' and r.headers['content-disposition'].startswith('inline')
    html = r.text
    res = a['result']
    # RPT-01: every top-10 % row and every footprint mean is printed from the same cells
    for cell in sorted(res['cells'], key=lambda x: x['rank_in_tile'])[:54]:
        row = (f'<td class="num">{cell["rank_in_tile"]}</td><td class="mono">{cell["wt_aa"]}{cell["position"]}'
               f'{cell["mut_aa"]}</td><td class="num">{cell["score_dpsi_raw"]:.4f}</td>'
               f'<td class="num">{cell["p_dpsi_ge_1_calibrated"]:.4f}</td>')
        assert row in html
    for fp in footprint_rows(res['cells'], res['tile']['sequence']):
        assert f'<td class="num">{fp["position"]}</td><td>{fp["wt"]}</td><td class="num">{fp["mean_prob"]:.4f}' in html
    assert html.count('<rect x=') >= 560                                       # 28 × 20 matrix cells
    # RPT-02: the same warnings and evidence as the screen, before any number; model hash and source attribution
    p = Collector()
    p.feed(html)
    assert p.sections.index('evidence') < p.sections.index('topk')
    assert p.sections.index('domain') < p.sections.index('topk')
    assert 'warning' in p.sections and p.sections.index('warning') < p.sections.index('topk')
    for w in res['warnings']:
        assert w['code'] in html
    assert html.index('Read this first') < html.index('<svg class="matrix"')
    assert res['provenance']['weights_sha256'] in html and res['provenance']['evidence_label'] in html
    for src in res['provenance']['data_sources']:
        assert src['attribution_text'].replace('&', '&amp;') in html or src['attribution_text'] in html
    assert 'Not a probability of disease; not for diagnostic use.' in html
    # attachment on request
    d = c.get(f"/v1/analyses/{a['analysis_id']}/report?format=html&download=true")
    assert d.headers['content-disposition'].startswith('attachment;') and 'report.html' in d.headers['content-disposition']


def test_rpt03_no_script_and_no_external_resource(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    a = _saved(c, {'sequence': SEQ})
    html = c.get(f"/v1/analyses/{a['analysis_id']}/report?format=html").text
    p = Collector()
    p.feed(html)
    assert not [t for t, _ in p.tags if t in ('script', 'link', 'iframe', 'img', 'object', 'embed', 'base', 'form')]
    for _, attrs in p.tags:
        for k in ('src', 'href', 'action', 'xlink:href'):
            assert not attrs.get(k), (k, attrs)
    assert not re.search(r'url\(\s*["\']?(https?:|//)', html)
    assert not re.search(r'@import', html)
    assert f'content="{REPORT_CSP_META}"' in html                             # also as a meta, for a saved file
    assert 'frame-ancestors' not in REPORT_CSP_META                           # ignored (and warned) in a meta


def test_report_escapes_text_and_validates_the_request(mini, dbcopy):
    c, _ = mk_client(mini, dbcopy)
    a = _saved(c, {'sequence': SEQ})
    assert c.get(f"/v1/analyses/{a['analysis_id']}/report").status_code == 422
    assert c.get(f"/v1/analyses/{a['analysis_id']}/report?format=pdf").status_code == 400
    assert c.get('/v1/analyses/00000000-0000-4000-8000-000000000000/report?format=html').status_code == 404
    data = c.get(f"/v1/analyses/{a['analysis_id']}").json()
    data['result']['provenance']['data_sources'] = [{'source_id': 'x', 'name': '<script>alert(1)</script>',
                                                     'version': '"><b>', 'license_name': 'CC0',
                                                     'attribution_text': '<img src=x onerror=alert(1)>'}]
    html = build_report(data)
    assert '<script>alert(1)</script>' not in html and '<img src=x' not in html
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in html


def test_probability_colours_follow_reversed_viridis():
    assert prob_color(0.0) == '#fde725' and prob_color(1.0) == '#440154' and prob_color(0.5) == '#21918c'
