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
#1) Error handling SP500: deve identificare qual è la prima "data non corrotta" e dire all'utente che cosa sta succedendo
#2) Codice IN INGLESE!!!
#3) Formattazione colori overall average drawdown (i colori devono essere basati sulla media oscillazioni e sulla varianza)

# Url of yahoo!finance ticker's list
url = "https://finance.yahoo.com/lookup/"
NomiMesi1 = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
               "NOVEMBER", "DECEMBER"]  # Defining the names of the months

current_year = datetime.now().year # Current year

# Introduction for the user
st.write("# LET'S ANALYZE THE SEASONALITY OF AN ASSET 📊")
st.write("### You have just to set: when to start with the monitoration,when to end and which is the asset to see")
st.write("Please, note that it has been used the YAHOO! FINANCE API, so you have to select the ticker of the asset based on the yahoo!finance database")
st.write("You can check the name of the asset 🔍 you're searching at this [link](%s)" % url)

AnnoPartenz = st.number_input("Starting year 📅: ",min_value = 1850, max_value=current_year-1, step = 1)

AnnoFin = st.number_input("End year 📅: ", value = current_year, min_value = 1900, max_value=current_year, step = 1)

# First validation check
if AnnoFin <= AnnoPartenz:
  st.warning(
    "# ⚠️ ATTENTION!!!\n### The starting year (" + str(AnnoPartenz) + ") mustn't be higher than the end year (" + str(AnnoFin) + ").")
  st.write("### Please, select another ending date for the relevation.")
  sys.exit(1)

ticker = st.text_input("Insert the TICKER 📈: ", value="GOOG")

