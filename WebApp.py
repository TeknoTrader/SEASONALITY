# NB: used pip freeze to get requirements.txt

import streamlit as st
import yfinance as yf
# import matplotlib.pyplot as plt
from datetime import date
import numpy as np
import pandas as pd

AnnoPartenz = st.number_input("Starting year: ",min_value = 1850, step = 1)

AnnoFin = st.number_input("End year: ", min_value = 1900, step = 1)
AnnoFine = int(AnnoFin)
end = date(AnnoFine, 1, 1)
st.write("\nEnd of the relevation: \t", end)

# Testo un attimo l'estrazione di informazioni, quali mesi ed anni
# print(end.month)

ticker = st.text_input("Insert the TICKER: ")
# Preliminary download of data 'GOOG'
data = yf.download(ticker)
# Find the first data avaible, to avoid errors
first_date = data.index[0]
st.write("Data of ",ticker, " avaible from: ",first_date.date())

year = int(first_date.strftime('%Y'))

if year < AnnoPartenz:
  AnnoPartenza = AnnoPartenz
else:
  AnnoPartenza = year+1

# Another control to do
if year >= AnnoFine:
  st.write("\n\tATTENTION!!!\nYou have to choose a data that is ABOVE ", {year})
  AnnoFine = int(input("End year: \n"))
end = date(AnnoFine, 1, 1)
st.write("\nEnd year at: \t", end)

#Inizialization
Annate1 = list(range(AnnoPartenza, AnnoFine))
NomiMesi = list(range(1, 13))

Annate = []  # Conversion of Annate1 's elements in string type
for i in Annate1:
  Annate.append(str(i))

#Now we download the serious data
inizio = date( AnnoPartenza, 1, 1)
st.write("\nStarting calculations from: \t",inizio)

df = yf.download(ticker, start = inizio, end = end, interval = "1mo")

df = pd.DataFrame(df["Open"]) # Riduciamo l'array alle sole aperture

array = []


# Funzione per identificare la varin punti
def Mensilit(mese, startY, endY):
  array = []
  for i in range(startY, endY):
    if (mese != 12):   # Se è dicembre, il mese successivo è gennaio quindi si sta attenti
      m = mese+1
      strt = date(i,mese,1)
      end = date(i,mese+1,1)
      dff = yf.download(ticker,start = strt, end = end, interval = "1mo")
      dffc = pd.DataFrame(dff["Close"])
      dffo = pd.DataFrame(dff["Open"])
      resultAbs = dffc.iat[0,0] - dffo.iat[0,0]  #Nominal return
      result = resultAbs * 100 / dffo.iat[0,0]  #In percentage
      array.append(result)
    else:
      m = mese+1
      strt = date(i,mese,1)
      end = date(i+1,1,1)
      dff = yf.download(ticker,start = strt, end = end, interval = "1mo")
      dffc = pd.DataFrame(dff["Close"])
      dffo = pd.DataFrame(dff["Open"])
      resultAbs = dffc.iat[0,0] - dffo.iat[0,0]   #Nominal return
      result = resultAbs * 100 / dffo.iat[0,0]   #In percentage
      array.append(result)
  return array

def Media(Arr):
  tot = 0
  for i in Arr:
    tot += i
  return (tot/len(Arr))

def WinRate(Arr):
  tot = 0
  for i in Arr:
    if(i>=0):
      tot+=1
  if(tot==0):
    return 0
  else:
    return (100/len(Arr)*tot)


# We start to create the list to keep in consideration
WRComplessivi=[]
MesiComplessivi=[]

NomiMesi1 = ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"] # Defining the names of the months

# Select the colors of the chart
def Color(negclr,posclr,element,minimum):
  if (float(element) < float(minimum)):
    return (negclr)
  else:
    return (posclr)

#------------------------------------------------------
#------------------------------------------------------
# We are going to:
# 1)Visualize the results of the 12 months of the year
# 2)Create an array that contains the data to analyze how does the varius seasons of the year performs
#------------------------------------------------------
# LET'S START WITH THE POINT 1!!!
#------------------------------------------------------
#------------------------------------------------------
for i in range (1,13):
  Mese = Mensilit(i,AnnoPartenza,AnnoFine)   # Si identifica la var di prezzo avvenuta
  colori = [] #Colors array
  for Y in Mese:
    colori.append(Color("#FF0000","#0000FF",Y,0))

# Defining a good title, to make everything more clear
  st.write("# MONTHLY RETURNS on the month of: ",NomiMesi1[i-1],"\n")
  st.write("# WIN RATE: ",round(WinRate(Mese),2), "%\n")
  st.write("# AVERAGE RETURN: ",round(Media(Mese),2), "%\n")
  st.write("Better excursion: ",round(max(Mese),2),"%")
  st.write("Worst excursion:  ", round(min(Mese),2), "%")
  #st.xlabel("Anni")C:\Users\tekno\PycharmProjects\Streamlit\Seasonality.py [ARGUMENTS]
  #st.ylabel("Rendimenti")
  MesiComplessivi.append(round(Media(Mese),2))  # Add to the array the value for the next chart
  #st.show()  # Show the chart
  WRComplessivi.append(round(WinRate(Mese),2))  # Add to the array the value for the next chart
  st.write (len (colori))
  st.bar_chart(dict(zip(np.array(Annate), np.array(Mese)))) #,color=colori) # Plot the bar chart of the results
  #st.axhline(0,color = "green")  # Horizontal line, to see better where are the positive and negative returns
