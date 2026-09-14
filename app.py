from pathlib import Path
import datetime as dt
import html
import math
import sys
import uuid
from runtime import atomic_json,entry,parser,read_json

LABELS={'numer_zlecenia':'Numer zlecenia','klient':'Klient','urzadzenie':'Urządzenie','producent':'Producent','model':'Model','serial':'Numer seryjny (opcjonalny)',
 'data':'Data','zgloszony_problem':'Zgłoszony problem','diagnoza':'Diagnoza','wykonane_czynnosci':'Wykonane czynności','czesci':'Części','test_koncowy':'Test końcowy',
 'zalecenia':'Zalecenia','czas_pracy_min':'Czas pracy (minuty)','technik':'Technik'}

def template():
    return {**{name:'' for name in LABELS},'data':dt.date.today().isoformat(),'technik':'Dominik Wasilak — Prestige Tech','czesci':[],'czas_pracy_min':0}

def validate(data):
    if not isinstance(data,dict) or set(data)-set(LABELS):raise ValueError('Nieznane pola raportu.')
    result={**template(),**data}
    for name in ('numer_zlecenia','klient','urzadzenie','zgloszony_problem','diagnoza','wykonane_czynnosci','test_koncowy'):
        if not isinstance(result[name],str) or not result[name].strip():raise ValueError('Brakuje wymaganego pola.')
    for name in LABELS:
        if name not in ('czesci','czas_pracy_min') and (not isinstance(result[name],str) or len(result[name])>50000):raise ValueError('Nieprawidłowy tekst.')
    dt.date.fromisoformat(result['data'])
    if not isinstance(result['czesci'],list) or any(not isinstance(x,str) for x in result['czesci']):raise ValueError('Części jako lista tekstów.')
    duration=result['czas_pracy_min']
    if isinstance(duration,bool) or not isinstance(duration,(int,float)) or not math.isfinite(duration) or duration<0:raise ValueError('Nieprawidłowy czas pracy.')
    return result

def render(data,directory):
    data=validate(data);directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);base=directory/('serwis-'+uuid.uuid4().hex)
    rows=[];text=['PRESTIGE TECH','by Dominik Wasilak','Raport serwisowy','']
    for key,label in LABELS.items():
        value='\n'.join(data[key]) if isinstance(data[key],list) else str(data[key])
        rows.append(f'<tr><th>{html.escape(label)}</th><td>{html.escape(value)}</td></tr>');text.extend([label+':',value,''])
    document='<!doctype html><html lang="pl"><meta charset="utf-8"><title>Raport serwisowy Prestige Tech</title><style>body{font:16px system-ui;max-width:1000px;margin:40px auto;padding:20px}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #ddd;padding:12px;white-space:pre-wrap;overflow-wrap:anywhere}th{width:28%}@media print{body{margin:0}tr{break-inside:avoid}}</style><h1>PRESTIGE TECH</h1><p>by Dominik Wasilak</p><h2>Raport serwisowy</h2><table>'+''.join(rows)+'</table></html>'
    atomic_json(base.with_suffix('.json'),data);base.with_suffix('.txt').write_text('\n'.join(text),encoding='utf-8');base.with_suffix('.html').write_text(document,encoding='utf-8')
    return {'files':[str(base.with_suffix('.'+extension)) for extension in ('html','json','txt')]}

def build():
    p=parser('Raport serwisowy Prestige Tech. Dane klienta pozostają lokalne.')
    p.add_argument('command',nargs='?',choices=['template','generate']);p.add_argument('--input');p.add_argument('--template-file',default='zlecenie.json');p.add_argument('--directory',default='reports')
    return p

def handle(a):
    if a.command=='template':
        if Path(a.template_file).exists():raise FileExistsError(a.template_file)
        atomic_json(a.template_file,template());return {'template':a.template_file}
    if a.command=='generate' and a.input:return render(read_json(a.input),a.directory)
    raise ValueError('Wybierz polecenie i wejście.')

if __name__=='__main__':sys.exit(entry(build,handle))
