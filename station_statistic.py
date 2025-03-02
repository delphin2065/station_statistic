import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
from station_statistic_dataDownload import data

# matplotlib 中文字顯示
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

# 匯入資料
df = data()
st.header('台鐵車站人數統計')
# 日期/ 站別碼/ 進站人數/ 出站人數

station = st.radio('查詢條件', ['依照日期', '依照站別'])
if station == '依照日期':
    staCode = np.unique(df['站別碼'])
    staCode = st.selectbox('選擇站別碼', staCode)

    btn = st.button('查詢')
    if btn:
        df_sta = df[df['站別碼'] == staCode].copy()
        df_sta.reset_index(drop=True, inplace=True)
        
        
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)  

        ax.plot(df_sta['日期'], df_sta['入站人數'], label='入站人數', marker='o')
        ax.plot(df_sta['日期'], df_sta['出站人數'], label='出站人數', marker='*')
        n = df_sta.shape[0]
        x = np.linspace(0, n-1, 5).astype(int)
        x_tick = [df_sta.loc[i, '日期'] for i in x]
        ax.set_xticks(x_tick)

        ax.grid(True)
        ax.legend()
        ax.set_title(staCode + ' ' +'人數統計')
        ax.set_xlabel('日期')
        ax.set_ylabel('人數')
        st.pyplot(fig)            

if station == '依照站別':
    
    sd = st.slider(min_value = df['日期'].min(), max_value = df['日期'].max(), label='選擇日期區間', value = (df['日期'].min(), df['日期'].max()))
    btn = st.button('查詢')

    if btn:
        dff = df[(df['日期']>=sd[0]) & (df['日期']<=sd[1])].copy()
        dffs = dff[['站別碼', '入站人數', '出站人數']]
        dfg = dffs.groupby(['站別碼']).sum()  
        dfg.reset_index(inplace=True, drop=False)
        dfg.insert(0, '起始日期', str(sd[0]))
        dfg.insert(1, '結束日期', str(sd[1]))
        dfg_top10 = dfg.sort_values(by='入站人數', ascending=True).tail(10).copy()
        dfg_top10.reset_index(inplace=True, drop=True)
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        bars = ax.bar(dfg_top10['站別碼'], dfg_top10['入站人數'], label='入站人數')
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom') 
        

        ax.grid(True)
        ax.set_xlabel('站別碼')
        ax.set_ylabel('人數')
        ax.set_title('入站人數前10名' + ' ' + '(' + str(sd[0]) + ' ~ ' + str(sd[1]) + ')')
        ax.legend()
        st.pyplot(fig)


        dfg_tail10 = dfg.sort_values(by='出站人數', ascending=True).tail(10).copy()
        dfg_tail10.reset_index(inplace=True, drop=True)
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        bars = ax.bar(dfg_tail10['站別碼'], dfg_tail10['出站人數'], label='出站人數')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom') 
        
        ax.grid(True)
        ax.set_xlabel('站別碼')
        ax.set_ylabel('人數')
        ax.set_title('出站人數前10名' + ' ' + '(' + str(sd[0]) + ' ~ ' + str(sd[1]) + ')')
        ax.legend()
        st.pyplot(fig)



if __name__ == '__main__':
    # print('this streamlit app is running~')
    pass
        