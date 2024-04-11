import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl


df1 = pd.read_excel('./RF_salaries.xlsx', skiprows=range(4))
df1 = df1.rename({'Unnamed: 0': 'Вид деятельности'}, axis=1)
df1.dropna(inplace=True)
df2 = pd.read_excel('RF_salaries.xlsx', sheet_name=1, skiprows=range(2))
df2.rename({'Unnamed: 0': 'Вид деятельности'}, axis=1, inplace=True)
df2.dropna(inplace=True)
df = pd.merge(left=df2, right=df1, on='Вид деятельности')

areas = ['Образование', 'Здравоохранение и предоставление социальных услуг', 'Добыча полезных ископаемых']
my_df = df.loc[(df['Вид деятельности'] == areas[0]) | (df['Вид деятельности'] == areas[1]) |
               (df['Вид деятельности'] == areas[2])]
my_df = my_df.reset_index(drop=True).rename({'Вид деятельности': 'Год'}, axis=1)
my_df = my_df.set_index('Год').transpose()

my_df['Годовой уровень инфляции'] = [0, 18.58, 15.06, 11.99, 11.74, 10.91, 9.00, 11.87, 
                                    13.28, 8.80, 8.78, 6.10, 6.58, 6.45, 11.36, 12.91, 
                                    5.38, 2.52, 4.27, 3.05, 4.91, 8.39, 11.92, 7.42 ]

my_df['Coef'] = 1 - my_df['Годовой уровень инфляции']/100

for area in areas:
    my_df[f'{area} (с учетом инфляции)'] = my_df[f'{area}'] * my_df['Coef'].cumprod()
    my_df[f'{area} (с учетом инфляции)'] = my_df[f'{area} (с учетом инфляции)'].round(2)

# графики динамики номинальных зарплат
fig1 = px.line(my_df, x=my_df.index, y=my_df.columns[:3], labels={
            'index':'Год', 'value': 'Средняя зарплата', 'variable': 'Вид деятельности'},
              markers=True, height=570, width=900) 
fig1.update_layout(title='Динамика номинальной среднемесячной ЗП работников в РФ за 2000-2023 гг',
title_font_size=20, legend=dict(
    orientation="v",
    yanchor="top",
    y=0.95,
    xanchor="left",
    x=0.05,
    title_text=''
))        

# графики динамики зарплат с учетом инфляции
fig2 = px.line(my_df, x=my_df.index, y=my_df.columns[5:], labels={
            'index':'Год', 'value': 'Средняя зарплата', 'variable': 'Вид деятельности'}, 
            markers=True, height=585, width=900)  
fig2.update_layout(title='Динамика реальной среднемесячной ЗП работников в РФ за 2000-2023 гг',
title_font_size=20, legend=dict(
    orientation="v",
    yanchor="top",
    y=0.98,
    xanchor="left",
    x=0.01,
    title_text=''
))         

# образование
fig3 = px.line(my_df, x=my_df.index, y=my_df.columns[[1, 5]], labels={
            'index':'Год', 'value': 'Средняя зарплата', 'variable': 'Вид деятельности'}, 
            markers=True, height=450, width=750)         
fig3.update_layout(title='Динамика среднемесячной ЗП работников в сфере образования в РФ за 2000-2023 гг',
title_font_size=14, legend=dict(
    orientation="v",
    yanchor="top",
    y=0.95,
    xanchor="left",
    x=0.05,
    title_text=''
))

newnames = {'Образование':'Номинальная ЗП', 'Образование (с учетом инфляции)': 'Реальная ЗП (с учетом инфляции)'}
fig3.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )

# добыча полезных ископаемых
fig4 = px.line(my_df, x=my_df.index, y=my_df.columns[[0, 7]], labels={
            'index':'Год', 'value': 'Средняя зарплата', 'variable': 'Вид деятельности'},
            markers=True, height=450, width=750)         
fig4.update_layout(title='Динамика среднемесячной ЗП работников в сфере добычи полезных ископаемых в РФ за 2000-2023 гг',
title_font_size=14, legend=dict(
    orientation="v",
    yanchor="top",
    y=0.95,
    xanchor="left",
    x=0.05,
    title_text=''
))

newnames = {'Добыча полезных ископаемых':'Номинальная ЗП',
        'Добыча полезных ископаемых (с учетом инфляции)': 'Реальная ЗП (с учетом инфляции)'}
fig4.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
# здравоохранение и социальные услуги
fig5 = px.line(my_df, x=my_df.index, y=my_df.columns[[2, 6]], labels={
            'index':'Год', 'value': 'Средняя зарплата', 'variable': 'Вид деятельности'},
            markers=True, height=450, width=750)        
fig5.update_layout(
title='Динамика среднемесячной ЗП работников в сфере здравоохранения и социальных услуг в РФ за 2000-2023 гг',
title_font_size=14, legend=dict(
    orientation="v",
    yanchor="top",
    y=0.95,
    xanchor="left",
    x=0.05,
    title_text=''
)) 

newnames = {'Здравоохранение и предоставление социальных услуг':'Номинальная ЗП', 
'Здравоохранение и предоставление социальных услуг (с учетом инфляции)': 'Реальная ЗП (с учетом инфляции)'}
fig5.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )


# Streamlit
tab1, tab2 = st.tabs(["Общие графики", "Сравнение динамики номинальной и реальной ЗП"])

with tab1:
    st.subheader('''Динамика среднемесячной  заработной платы \
    работников организаций по видам экономической деятельности в Российской Федерации за 2000-2023 гг''')
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
with tab2:
    st.subheader('Динамика номинальной ЗП Vs \
             динамика реальной ЗП')
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
    st.plotly_chart(fig5)
