# Please note that the code is now incomplete and that it is a work in progress!!!

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import numpy as np

AnnoPartenz = int(input("Anno di partenza: \n"))

AnnoFine = int(input("Anno di fine: \n"))
end = date(AnnoFine,1,1)
print("\nFine rilevazione al: \t",end)

# Testo un attimo l'estrazione di informazioni, quali mesi ed anni
#print(end.month)

ticker = input("Inserisci il ticker:\n")
# Preliminary download of data 'GOOG'
data = yf.download(ticker)
# Find the first data avaible, to avoid errors
first_date = data.index[0]
print(f"Data of {ticker} avaible from {first_date.date()}")

year = int(first_date.strftime('%Y'))

if (year < AnnoPartenz):
  AnnoPartenza = AnnoPartenz
else:
  AnnoPartenza = year+1

# Another control to do
if(year >= AnnoFine):
  print("\n\TATTENTION!!!\nYou have to choose a data that is ABOVE ",{year})
  AnnoFine = int(input("Anno di fine: \n"))
end = date(AnnoFine,1,1)
print("\nFine rilevazione al: \t",end)

#Inizialization
Annate1 = list(range(AnnoPartenza,AnnoFine))
NomiMesi = list(range(1,13))

Annate = []  # Conversion of Annate1 's elements in string type
for i in Annate1:
  Annate.append(str(i))

#Now we download the serious data
inizio = date(AnnoPartenza,1,1)
print("\nInizio calcolo dal: \t",inizio)

df = yf.download(ticker, start = inizio, end = end, interval = "1mo")

df = df["Open"] # Riduciamo l'array alle sole aperture

array = []


# Funzione per identificare la varin punti
def Mensilit(mese,startY,endY):
  array = []
  for i in range(startY,endY):
    if (mese != 12):   # Se è dicembre, il mese successivo è gennaio quindi si sta attenti
      m = mese+1
      strt = date(i,mese,1)
      end = date(i,mese+1,1)
      dff = yf.download(ticker,start = strt, end = end, interval = "1mo")
      resultAbs = dff["Close"][0] - dff["Open"][0]  #Nominal return
      result = resultAbs * 100 / dff["Open"][0]  #In percentage
      array.append(result)
    else:
      m = mese+1
      strt = date(i,mese,1)
      end = date(i+1,1,1)
      dff = yf.download(ticker,start = strt, end = end, interval = "1mo")
      resultAbs = dff["Close"][0] - dff["Open"][0]   #Nominal return
      result = resultAbs * 100 / dff["Open"][0]   #In percentage
      array.append(result)
  return array

def Media(Arr):
  tot = 0
  for i in Arr:
    tot += i
  return (i/len(Arr))

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
    colori.append(Color("red","blue",Y,0))
  plt.bar(np.array(Annate),np.array(Mese),color=np.array(colori)) # Plot the bar chart of the results
  plt.axhline(0,color = "green")  # Horizontal line, to see better where are the positive and negative returns

# Defining a good title, to make everything more clear
  plt.title(f"RITORNI MENSILI DEL MESE {NomiMesi1[i-1]}\n\
  WIN RATE: {round(WinRate(Mese),2)}%\n\
  AVERAGE RETURN: {round(Media(Mese),2)}%\n\
  \n\
  Better excursion: {round(max(Mese),2)}%\n\
  Worst excursion:  {round(min(Mese),2)}%")
  plt.xlabel("Anni")
  plt.ylabel("Rendimenti")
  MesiComplessivi.append(round(Media(Mese),2))  # Add to the array the value for the next chart
  plt.show()  # Show the chart
  WRComplessivi.append(round(WinRate(Mese),2))  # Add to the array the value for the next chart

NomiMesi2 = ["Jan","Feb","Mar","Apr","May","JuN","JuL","Aug","Sept","Oct","Nov","Dec"]  # Abbreviated month's name

plt.title("Rendimento complessivo mesi")
color = []
for i in MesiComplessivi:
  color.append(Color("red","green",i,0.0))
plt.barh(NomiMesi2,MesiComplessivi,color = color)
plt.axvline(0,color = "blue")
plt.xlabel("Rendimenti")
plt.ylabel("Anni")
plt.show()

# Second type of colors function
# We are going to create 3 colors interval
def Color(clr1,clr2,clr3,element,value1,value2):
  if (float(element) <= float(value1)):
    return (clr1)
  elif (float(value2) <= float(element)):
    return (clr3)
  else:
    return (clr2)

color = []
for i in WRComplessivi:
  color.append(Color("red","yellow","blue",i,25,75))
plt.barh(NomiMesi2, WRComplessivi,color = color)
plt.axvline(25,color = "red")
plt.axvline(50,color = "yellow")
plt.axvline(75,color = "blue")
plt.legend(["Profitability at 25% or below","Profitability from 25% to 75%","Profitability at 75% or above"],loc='center left', bbox_to_anchor=(1, 0.5))
plt.title("Grafico dei mesi più profittevoli")
plt.xlabel("Win rate")
plt.ylabel("Mesi")

plt.show()
