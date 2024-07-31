import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
import numpy as np
import math
import matplotlib.patches as mpatches

AnnoPartenza = int(input("Anno di partenza: \n"))
inizio = date(AnnoPartenza,1,1)
print("\nInizio calcolo dal: \t",inizio)

AnnoFine = int(input("Anno di fine: \n"))
end = date(AnnoFine,1,1)
print("\nFine rilevazione al: \t",end)

# Testo un attimo l'estrazione di informazioni, quali mesi ed anni
#print(end.month)

Annate1 = list(range(AnnoPartenza,AnnoFine))
NomiMesi = list(range(1,13))

Annate = []  # Conversion of Annate1 's elements in string type
for i in Annate1:
  Annate.append(str(i))

ticker = input("Inserisci il ticker:\n")
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
  return (tot/len(Arr))

def WinRate(Arr):
  tot = 0
  for i in Arr:
    if(i>=0):
      tot+=1
  return (100/len(Arr)*tot)


# Ora finalmente COMINCIAMO A CREARE I CONTENITORI
WRComplessivi=[]
MesiComplessivi=[]

NomiMesi1 = ["GENNAIO","FEBBRAIO","MARZO","APRILE","MAGGIO","GIUGNO","LUGLIO","AGOSTO","SETTEMBRE","OTTOBRE","NOVEMBRE","DICEMBRE"]

# Select the colors of the chart
def Color(negclr,posclr,element,minimum):
  if (float(element) < float(minimum)):
    return (negclr)
  else:
    return (posclr)

for i in range (1,13):
  Mese = Mensilit(i,AnnoPartenza,AnnoFine)   # Si identifica la var di prezzo avvenuta
  colori = [] #Colors array
  for Y in Mese:
    colori.append(Color("red","blue",Y,0))
  plt.bar(np.array(Annate),np.array(Mese),color=np.array(colori)) # Plot the bar chart of the results
  plt.axhline(0,color = "green")  # Horizontal line, to see better where are the positive and negative returns

    # Varianza
  DevStd = math.sqrt(sum((x - Media(Mese)) ** 2 for x in Mese) / len(Mese))

  # Stampa a video!
  plt.title(f"RITORNI MENSILI DEL MESE {NomiMesi1[i-1]}\n\
  Win rate: {round(WinRate(Mese),2)}%\n\
  Ritorno medio: {round(Media(Mese),2)}%\n\
  Standard deviation: {round(DevStd,2)}%")
  plt.axhline(Media(Mese),color = "red")
  plt.xlabel("Anni")
  plt.ylabel("Rendimenti")

  MesiComplessivi.append(round(Media(Mese),2))  # Add to the array the value for the next chart

 # Aggiungi la legenda
  band_patch = mpatches.Patch(color='gray', alpha=0.3, label=f"± Deviazione standard ({DevStd}%)")
  plt.legend(handles=[plt.Line2D([0], [0], color="red", lw=4, label="Mesi negativi"),
                      plt.Line2D([0], [0], color="blue", lw=4, label="Mesi positivi"),
                      plt.Line2D([0], [0], color="red", lw=2, label="Media dei rendimenti"),
                      band_patch],
             loc='upper left', bbox_to_anchor=(1, 1))

  # Fill between

  plt.fill_between(
    Annate,
    Media(Mese) + DevStd,
    Media(Mese) - DevStd,
    color='none',
    alpha=0.3,
    hatch="X",
    edgecolor="gray",
    label=f"± Deviazione standard ({DevStd}%)")

  # Show the chart
  plt.show()
  WRComplessivi.append(round(WinRate(Mese),2))  # Add to the array the value for the next chart

NomiMesi2 = ["Genn","Febb","Mar","Apr","Magg","Giu","Lugl","Ago","Sept","Oct","Nov","Dec"]

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
