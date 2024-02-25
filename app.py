import pandas as pd
import streamlit as st
import re
import os
import editdistance
import json

quotes_pattern = r'[\s.]".+"[\s.]'
quotes_pattern =  r'[^<>]".+"[^<>]'
quotes_pattern = r"""[\u0590-\u05fe]"[^\u0590-\u05fe]"""
quotes_pattern = r"""[^\u0590-\u05fe]"[\u0590-\u05fe]?"""
word_quotes_pattern = r"""[\u0590-\u05fe]"[\u0590-\u05fe]"""
word_quotes_pattern2 = r"""[\u0590-\u05fe]״[\u0590-\u05fe]"""

#import openpyxl
cols_ora_data = ['Submission ID','Location',\
 'Problem Name','Item ID','Anonymized Student ID','Date/Time Response Submitted','Response','Assessment Details','Assessment Scores','Date/Time Final Score Given','Final Score Points Earned',\
'Final Score Points Possible',\
 'Feedback Statements Selected',\
 'Feedback on Peer Assessments']

dfs = []

def get_response_text(s):
    try:
        return json.loads(s)["parts"][0]["text"]
    except Exception as e:
        if isinstance(s, str):
             return s.replace("""{"parts": [{"text": :""","")
        else:
            return ""
def get_quotes(x):
    x_filtered_words = re.sub(word_quotes_pattern,"",x)
    x_filtered_words = re.sub(word_quotes_pattern2,"",x_filtered_words)

    quotes_1 = set(re.findall('".+"',x_filtered_words))
    quotes_2 = set(re.findall('״.+״',x_filtered_words))
    return list(quotes_1 | quotes_2)


def get_num_of_quotes(x):
   return len(get_quotes(x))



def get_number_of_words(s):
    return len(get_words(s))


def get_words(s):
    return s.split()

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

import re

word_pattern = r'\W+'

st.markdown("<h1 style='text-align: center; color: #F63366;'>Noa's</h1>", unsafe_allow_html=True)
#st.markdown("<h3 style='text-align: left; color: #F63366;'>Choose 3 Excels Files</h3>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("Choose 3 Excel Files", accept_multiple_files=True,type = ["xlsx"])
#st.cache_data.clear()
message = st.text(body = "")
files_set= set()

for uploaded_file in uploaded_files:
    try:        

        if re.search("ora_data",uploaded_file.name,re.IGNORECASE):
            df_ora_data = pd.read_excel(uploaded_file)
            cols = list(df_ora_data.iloc[-2, :])
            df_ora_data.columns = cols
            files_set.add("ora_data")

        
        if re.search("anonymized_ids",uploaded_file.name,re.IGNORECASE):
            df_anonymized_ids = pd.read_excel(uploaded_file,skiprows=1)
            files_set.add("anonymized_ids")



        if re.search("student_profile_info",uploaded_file.name,re.IGNORECASE):
            df_student_profile_info = pd.read_excel(uploaded_file,skiprows=1)
            files_set.add("student_profile_info")

       

    except Exception as e:
        st.write("exception",e)
        
if len(files_set)==3:
            df23 = df_anonymized_ids.merge(df_student_profile_info,left_on="User ID",right_on="id")
            df123 = df_ora_data.merge(df23,left_on="Anonymized Student ID",right_on="Course Specific Anonymized User ID")
            df123["response_text"] = df123["Response"].apply(lambda x: get_response_text(x))
            #df123["response_words"] = df123["response_text"].apply(lambda x: get_words(x))
            df123["response_num_words"] = df123["response_text"].apply(lambda x: get_number_of_words(x))
            df123["response_quotes"] = df123["response_text"].apply(lambda x:get_quotes(x))
            df123["response_num_quotes"] = df123["response_text"].apply(lambda x: get_num_of_quotes(x))
            #df123["jaccard_similarity"] = df123["response_text"].apply(lambda x: )


            csv = convert_df(df123)


    
            st.download_button(
               "Press to Download Merged CSV file",
               csv,
               "noa_merged.csv",
               "text/csv",
               key='download-csv'
            )


else:
    pass
    #message.write("Files:"+ ",".join(list(files_set)))
        

    
