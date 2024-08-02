# NB: used pip freeze to get requirements.txt
import sys
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import numpy as np
import pandas as pd
import math
import matplotlib.patches as mpatches
import altair as alt

# MANCA SOLO:
#0) Formattazione di Altair
#1) Scelta tra visualizzazione (immagine, altair o dataframe [scaricabile o solo visualizzazione bellina e color?])
#2) Error handling SP500: deve identificare qual è la prima "data non corrotta" e dire all'utente che cosa cazzo sta succedendo
#3) Codice IN INGLESE!!!
#4) Formattazione colori overall average drawdown (i colori devono essere basati sulla media oscillazioni e sulla varianza)
# Url of yahoo!finance ticker's list
url = "https://finance.yahoo.com/lookup/"

current_year = datetime.now().year # Current year

# Introduction for the user
st.write("# LET'S ANALYZE THE SEASONALITY OF AN ASSET 📊")
st.write("### You have just to set: when to start with the monitoration,when to end and which is the asset to see")
st.write("Please, note that it has been used the YAHOO! FINANCE API, so you have to select the ticker of the asset based on the yahoo!finance database")
st.write("You can check the name of the asset 🔍 you're searching at this [link](%s)" % url)

AnnoPartenz = st.number_input("Starting year 📅: ",min_value = 1850, max_value=current_year-1, step = 1)

AnnoFin = st.number_input("End year 📅: ", value = current_year, min_value = 1900, max_value=current_year, step = 1)

# Testo un attimo l'estrazione di informazioni, quali mesi ed anni

