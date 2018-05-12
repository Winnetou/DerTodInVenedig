# script to convert xlsx into :class:`pandas.DataFrame` object
import pandas

def read_data_to_df(xlsx_path):
    """
    Read the xlsx file, keep only interesting data,
    reshape for easy querying 
    :return: 
    """
    mors = pandas.read_excel(xlsx_path, skiprows=range(0,6),header=0,usecols=200)
    # Only keep the median observations and ISO Code, U5MR, IMR and NMR columns
    mors = mors[mors['Uncertainty bounds*'] == 'Median']
    mors.set_index(mors['ISO Code'])
    del mors['Uncertainty bounds*']
    del mors['CountryName']
    # Bring the DataFrame into long format with a new column for year
    stubnames = ['U5MR', 'IMR', 'NMR']
    final_df = pandas.wide_to_long(mors, stubnames=stubnames, i='ISO Code', j='year', sep='.')
    return final_df
