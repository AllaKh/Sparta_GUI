#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      aceslab
#
# Created:     09/11/2017
# Copyright:   (c) aceslab 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import os
import pandas as pd
import numpy as np
import sqlite3
from os.path import join
from collections import OrderedDict
import time as time

class Dal(object):

    def __init__(self,database_name,general_lab_path=r'Z:\Projects\pfe_shuttle'):
        """
            Create a SQL connection to our test database,
            if not exist create a new one with the name of the test.
        """
        self.general_lab_path = general_lab_path

        if os.path.exists(database_name):

            database_path=database_name
        else:
            database_path=join(general_lab_path,database_name)

        try:
            with sqlite3.connect(database_path) as self.conn:
                self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:

            print(e)
            raise

    def __del__(self):
        """
        destructor
        """
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print('del have been done!')

    def ReadSqlQuery(self,Query):

        df=pd.read_sql(Query,self.conn)

        return df

    def getRawDataByTime(self,Time):
        """
            this fuction return the raw data of test by Time
            args:
                Time - Test time
            return:

        """
        query="SELECT * From rawData WHERE Time = '%s' "%Time
        df=self.ReadSqlQuery(query)
        return df


    def getPivotDataFromDF(self,df,index='Time',columns='Key',values='Value'):
        """
                        dataframe obj contain column of raw data,
                for example:
                    Time    ADC     DNL     ......
                    -----   -----   -----
                    hh:mm   Series  Series  ......
                            of np   of np
                            values  values

        :param df:
        :param index:
        :param columns:
        :param values:
        :return:
        """
        if not df.empty:
            pivotData = pd.pivot_table(df, index = index, columns = columns, values = values,aggfunc =lambda x: ' '.join(x))
            func = lambda x: pd.Series([i for i in reversed(x.split(','))],index=None,dtype=np.float, )
            pivotData = pivotData.applymap(func)
            return pivotData
        else:
            print "No results found"


    def getAllTestData(self,TestName):

        query = "SELECT * From  %s "% TestName

        return self.ReadSqlQuery(query)

    def getAllTablesList(self):

        try:
            testsList = []
            res = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            for name in res:
                testsList.append(name[0])
                print (name[0])

            testsList.remove("rawData")
        except sqlite3.DatabaseError as e:
            print("sqlite3 error")
            error, = e.args
            sys.stderr.write(error.message)
            self.conn.execute("ROLLBACK")
            self.conn.close()

            raise e

        return testsList

    def getDataCahngedAtRegression(self,testsData):

        RegressionFeatures = []
        for col in testsData.columns:
            if testsData[col].nunique() > 1:
                RegressionFeatures.append(col)

        return testsData.filter(items=RegressionFeatures)


    def insert_test_params(self,testName, DataDic, rawData):
        """
            insert data to "testName" table, if not exist creates.

        """
        new_raw_data_df = pd.DataFrame(columns = ['Time','Key','Value'])

        for i,key in zip(range(len(rawData.keys())),rawData.keys()):

            rawStr = ','.join(map(str,rawData[key]))
            new_raw_data_df.loc[i] = [DataDic['Time'],key,rawStr]

        new_raw_data_df.to_sql("rawData",self.conn, if_exists = 'append',index=False)
        self.conn.commit()
        #dictionary to dataFrame
        df = pd.DataFrame([DataDic], columns=DataDic.keys())
        #insert the rawData to rawData Table in db and the testData to the 'testName' table.

        df.to_sql(testName, self.conn, if_exists='append', index=True)
        self.conn.commit()

    def insert(self,table_name, command, *args):
        """
        Adding new row into existing .db file

        command=tuple([NULL]+len(args)["?"])

        """

        # conn=sqlite3.connect("test_boards.db")
        # cur=conn.cursor()
        self.cur.execute("INSERT INTO %s VALUES %s" % (table_name, command), tuple(args))

        self.conn.commit()

    def update(self,table_name, command, id, *args):
        """
        Updating a row in existing .db file

        """
        my_args = tuple([NULL] + len(args)["?"])
        self.cur.execute("UPDATE %s SET %s WHERE %s" % (table_name, command, id), tuple(args))

        self.conn.commit()


def main():
    f_h=time.ctime().split(' ')[0:5]
    Timestamp='_'+f_h[0]+'_'+f_h[1]+'_'+f_h[2]+'_'+f_h[3].replace(':','_')+'_'+f_h[4]

    constantRecordDic = OrderedDict([ ('User',         'Emanuel'),
                                      ('ProductName',      'PFE'),
                                      ('ProductPhase', 'AAA test'),
                                      ('BoardFabRev',    'rev0'),
                                      ('BoardName',      'Shuttle'),
                                      ('BoardSerial',    '001'),
                                      ('llVersion',      '653498'),
                                      ('FwVersion',      '15'),
                                      ('NvmVersion',     '48'),
                                      ('ChipID',          10),
                                      ('Skew',           'Nominal'),
                                      ("Time",pd.Timestamp.today() )
                               ])

    from os import path
    fname = path.expanduser(r'Z:\Projects\01_06_24.csv')
    data = pd.read_csv(fname, header=None)
    data.__delitem__(0)
##    print(data)

    save_data = []
    DNL = [0,1,2,3,4,5,6]
    INL = [789,1,2,4,5,6,3,5,77]

    save_data.append(pd.Series(DNL,name="DNL"))
    save_data.append(pd.Series(INL,name="INL"))
    save_data.append(pd.Series(INL,name="TTT"))


    df = pd.concat(save_data, axis=1)
    data = pd.concat([df,data], axis=1)
    x = np.random.randn(50, 25)
    random_frame = pd.DataFrame(x)
    data = pd.concat([random_frame, data],axis = 1)
##    print data
    dal= Dal("test_test.db")
##    for i in range(20):
##        time.sleep(2)
##        brkdal.insert_test_params("test1",constantRecordDic,data)
    print dal.getRawDataByTime("Wed Dec 06 15:24:14 2017")

if __name__ == '__main__':
    main()
