#!/bin/python3
from time import sleep,time
import pandas as pd
import numpy as np
import api
import psycopg2 as pg
from random import random
from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://app:dev@localhost/app', echo = False)
####                                                              use echo = True for debugging

# try to empty the working table if it already exists
try:
    engine.execute('TRUNCATE TABLE dataframe')
except:
    pass

#metrics namespace
metric = 'app.load.data.'
#con = pg.connect("host=localhost dbname=app user=app password=dev")

while True:
    timer = api.start_timer()

    #retrieve a subset, no indexes
    try:
        with engine.begin() as con:
            df = pd.read_sql('SELECT * FROM dataframe WHERE a > 1.0 AND b < 2.0 AND c > 3.0', con)
            print(df.size)
        timer = api.submit_timer_metric(timer, f'{metric}retrieve' )

        # transform
        df = df ** 0.5 ** 2.8 * df
        timer = api.submit_timer_metric(timer, f'{metric}transform' )

    except Exception as e:
        # it will fail the first time if table not there yet
        print (e)
        df = pd.DataFrame()
        #restart timer
        timer = api.start_timer()

    # generate more  data
    df = pd.DataFrame(np.random.randint(0,100,size=(10**6, 4)), columns=list('abcd'))
    timer = api.submit_timer_metric(timer, f'{metric}generate')

    # store
    with engine.begin() as con:
        df.to_sql('dataframe', con=con, if_exists = 'append')
    timer = api.submit_timer_metric(timer, f'{metric}store' )

    sleep(random()*5.0)
