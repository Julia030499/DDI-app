import streamlit as st
import pandas as pd

#Datenbank laden Quelle: https://gist.github.com/nikkisharma536/650a2dae1cbd507ecd449671d839261b
@st.cache_data
def load_data():
    return pd.read_csv("CombinedDatasetConservativeTWOSIDES3.csv", sep = ';', on_bad_lines = 'skip')

df = load_data()

st.title("Check your Drugs") 


# Medikamentennamen sammeln, NaN entfernen, zu String konvertieren und sortieren; Quelle: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html
def get_all_medications(df):
    meds1 = df["object"].dropna().astype(str).str.strip()
    meds2 = df["precipitant"].dropna().astype(str).str.strip()
    all_meds = pd.Series(pd.concat([meds1, meds2])).drop_duplicates() 
    return sorted(all_meds)

alle_medikamente = get_all_medications(df)

# Eingabefelder mit Autovervollständigung Quelle: https://discuss.streamlit.io/t/how-can-i-add-a-user-input-box-that-gives-an-auto-complete-suggestion-from-a-list-but-also-allows-user-too-input-its-own-query/15502
med1 = st.selectbox("choose first drug:", alle_medikamente)
med2 = st.selectbox("choose second drug:", alle_medikamente)

if med1 and med2:
    med1_clean = med1.strip().lower()
    med2_clean = med2.strip().lower()

    # med1 & med2 oder med2 & med1 
    wechselwirkung = df[
        ((df["object"].str.lower() == med1_clean) & (df["precipitant"].str.lower() == med2_clean)) |
        ((df["object"].str.lower() == med2_clean) & (df["precipitant"].str.lower() == med1_clean))
    ]

    if not wechselwirkung.empty:
        row = wechselwirkung.iloc[0]
        if row["contraindication"] == True:
            st.error("Kontraindikation! Kombination sollte vermieden werden")
        elif row["precaution"] == True:
            st.warning("Vorsicht! Kombination erfordert besondere Aufmerksamkeit.")
        else:
            st.success("Keine kritische Wechselwirkung.")
    else:
        st.info("Keine bekannte Wechselwirkung in Datenbank gefunden.")
