import os,sys
import shutil
import pandas as pd
from openpyxl import load_workbook


class CsvHandler():

    def __init__(self,FilePath=None):
        """
        If File Path given it returns File object or creates an empty file @ given path
        :param FilePath:
               sheetname:

        """
        if FilePath is None:

            print("CSV File Object not created")

        else:
            try:

                if not os.path.exists(FilePath):
                    print("File not exist- Creating new .csv file @ given path")
                    self.df=self.CreateEmptyFile(FilePath)

                else:
                    if os.path.split(FilePath)[1].split('.')[1]!="csv":
                        print("Not a valid csv file or missed .csv")
                        raise("Please provide the accurate path")

            except:
                raise


    def CreateEmptyFile(self,Path,Header=[],save_now=False):
        """
        Creating Empty Excel file @ specific path
        :return:
        """

        df = pd.DataFrame(columns=Header)
        df.to_csv(Path)

        return(df)


    def ReadFromExistedFile(self,Path):

        CsvFile=pd.read_csv(Path,index_col=0)

        return(CsvFile)

    def AppendDataFrames(self,df1,df2):

        """
        DataFrames should have same column names

        :param df1:
        :param df2:
        :return:
        """

        df = df1.append(df2, ignore_index=True)

        return(df)

class ExcelHandler():

    def __init__(self,FilePath=None,sheetname=None):
        """
        If File Path given it returns File object or creates an empty file @ given path
        :param FilePath:
               sheetname:

        """
        if FilePath is None:

            print("Excel File Object not created")

        else:
            try:

                if not os.path.exists(FilePath):
                    print("File not exist- Creating new .xlsx file @ given path")
                    self.CreateEmptyFile(FilePath)

                else:
                    if os.path.split(FilePath)[1].split('.')[1]!="xlsx":
                        print("Not a valid Excel file or missed .xlsx")
                        raise("Please provide the accurate path")
                    else:
                        print("Creating Excel witer @ %s"%FilePath)
                        self.writer=pd.ExcelWriter(FilePath)

            except:
                raise

    def CreateEmptyFile(self,Path,sheetname="Sheet1",Header=[],save_now=False):
        """
        Creating Empty Excel file @ specific path
        :return:
        """

        df = pd.DataFrame(columns=Header)
        writer = pd.ExcelWriter(Path, engine='openpyxl')
        df.to_excel(writer,sheetname,index=False)
        if save_now:
            writer.save()
            return

        return(writer)


    def ReadFromExistedFile(self,RegPath,sheet_name):

        ExcelFile=pd.read_excel(RegPath, sheet_name=sheet_name, index_col=0)

        return(ExcelFile)

    def WriteToNewFile(self,path,sheetname,ws_dict):

        with pd.ExcelWriter(path,engine='xlsxwriter',datetime_format='yyyy-mm-dd',date_format='yyyy-mm-dd') as writer:
            for ws_name,df_sheet in ws_dict.items():
                df_sheet.to_excel(writer, sheet_name=ws_name)


    def WriteToExistedFile(self,filename, df, sheet_name='Sheet1', startrow=0,**to_excel_kwargs):
        """
        Usage
        append_df_to_excel('d:/temp/test.xlsx', df)

        append_df_to_excel('d:/temp/test.xlsx', df, header=None, index=False)

        append_df_to_excel('d:/temp/test.xlsx', df, sheet_name='Sheet2', index=False)

        append_df_to_excel('d:/temp/test.xlsx', df, sheet_name='Sheet2', index=False, startrow=25)

        Append a DataFrame [df] to existing Excel file [filename]
        into [sheet_name] Sheet.
        If [filename] doesn't exist, then this function will create it.

        Parameters:
          filename : File path or existing ExcelWriter
                     (Example: '/path/to/file.xlsx')
          df : dataframe to save to workbook
          sheet_name : Name of sheet which will contain DataFrame.
                       (default: 'Sheet1')
          startrow : upper left cell row to dump data frame.
                     Per default (startrow=None) calculate the last row
                     in the existing DF and write to the next row...
          to_excel_kwargs : arguments which will be passed to `DataFrame.to_excel`
                            [can be dictionary]

        Returns: None
        """
        # ignore [engine] parameter if it was passed
        if 'engine' in to_excel_kwargs:
            to_excel_kwargs.pop('engine')

        # create a writer
        writer = pd.ExcelWriter(filename, engine='openpyxl')

        try:
            # try to open an existing workbook
            writer.book = load_workbook(filename)
            # get the last row in the existing Excel sheet
            # copy existing sheets
            writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
        except:
            print("Probably file not exist or permission denied")
            raise

        # write out the new sheet
        df.to_excel(writer, sheet_name, startrow=startrow, **to_excel_kwargs)

        # save the workbook
        writer.save()
		
		



def MakeArchive(path,ArchiveName):

    archive_name = os.path.expanduser(os.path.join(path,ArchiveName))
    root_dir = os.path.expanduser(os.path.join(path,'Backup'))
    shutil.make_archive(archive_name, 'gztar', root_dir)

	

	
if __name__=="__main__":

    path=r'C:\Users\User\Documents\Python Scripts'

    ArchiveName='Test'
		