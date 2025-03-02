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
st.write('資料來源: 臺鐵每日各站點進出站人數, from https://data.gov.tw/dataset/8792')

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

        ax.plot(df_sta['日期'], df_sta['入站人數'], label='Number of people entring', marker='o')
        ax.plot(df_sta['日期'], df_sta['出站人數'], label='Number of people leaving', marker='*')
        n = df_sta.shape[0]
        x = np.linspace(0, n-1, 5).astype(int)
        x_tick = [df_sta.loc[i, '日期'] for i in x]
        ax.set_xticks(x_tick)

        ax.grid(True)
        ax.legend()
        ax.set_title(staCode + ' ' +'People Counting')
        ax.set_xlabel('Date')
        ax.set_ylabel('Person Counts')

        max_entry_index = df_sta['入站人數'].idxmax()
        max_exit_index = df_sta['出站人數'].idxmax()

        st.write(staCode + " 入站人數最多的日期: " + str(df_sta.loc[max_entry_index, "日期"]) + ", 共" + str(df_sta.loc[max_entry_index, "入站人數"]) + '人')

        st.write(staCode + " 出站人數最多的日期: " + str(df_sta.loc[max_entry_index, "日期"]) + ", 共" + str(df_sta.loc[max_entry_index, "出站人數"]) + '人')

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
        dfg_tail10 = dfg.sort_values(by='出站人數', ascending=True).tail(10).copy()
        dfg_tail10.reset_index(inplace=True, drop=True)

        max_entry_index = dfg_top10['入站人數'].idxmax()
        max_exit_index = dfg_tail10['出站人數'].idxmax()
        st.write('入站人數Top1為' + dfg_top10.loc[max_entry_index, '站別碼'] + ', 共' + str(dfg_top10.loc[max_entry_index, '入站人數']) + ' 人')
        st.write('出站人數Top1為' + dfg_top10.loc[max_entry_index, '站別碼'] + ', 共' + str(dfg_top10.loc[max_entry_index, '出站人數']) + ' 人')


        # 入站人數畫圖
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        bars = ax.bar(dfg_top10['站別碼'], dfg_top10['入站人數'], label='Number of people entering')
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom') 
        

        ax.grid(True)
        ax.set_xlabel('Station Code')
        ax.set_ylabel('Person Counts')
        ax.set_title('Top 10 stations with the most visitors' + ' ' + '(' + str(sd[0]) + ' ~ ' + str(sd[1]) + ')')
        ax.legend()
        st.pyplot(fig)


        # 出站人數畫圖
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        bars = ax.bar(dfg_tail10['站別碼'], dfg_tail10['出站人數'], label='Number of people leaving')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom') 
        
        ax.grid(True)
        ax.set_xlabel('Station Code')
        ax.set_ylabel('Person Counts')
        ax.set_title('Top 10 stations with the most departures' + ' ' + '(' + str(sd[0]) + ' ~ ' + str(sd[1]) + ')')
        ax.legend()         
        st.pyplot(fig)



if __name__ == '__main__':
    # print('this streamlit app is running~')
    pass
        