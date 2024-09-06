import pandas as pd
from datetime import datetime
import logging
from config import *
from utils import executable_time
import os
from typing import Optional


class Detectors():
    def __init__(self):
        self._indication_df: pd.DataFrame = pd.DataFrame()
        self._status_df: pd.DataFrame = pd.DataFrame()
        self._loaded_file: set(str) = set()
    
    @property
    def count_detector(self):
        return self._indication_df.shape[1]
    
    @property
    def count_values(self):
        return self._indication_df.shape[0]

    def get_indication(self, kks:str, start_time:Optional[datetime]=None, finish_time:Optional[datetime]=None):
        logging.info(f"GET {kks}, Time: {start_time} - {finish_time}")
        s:pd.Series = self._indication_df.get(kks)
        s = s[s.index >= start_time] if start_time and isinstance(start_time,datetime) else s
        s = s[s.index <= finish_time]if finish_time and isinstance(finish_time,datetime) else s
        return s

    @executable_time
    def load_rsa_file(self, file_name:str):
        """ 
            read data from RSA file 
            params:
                file_name <str>: name of RSA file
            return:
                df_value - DataFrame with detectors value 
                df_status - DataFrame with detectors status   
        """
        with open(file_name, 'r', encoding='koi8-r') as file:
            # пропускаем всестроки до KKS
            for line in file:
                if line.find('SignalsArray') != -1:
                    break
            
            # читаем все строки с KKS
            kks_list = []
            while line.startswith('SignalsArray'):
                # удаляю SignalsArray= и получаю массив с KKS из строки
                kks_list.extend(line[13:].strip('; \n').split(';'))
                line = file.readline()
            
            # dates - список дат из файла
            # indication_table - двумерный массив показаний датчика(строка - момент времени, столбец - показания датчика)
            # status_table - двумерный массив статусов датчика(строка - момент времени, столбец - статус датчика)
            dates:list[datetime] = list()                
            indication_table:list[list[float]] = list()
            status_table:list[list[int]] = list()

            for line in file:
                # пропускаем все строки, которые не содержат данных в том числе текущую
                if line.startswith('RsaData'):
                    # удаляю из строки RsaData=
                    datas = line[8:].strip(';\n').split(';')
                    # получаю дату и время
                    dates.append(datetime.strptime(datas.pop(0),f'%d.%m.%Y %H:%M:%S.%f'))
                    
                    # список значений и статусов
                    indications:list[float] = list()
                    statuses:list[int] = list()
                
                    # разбиваю строку и получаю список из показаний датчика и статуса этого показания  
                    for data in datas:
                        *_, val, status = data.split()
                        # показания датчика
                        try:
                            indications.append(float(val))
                        except ValueError:
                            logging.error(f"{val} is not float")
                            indications.append(-1)
                        # статус показаний
                        try:
                            statuses.append(int(status))
                        except ValueError:
                            logging.error(f"{status} is not integer")
                            statuses.append(STATUS_ERROR)
                    
                    indication_table.append(indications)
                    status_table.append(statuses)
            self._indication_df = pd.DataFrame(indication_table, index=dates, columns=kks_list)
            self._status_df = pd.DataFrame(status_table, index=dates, columns=kks_list)
            self._loaded_file.add(os.path.abspath(file_name))
