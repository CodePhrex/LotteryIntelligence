import streamlit as st
import pandas as pd
import csv, io
from lottery import DATA,GAMES,FIELDS,SOURCES,save,sync
st.set_page_config(page_title='Lottery Intelligence',layout='wide')
st.title('Lottery Intelligence | CodePhrex')
st.caption('Historical research — local archive')
game=st.selectbox('Game',GAMES)
if st.button('Sync national sources'):
    for g in SOURCES:
        try: st.success(f'{g}: {sync(g)} source records processed')
        except Exception as e: st.error(f'{g}: {e}')
upload=st.file_uploader('Import normalized historical CSV',type='csv')
if upload and st.button('Import'):
    try:
        reader=csv.DictReader(io.StringIO(upload.getvalue().decode('utf-8-sig')))
        save([tuple(row[k] for k in FIELDS) for row in reader])
        st.success('Imported')
    except Exception as e: st.error(str(e))
p=DATA/(game+'.csv')
if p.exists():
    df=pd.read_csv(p,dtype=str,keep_default_na=False)
    st.metric('Archived drawings',len(df))
    st.dataframe(df,use_container_width=True)
    st.download_button('Export game CSV',p.read_bytes(),p.name,'text/csv')
else: st.info('No local archive yet.')
if (DATA/'master.csv').exists(): st.download_button('Export master CSV',(DATA/'master.csv').read_bytes(),'master.csv','text/csv')
st.caption('Michigan automatic retrieval and full historical coverage are pending.')
