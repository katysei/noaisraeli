import pandas as pd
import streamlit as st
import re
import os

#import openpyxl
cols_ora_data = ['Submission ID','Location',\
 'Problem Name','Item ID','Anonymized Student ID','Date/Time Response Submitted','Response','Assessment Details','Assessment Scores','Date/Time Final Score Given','Final Score Points Earned',\
'Final Score Points Possible',\
 'Feedback Statements Selected',\
 'Feedback on Peer Assessments']

dfs = []

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')



st.header("Noa's", divider='rainbow')
  
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
st.cache_data.clear()
message = st.text(body = "")
files_set= set()
#df = pd.read_excel("ono/JPPI_ACD_SPOC_IsraeliIdentity_HE_2023_1_ccx_22269_anonymized_ids_2024-02-11-1154.xlsx") 

for uploaded_file in uploaded_files:
    try:        

        if re.search("ora_data",uploaded_file.name,re.IGNORECASE):
            df_ora_data = pd.read_csv(uploaded_file)
            df_ora_data.columns = cols_ora_data
            files_set.add("ora_data")
            #dfs.append(df_ora_data)
           
        
        if re.search("anonymized_ids",uploaded_file.name,re.IGNORECASE):
            df_anonymized_ids = pd.read_csv(uploaded_file,skiprows=1)
            files_set.add("anonymized_ids")
            dfs.append(df_anonymized_ids)
           


        if re.search("student_profile_info",uploaded_file.name,re.IGNORECASE):
            df_student_profile_info = pd.read_csv(uploaded_file,skiprows=1)
            dfs.append(df_student_profile_info)
            files_set.add("student_profile_info")

       

        #dfs.append(df)
    except Exception as e:
        st.write("exception",e)
        
if len(files_set)==3:
            df23 = df_anonymized_ids.merge(df_student_profile_info,left_on="User ID",right_on="id")
            df123 = df_ora_data.merge(df23,left_on="Anonymized Student ID",right_on="Anonymized User ID")
    
            csv = convert_df(df23)
    
            st.download_button(
               "Press to Download",
               csv,
               "file.csv",
               "text/csv",
               key='download-csv'
            )
else:
    message.write("Files: "+ str(files_set))
        

    