# Verify the ticker
try:
  asset = yf.Ticker(ticker)
  info = asset.info
  info.get('longName', 'N/A')
  if info and "error" in info:
      st.warning(f"# ⚠️ The asset {ticker} doesn't exist. ⚠️")
      st.write("### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
      sys.exit(1)
except Exception as e:
    st.warning(f"# ⚠️ Error with the asset {ticker}.")
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
      st.warning(f"# ⚠️ The asset {ticker} doesn't exist. ⚠️")
      st.write(
        "### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
      sys.exit(1)
  except Exception as e:
    # Se non ci sono dati disponibili, fornire un messaggio personalizzato
    st.warning(f"# ⚠️ The asset {ticker} doesn't exist. ⚠️")
    st.write("### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
    sys.exit(1)

  # Controls to do: there must be no invalid periods of time

  # 1)The starting year must be superior than the first date avaible in the database
  if year >= AnnoFine:
    st.warning("# ⚠️ ATTENTION!!!\n### You have to choose a data that is ABOVE ", year)
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

  # We start to create the list to keep in consideration
  WRComplessivi = []
  MesiComplessivi = []
  Months_to_consider = []
  NomiMesi2 = ["01-Jan", "02-Feb", "03-Mar", "04-Apr", "05-May", "06-JuN", "07-JuL", "08-Aug", "09-Sept", "10-Oct", "11-Nov",
              "12-Dec"]  # Abbreviated month's name

  # ------------------------------------------------------
  # ------------------------------------------------------
  # We are going to:
  #  1)Visualize the results of the 12 months of the year
  #  2)Create an array that contains the data to analyze how does the varius seasons of the year performs
  # ------------------------------------------------------
  # LET'S START WITH THE POINT 1!!!
  # ------------------------------------------------------
  # ------------------------------------------------------

  W = 600  # Chart
  H = 600  # Chart Height

  st.write("# LET'S SEE THE RESULTS 📈")
  Months = st.checkbox("Represent all months")

  first_representation_model = "Not longer"
  if (Months == False):
    if (first_representation_model == "Longer"):
      # Create a dictionary to store the state of each toggle
      if 'month_toggles' not in st.session_state:
        st.session_state.month_toggles = {month: False for month in NomiMesi1}

      # Use columns to organize the toggles
      cols = st.columns(3)  # You can adjust the number of columns as needed

      # Create toggles for each month
      for index, month in enumerate(NomiMesi1):
        with cols[index % 3]:  # This will distribute the toggles across the columns
          st.session_state.month_toggles[month] = st.toggle(month, st.session_state.month_toggles[month])
    else:
      options = st.multiselect(
        "# Select the months to consider",
        NomiMesi1
      )

  rad = st.radio("Overall months rappresentation:",
                 ["No more data",
                  "Extended"])

  def Represent(Mese, i, selections, db_selections):
    colori = []
    for Y in Mese:
      colori.append(Color("#FF0000", "#0000FF", Y, 0))

    # Defining a good title, to make everything more clear
    st.write("# ",number_emojis[i-1],"MONTHLY RETURNS of", asset_name, "on the month of: ", NomiMesi1[i - 1], "\n")
    st.write("# WIN RATE\t:", round(WinRate(Mese), 2), "%\n")
    st.write("# AVERAGE RETURN\t:", round(Media(Mese), 2), "%\n")

    DevStd = math.sqrt(sum((x - Media(Mese)) ** 2 for x in Mese) / len(Mese))
    st.write("### Standard deviation\t:", round(DevStd,2), "%")

    st.write("Better excursion:", round(max(Mese), 2), "%")
    st.write("Worst excursion:", round(min(Mese), 2), "%")

    options = ["Image", "Complete", "Simple"]
    key = f'select_{i+1}'
    selections[key] = st.selectbox("### Type of chart", options, key=key)

    # FIRST: THE CHART

    xsize = 10
    ysize = 10
    if selections[key] == "Simple":
      st.bar_chart(dict(zip(np.array(Annate), np.array(Mese))))
      plt.figure(figsize=(xsize, ysize))
      plt.bar(np.array(Annate), np.array(Mese), color=np.array(colori))
      plt.axhline(0, color="green")

    elif selections[key] == "Image":
      fig, ax = plt.subplots(figsize=(xsize, ysize))  # Aumentato ulteriormente per assicurare spazio

      # Disegna il grafico a barre
      ax.bar(Annate, Mese, color=['blue' if x >= 0 else 'red' for x in Mese])

      # Aggiungi la linea della media
      ax.axhline(Media(Mese), color="red", linestyle='--', linewidth=2)
      ax.axhline(0, color="green")

      # Aggiungi le etichette degli assi
      ax.set_xlabel("Years")
      ax.set_ylabel("Returns")

      # Crea il patch per la deviazione standard
      band_patch = mpatches.Patch(color='gray', alpha=0.3, label=f"Average ± Standard Deviation ({round(DevStd, 2)}%)")

      # Aggiungi la banda della deviazione standard
      ax.fill_between(
        Annate,
        Media(Mese) + DevStd,
        Media(Mese) - DevStd,
        color='gray',
        alpha=0.3,
        hatch="X",
        edgecolor="gray",
        label=f"Average ± Standard Deviation ({DevStd}%)"
      )

      # Crea la legenda
      ax.legend(handles=[
        plt.Line2D([0], [0], color="red", lw=4, label="Negative Months"),
        plt.Line2D([0], [0], color="blue", lw=4, label="Positive Months"),
        plt.Line2D([0], [0], color="red", linestyle='--', lw=2, label="Average returns"),
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

    else:
      avacac = 2
      # Definisci gli array
      Assex = Annate1
      Assey = Mese

      Valore_Media = Media(Mese)

      # Crea un DataFrame
      df = pd.DataFrame({
        'Year': Assex,
        'Return': Assey
      })

      # Calcola il dominio dell'asse Y basato sui dati
      y_min = min(min(Assey), Valore_Media - DevStd)
      y_max = max(max(Assey), Valore_Media + DevStd)
      y_domain = [y_min - 1, y_max + 1]  # Aggiungiamo un po' di spazio

      # Crea il grafico base con Altair
      base = alt.Chart(df).encode(
        x=alt.X('Year:O', title='Years')
      )

      # Crea l'area di riempimento con tooltip personalizzato
      fill_area = base.mark_area(opacity=0.2, color='gray').encode(
        y=alt.Y('y1:Q', scale=alt.Scale(domain=y_domain), title='Return'),
        y2=alt.Y2('y2:Q'),
        tooltip=[
          alt.Tooltip('y1:Q', title='Media - Standard Deviation', format='.2f'),
          alt.Tooltip('y2:Q', title='Media + Standard Deviation', format='.2f'),
          alt.Tooltip('average_return:Q', title='Average Return', format='.2%')
        ]
      ).transform_calculate(
        y1=f"{Valore_Media - DevStd}",
        y2=f"{Valore_Media + DevStd}",
        average_return=f"{Valore_Media / 100}"
      )

      # Crea il grafico a barre
      bars = base.mark_bar().encode(
        y=alt.Y('Return:Q', scale=alt.Scale(domain=y_domain)),
        color=alt.condition(
          alt.datum.Return > 0,
          alt.value('blue'),
          alt.value('red')
        ),
        tooltip=[
          alt.Tooltip('Year:O', title='Year'),
          alt.Tooltip('return_percentage:Q', title='Return', format='.2%'),
          alt.Tooltip('average_return:Q', title='Average Return', format='.2%')
        ]
      ).transform_calculate(
        return_percentage="datum.Return/100",
        average_return=f"{Valore_Media / 100}"
      )

      # Aggiungi le linee orizzontali
      zero_line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='green', size=2).encode(
        y='y'
      )
      three_line = alt.Chart(pd.DataFrame({'y': [Valore_Media]})).mark_rule(
        color='orange',
        strokeDash=[4, 4],
        size=2
      ).encode(y='y')

      # Combina tutti gli elementi
      final_chart = (fill_area + bars + zero_line + three_line).properties(
        width=W,
        height=H,
        title='Interactive chart'
      )

      # Crea la legenda personalizzata
      legend_data = pd.DataFrame({
        'color': ['gray', 'blue', 'red', 'green', 'orange'],
        'Chart elements': ['Standard Dev.', 'Positive Return', 'Negative Return', 'Zero Line', 'Average Return']
      })

      legend = alt.Chart(legend_data).mark_rect().encode(
        y=alt.Y('Chart elements:N', axis=alt.Axis(orient='right')),
        color=alt.Color('color:N', scale=None)
      ).properties(
        width=150,
        title='Legend'
      )

      # Combina il grafico principale con la legenda
      combined_chart = alt.hconcat(final_chart, legend)

      # Mostra il grafico in Streamlit
      st.altair_chart(combined_chart, use_container_width=True)

    # SECOND: THE DATAFRAME
    options_DB = ["Graphical", "For CSV download"]
    db_key = f'db_select_{i + 1}'
    db_selections[db_key] = st.selectbox("### Type of database visualization", options_DB, key=db_key)

    if db_selections[db_key] == "For CSV download":
      # Pandas dataframe creation
      MeseDF = pd.DataFrame({
        "Year 📆": Annate,
        "Return 📈": Mese}
      )
      st.dataframe(MeseDF, hide_index=True)

    else:
      # Pandas dataframe creation
      table1 = pd.DataFrame({
        "Year": Annate,
        "Monthly return": Mese
      })

      # Tentativo di conversione della colonna "Year" in numeri
      table1['Year'] = pd.to_numeric(table1['Year'], errors='coerce')

      # Funzione per colorare le celle e aggiungere il contorno
      def style_monthly_return(val):
        color = 'red' if val < 0 else 'blue'
        return f'color: {color}; text-shadow: -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, 1px 1px 0 white; font-weight: bold;'

      # CSS per nascondere l'indice, impostare le larghezze delle colonne e stilizzare la tabella
      custom_css = """
              <style>
              thead tr th:first-child {display:none}
              tbody th {display:none}
              .col0 {width: 30% !important;}
              .col1 {width: 70% !important;}
              .dataframe {
                  width: 100% !important;
                  text-align: center;
              }
              .dataframe td, .dataframe th {
                  text-align: center !important;
                  vertical-align: middle !important;
              }
              .monthly-return-cell {
                  position: relative;
                  z-index: 1;
                  display: flex !important;
                  justify-content: center !important;
                  align-items: center !important;
                  height: 100%;
              }
              .monthly-return-cell::before {
                  content: "";
                  position: absolute;
                  top: 2px;
                  left: 2px;
                  right: 2px;
                  bottom: 2px;
                  background: rgba(255, 255, 255, 0.7);
                  z-index: -1;
                  border-radius: 4px;
              }
              </style>
          """

      # Inject CSS with Markdown
      st.markdown(custom_css, unsafe_allow_html=True)

      # Stile della tabella
      def style_table(styler):
        styler.format({'Year': '{:.0f}', 'Monthly return': '{:.2f}'})
        styler.applymap(style_monthly_return, subset=['Monthly return'])
        styler.bar(subset=['Monthly return'], align="mid", color=['#d65f5f', '#5fba7d'])
        styler.set_properties(**{'class': 'monthly-return-cell'}, subset=['Monthly return'])
        return styler

      # Visualizza la tabella
      st.write(table1.style.pipe(style_table).to_html(classes=['dataframe', 'col0', 'col1'], escape=False),
               unsafe_allow_html=True)

    # End of the month's analysis
    st.divider()

  for i in range(1, 13):
    if rad == "Extended":
      if (Months == True) or (NomiMesi1[i-1] in options):
        Mese = Mensilit(i, AnnoPartenza, AnnoFine)  # Si identifica la var di prezzo avvenuta
        # Arrays for later
        MesiComplessivi.append(round(Media(Mese), 2))  # Add to the array the value for the next chart
        WRComplessivi.append(round(WinRate(Mese), 2))  # Add to the array the value for the next chart
        Months_to_consider.append(NomiMesi2[i-1])

    selections = {}
    db_selections = {}
    if (Months == True) or (NomiMesi1[i-1] in options): #or (st.session_state.month_toggles[NomiMesi1[i-1]]):
      Represent(Mensilit(i, AnnoPartenza, AnnoFine), i, selections, db_selections)

  
  if rad == "Extended":
    st.title("⚠️OVERALL AVERAGE RETURN MONTHS:")
    st.bar_chart(dict(zip(np.array(Months_to_consider), np.array(MesiComplessivi))))
    plt.figure(figsize=(10, 5))
    color = [Color2("red", "yellow", "blue", i, 40, 60) for i in WRComplessivi]
    plt.barh(Months_to_consider, WRComplessivi, color=color)
    plt.axvline(25, color="red")
    plt.axvline(50, color="yellow")
    plt.axvline(75, color="blue")
    plt.legend(["Profitability at 40% or below", "Profitability from 40% to 60%", "Profitability at 60% or above"],
               loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title("Overall months's profits chart")
    plt.xlabel("Win rate")
    plt.ylabel("Months")
    st.pyplot(plt.gcf())
    plt.close()

# Var in punti dei mesi
def Mensilit(mese, startY, endY):
  array = []
  for i in range(startY, endY):
    if (mese != 12):  # Se è dicembre, il mese successivo è gennaio quindi si sta attenti
      strt = date(i, mese, 1)
      end = date(i, mese + 1, 1)
      dff = yf.download(ticker, start=strt, end=end, interval="1mo")
      dffc = pd.DataFrame(dff["Close"])
      dffo = pd.DataFrame(dff["Open"])
      resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
      result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
      array.append(result)
    else:
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

if(ticker != ""):
  main()
