import pandas as pd

#Clean .csv file
df=pd.read_csv('data.csv', sep=';')
df=df[['Descripción Alarma', 'IdEquipo', 'Fecha de inicio', 'Fecha de fin', 'Texto']]
df.rename(columns={'Descripción Alarma':'Alarm Description', 'IdEquipo':'Equipment', 'Fecha de inicio':'Start Date', 'Fecha de fin':'End Date', 'Texto':'Text'}, inplace=True)
df['Alarm Description']=df['Alarm Description'].str.replace('\t', '')

#Clean .ini file | 0:EXT - 1:INT
dx=pd.read_csv('alarm.ini', sep='|')
dx=dx[['[ALARM ', ' INTERNAL ']]
dx.rename(columns={'[ALARM ': 'ALARM', ' INTERNAL ':'TYPE'}, inplace=True)
dx['ALARM']=dx['ALARM'].str.replace('\t', '')
dx['ALARM']=dx['ALARM'].str.split('=').str[1]
dx['TYPE']=dx['TYPE'].replace(0, 'EXT')
dx['TYPE']=dx['TYPE'].replace(1, 'INT')
dx[dx['TYPE']=='INT']

#Joining .ini with .csv
df=df.join(dx.set_index('ALARM'), on='Alarm Description')

#Complete fields
df['EquipmentType']='CB30'
df['Duration']=''
df['Ack.']=''
df['Operator intervention time']=''
df['Cause declared by operator']=''
df['ID']=''
df.rename(columns={'TYPE':'Category'}, inplace=True)
df=df[['Alarm Description', 'Equipment', 'EquipmentType', 'Start Date', 'End Date', 'Duration', 'Category', 'Ack.', 'Operator intervention time', 'Cause declared by operator', 'ID', 'Text']]

#Export file cleaned
df.to_excel('Root_cleaned.xlsx', index=False)
