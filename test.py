from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pandas.io.sql as psql
engine = create_engine('postgresql+psycopg2://app:dev@localhost/app', echo = True)

#df = pd.read_sql('select * from Stat_Table', con=engine)
df = pd.DataFrame(np.random.randint(0,100,size=(10, 4)), columns=list('abcd'))
df = df ** 0.5
df = df.append(pd.DataFrame(np.random.randint(0,100,size=(10, 4)), columns = list('abcd')),  sort = False, ignore_index = True)
print(df)
engine = create_engine('postgresql+psycopg2://app:dev@localhost/app', echo = True)
#with engine.begin() as con:
#    df.to_sql('dataframe', con, if_exists='append') 

print('ok')