ticker = st.text_input("Insert the TICKER 📈: ", value="GOOG")
# Verify the ticker
try:
  asset = yf.Ticker(ticker)
  info = asset.info
  info.get('longName', 'N/A')
  if info and "error" in info:
      st.warning(f"⚠️ # The asset {ticker} doesn't exist. ⚠️")
      st.write("### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
      sys.exit(1)
except Exception as e:
    st.warning(f"⚠️ # Error with the asset {ticker}.")
    st.write("### Probably you didn't insert the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)\n")
    st.write(f"Fing here more details: \n{str(e)}")
    sys.exit(1)

asset = yf.Ticker(ticker)
info = asset.info
asset_name = info.get('longName', 'N/A')
def main():
  AnnoFine = int(AnnoFin)
  end = date(AnnoFine, 1, 1)
  st.write("\nEnd of the relevation: \t", end)
  year = 0
  try:
    data = yf.download(ticker)
    if not data.empty:
      # Find the first data avaible, to avoid errors
      first_date = data.index[0]
      st.write("Data of ", ticker, " avaible from: ", first_date.date())

      year = int(first_date.strftime('%Y'))
    else:
      st.warning(f"⚠️ # The asset {ticker} doesn't exist. ⚠️")
      st.write(
        "### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
      sys.exit(1)
  except Exception as e:
    # Se non ci sono dati disponibili, fornire un messaggio personalizzato
    st.warning(f"⚠️ # The asset {ticker} doesn't exist. ⚠️")
    st.write("### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
    sys.exit(1)

  # Another control to do
  if year >= AnnoFine:
    st.write("\n\tATTENTION!!!\nYou have to choose a data that is ABOVE ", {year})
    AnnoFine = int(input("End year: \n"))
    sys.exit(1)
  end = date(AnnoFine, 1, 1)
  st.write("\nEnd year at: \t", end)

  if year < AnnoPartenz:
    AnnoPartenza = AnnoPartenz
  else:
    AnnoPartenza = year + 1

  # Inizialization
  Annate1 = list(range(AnnoPartenza, AnnoFine))
  NomiMesi = list(range(1, 13))
  number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣","🔟", "1️⃣1️⃣", "1️⃣2️⃣"] # There is no unicode for 2 decimals numbers

  Annate = []  # Conversion of Annate1 's elements in string type
  for i in Annate1:
    Annate.append(str(i))

  inizio = date(AnnoPartenza, 1, 1)
  # Now we download the serious data
  st.write("\nStarting calculations from: \t", inizio)

  df = yf.download(ticker, start=inizio, end=end, interval="1mo")

  df = pd.DataFrame(df["Open"])  # Riduciamo l'array alle sole aperture

  array = []

  # Funzione per identificare la varin punti
  def Mensilit(mese, startY, endY):
    array = []
    for i in range(startY, endY):
      if (mese != 12):  # Se è dicembre, il mese successivo è gennaio quindi si sta attenti
        m = mese + 1
        strt = date(i, mese, 1)
        end = date(i, mese + 1, 1)
        dff = yf.download(ticker, start=strt, end=end, interval="1mo")
        dffc = pd.DataFrame(dff["Close"])
        dffo = pd.DataFrame(dff["Open"])
        resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
        result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
        array.append(result)
      else:
        m = mese + 1
        strt = date(i, mese, 1)
        end = date(i + 1, 1, 1)
        dff = yf.download(ticker, start=strt, end=end, interval="1mo")
        dffc = pd.DataFrame(dff["Close"])
        dffo = pd.DataFrame(dff["Open"])
        resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
        result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
        array.append(result)
    return array

  def Media(Arr):
    tot = 0
    for i in Arr:
      tot += i
    return (tot / len(Arr))

  def WinRate(Arr):
    tot = 0
    for i in Arr:
      if (i >= 0):
        tot += 1
    if (tot == 0):
      return 0
    else:
      return (100 / len(Arr) * tot)

  # We start to create the list to keep in consideration
  WRComplessivi = []
  MesiComplessivi = []

  NomiMesi1 = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
               "NOVEMBER", "DECEMBER"]  # Defining the names of the months

  # Select the colors of the chart
  def Color(negclr, posclr, element, minimum):
    if (float(element) < float(minimum)):
      return (negclr)
    else:
      return (posclr)

  def Color2(clr1, clr2, clr3, element, value1, value2):
    if element <= value1:
      return clr1
    elif value2 <= element:
      return clr3
    else:
      return clr2

  # ------------------------------------------------------
  # ------------------------------------------------------
  # We are going to:
  # 1)Visualize the results of the 12 months of the year
  # 2)Create an array that contains the data to analyze how does the varius seasons of the year performs
  # ------------------------------------------------------
  # LET'S START WITH THE POINT 1!!!
  # ------------------------------------------------------
  # ------------------------------------------------------

  for i in range(1, 13):
    Mese = Mensilit(i, AnnoPartenza, AnnoFine)  # Si identifica la var di prezzo avvenuta
    colori = []  # Colors array
    for Y in Mese:
      colori.append(Color("#FF0000", "#0000FF", Y, 0))

    # Defining a good title, to make everything more clear
    st.write("# ",number_emojis[i-1],"MONTHLY RETURNS of", asset_name, "on the month of: ", NomiMesi1[i - 1], "\n")
    st.write("# WIN RATE: ", round(WinRate(Mese), 2), "%\n")
    st.write("# AVERAGE RETURN: ", round(Media(Mese), 2), "%\n")

    DevStd = math.sqrt(sum((x - Media(Mese)) ** 2 for x in Mese) / len(Mese))
    st.write("### Standard deviation:  ", round(DevStd,2), "%")

    st.write("Better excursion: ", round(max(Mese), 2), "%")
    st.write("Worst excursion:  ", round(min(Mese), 2), "%")

    # Arrays for later
    MesiComplessivi.append(round(Media(Mese), 2))  # Add to the array the value for the next chart
    WRComplessivi.append(round(WinRate(Mese), 2))  # Add to the array the value for the next chart

    # Columns
    col1, col2 = st.columns(2)
    xsize = 10
    ysize = 10
    with col2:
      st.bar_chart(dict(zip(np.array(Annate), np.array(Mese))))
      plt.figure(figsize=(xsize, ysize))
      plt.bar(np.array(Annate), np.array(Mese), color=np.array(colori))
      plt.axhline(0, color="green")

    with col1:
      fig, ax = plt.subplots(figsize=(xsize, ysize))  # Aumentato ulteriormente per assicurare spazio

      # Disegna il grafico a barre
      ax.bar(Annate, Mese, color=['blue' if x >= 0 else 'red' for x in Mese])

      # Aggiungi la linea della media
      ax.axhline(Media(Mese), color="red", linestyle='--', linewidth=2)
      ax.axhline(0, color="green")

      # Aggiungi le etichette degli assi
      ax.set_xlabel("Anni")
      ax.set_ylabel("Rendimenti")

      # Crea il patch per la deviazione standard
      band_patch = mpatches.Patch(color='gray', alpha=0.3, label=f"± Deviazione standard ({round(DevStd, 2)}%)")

      # Aggiungi la banda della deviazione standard
      ax.fill_between(
        Annate,
        Media(Mese) + DevStd,
        Media(Mese) - DevStd,
        color='gray',
        alpha=0.3,
        hatch="X",
        edgecolor="gray",
        label=f"± Deviazione standard ({DevStd}%)"
      )

      # Crea la legenda
      ax.legend(handles=[
        plt.Line2D([0], [0], color="red", lw=4, label="Mesi negativi"),
        plt.Line2D([0], [0], color="blue", lw=4, label="Mesi positivi"),
        plt.Line2D([0], [0], color="red", linestyle='--', lw=2, label="Media dei rendimenti"),
        band_patch],
        loc='upper right'  # Posiziona la legenda nell'angolo in alto a destra
      )

      # Ruota le etichette dell'asse x per una migliore leggibilità
      plt.xticks(rotation=45, ha='right')

      # Adatta il layout
      plt.tight_layout()

      # Mostra il grafico in Streamlit
      st.pyplot(fig)

      # Chiudi la figura per liberare memoria
      plt.close(fig)

    # Definisci gli array
    Assex = range(2000, 2006)
    Assey = [2, 4, -1, 7, -10, 3]

    # Crea un DataFrame
    df = pd.DataFrame({
      'Anno': Assex,
      'Valore': Assey
    })

    # Calcola il dominio dell'asse Y basato sui dati
    y_min = min(min(Assey), -5)
    y_max = max(max(Assey), 4)
    y_domain = [y_min - 1, y_max + 1]  # Aggiungiamo un po' di spazio

    # Crea il grafico base con Altair
    base = alt.Chart(df).encode(
      x=alt.X('Anno:O', title='Anno')
    )

    # Crea l'area di riempimento
    fill_area = base.mark_area(opacity=0.2, color='gray').encode(
      y=alt.Y('y1:Q', scale=alt.Scale(domain=y_domain), title='Valore'),
      y2=alt.Y2('y2:Q')
    ).transform_calculate(
      y1='-5',
      y2='4'
    )

    # Crea il grafico a barre
    bars = base.mark_bar().encode(
      y=alt.Y('Valore:Q', scale=alt.Scale(domain=y_domain)),
      color=alt.condition(
        alt.datum.Valore > 0,
        alt.value('blue'),
        alt.value('red')
      )
    )

    # Aggiungi le linee orizzontali
    zero_line = base.mark_rule(color='green').encode(y=alt.Y(datum=0))
    three_line = alt.Chart(pd.DataFrame({'y': [3]})).mark_rule(
      color='orange',
      strokeDash=[4, 4]  # Questa opzione rende la linea tratteggiata
    ).encode(y='y')

    # Combina tutti gli elementi
    final_chart = (fill_area + bars + zero_line + three_line).properties(
      width=600,
      height=400,
      title='Grafico a Barre 2000-2005 con Area di Riempimento'
    )

    # Mostra il grafico in Streamlit
    st.altair_chart(final_chart, use_container_width=True)

    # End of the month's analysis
    st.divider()

  NomiMesi2 = ["01-Jan", "02-Feb", "03-Mar", "04-Apr", "05-May", "06-JuN", "07-JuL", "08-Aug", "09-Sept", "10-Oct", "11-Nov",
               "12-Dec"]  # Abbreviated month's name
  rad = st.radio(
    "### Type of table:",
    ["No more data", "Extended"]
  )

  if rad == "Extended":
    st.title("⚠️OVERALL AVERAGE RETURN MONTHS:")
    st.bar_chart(dict(zip(np.array(NomiMesi2), np.array(MesiComplessivi))))
    plt.figure(figsize=(10, 5))
    color = [Color2("red", "yellow", "blue", i, 25, 75) for i in WRComplessivi]
    plt.barh(NomiMesi2, WRComplessivi, color=color)
    plt.axvline(25, color="red")
    plt.axvline(50, color="yellow")
    plt.axvline(75, color="blue")
    plt.legend(["Profitability at 25% or below", "Profitability from 25% to 75%", "Profitability at 75% or above"],
               loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title("Grafico dei mesi più profittevoli")
    plt.xlabel("Win rate")
    plt.ylabel("Mesi")
    st.pyplot(plt.gcf())
    plt.close()

if(ticker != ""):
  main()
