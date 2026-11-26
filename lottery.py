import csv, io, sqlite3, datetime, pathlib, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
DATA=ROOT/'data'
GAMES=('powerball','mega_millions','michigan_daily_3','michigan_daily_4')
FIELDS=('game','draw_date','session','numbers','bonus','multiplier','source')
SOURCES={'powerball':'https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Winning_Numbers/powerball.csv','mega_millions':'https://www.texaslottery.com/export/sites/lottery/Games/Mega_Millions/Winning_Numbers/megamillions.csv'}
def parse(game, raw, source):
    for row in csv.reader(io.StringIO(raw)):
        if not row: continue
        if len(row) not in (10,11): raise ValueError('Unexpected source format')
        date=datetime.date(int(row[3]),int(row[1]),int(row[2])).isoformat()
        yield (game,date,'evening',' '.join(str(n) for n in sorted(map(int,row[4:9]))),str(int(row[9])),row[10].strip() if len(row)==11 else '',source)
def save(rows):
    DATA.mkdir(exist_ok=True)
    with sqlite3.connect(DATA/'draws.sqlite',timeout=30) as db:
        db.execute('CREATE TABLE IF NOT EXISTS draws(game TEXT,draw_date TEXT,session TEXT,numbers TEXT,bonus TEXT,multiplier TEXT,source TEXT,PRIMARY KEY(game,draw_date,session))')
        for r in rows:
            if r[0] not in GAMES or r[2] not in ('midday','evening'): raise ValueError('Invalid game/session')
            datetime.date.fromisoformat(r[1])
            if r[0].startswith('michigan'):
                if len(r[3]) != int(r[0][-1]) or not r[3].isascii() or not r[3].isdigit(): raise ValueError('Invalid digits')
            else:
                nums=list(map(int,r[3].split()))
                if len(nums)!=5 or len(set(nums))!=5 or min(nums)<1 or max(nums)>75 or not 1<=int(r[4])<=60: raise ValueError('Invalid balls')
            old=db.execute('SELECT numbers,bonus,multiplier FROM draws WHERE game=? AND draw_date=? AND session=?',r[:3]).fetchone()
            if old and old!=r[3:6]: raise ValueError('Conflicting draw: '+str(r[:3]))
            db.execute('INSERT OR IGNORE INTO draws VALUES(?,?,?,?,?,?,?)',r)
        db.commit()
        db.execute('BEGIN IMMEDIATE')
        for name in ('master',*GAMES):
            rows=db.execute('SELECT * FROM draws'+(' WHERE game=?' if name!='master' else '')+' ORDER BY draw_date,game,session', (name,) if name!='master' else ()).fetchall()
            tmp=DATA/(name+'.tmp')
            with tmp.open('w',newline='',encoding='utf-8') as f:
                w=csv.writer(f);w.writerow(FIELDS);w.writerows(rows)
            tmp.replace(DATA/(name+'.csv'))
def sync(game):
    url=SOURCES[game]
    with urllib.request.urlopen(url,timeout=60) as response:
        raw=response.read().decode('utf-8-sig')
    rows=list(parse(game,raw,url))
    if not rows: raise ValueError('Empty archive')
    save(rows)
    return len(rows)
if __name__=='__main__':
    failed=False
    for game in SOURCES:
        try: print(game,sync(game))
        except Exception as e: print(game,e);failed=True
    raise SystemExit(int(failed))
