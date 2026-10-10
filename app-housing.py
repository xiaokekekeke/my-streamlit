"""
BANA409 Data App Lab —— California Housing (1990)
参考实现（不是标准答案，只是把 7 条要求逐条落到代码上）

放到 my-streamlit/ 文件夹里，和 housing.csv 同级，然后：
    uv run streamlit run app-housing.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 可选：tutorial 里用了这个风格（浅灰底 + 网格）。讲义 lab 的截图看起来是默认白底，
# 所以这行留着注释，你想要 tutorial 那个样子再打开。
# plt.style.use('seaborn-v0_8')

# ---------------------------------------------------------------- 要求 1：标题
st.title('California Housing Data (1990) by Qirun Wang')

# 每次任何控件被拖动，下面整段都会从头再跑一遍 —— 所以数据要在这里重新读
df = pd.read_csv('housing.csv')

# ------------------------------------------------- 要求 2：主区滑块（房价下限）
# 上限写 500001：这是数据里 median_house_value 的真实最大值
value_filter = st.slider('Minimal Median House Value', 0, 500001, 200000)

# ------------------------------------------------------ 要求 3：侧栏提示小标题
st.subheader('See more filters in the sidebar:')

# ------------------------------------------- 要求 4：侧栏多选（海距类型，默认全选）
ocean_filter = st.sidebar.multiselect(
    'Choose the location type',
    df.ocean_proximity.unique(),   # 选项：5 个类型
    df.ocean_proximity.unique())   # 默认：5 个全选

# ------------------------------------------------ 要求 5：侧栏单选（收入档位）
# 不传 index，默认落在第一个选项 Low —— 与讲义截图的默认状态一致
income_filter = st.sidebar.radio('Choose income level', ['Low', 'Medium', 'High'])

# ------------------------------------------------------------------- 三道过滤
# 顺序无所谓（都是行筛选），但写法必须是链式覆盖 df
df = df[df.median_house_value >= value_filter]
df = df[df.ocean_proximity.isin(ocean_filter)]

if income_filter == 'Low':
    # 题面：median_income <= 2.5。数据里有 28 行恰好 == 2.5，别写成 <
    df = df[df.median_income <= 2.5]
elif income_filter == 'Medium':
    # 题面：2.5 < median_income < 4.5（两端都不含）
    df = df[(df.median_income > 2.5) & (df.median_income < 4.5)]
else:
    # 题面：median_income >= 4.5。数据里有 24 行恰好 == 4.5，别写成 >
    df = df[df.median_income >= 4.5]

# --------------------------------------------------- 要求 6：地图（列名刚好合规）
st.map(df)

# ------------------------------------------------ 要求 7：地图下方 30 桶直方图
fig, ax = plt.subplots()
ax.hist(df.median_house_value, bins=30)
ax.set_xlabel('Median House Value (USD)')
ax.set_ylabel('Number of Districts')
st.pyplot(fig)
