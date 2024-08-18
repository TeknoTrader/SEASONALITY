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

# COLORI DA INSERIRE
# text, widget e label = bianco
# sidebar + text = #1A4054
# header = #880C14
# background = #649ABA
# Color pickers
sidebar_color = "#1A4054"
main_bg_color = "#649ABA"
text_color = "#1A4054"
widget_color = "#ffffff"
header_color = "#880C14"
#text_color = "#FFFFFF"
label_color = "#FFFFFF"

# DA MODIFICARE LA SIDEBAR

def WinRate(Arr):
    tot = 0
    for i in Arr:
        if (i >= 0):
            tot += 1
    if (tot == 0):
        return 0
    else:
        return (100 / len(Arr) * tot)

def Sortino_Ratio(returns, risk_free_rate=0, target_return=0):
    """
        Calcola il Sortino Ratio.

        Parameters:
        returns (array-like): Array o lista dei rendimenti del portafoglio o dell'investimento.
        risk_free_rate (float): Tasso di rendimento privo di rischio. Default è 0.
        target_return (float): Rendimento target o minimo accettabile. Default è 0.

        Returns:
        float: Il Sortino Ratio.
        """
    # Calcolo dell'excess return (rendimento in eccesso rispetto al tasso privo di rischio)
    excess_returns = np.array(returns) - risk_free_rate

    # Calcolo della downside deviation
    downside_deviation = np.sqrt(np.mean(np.minimum(0, excess_returns - target_return) ** 2))

    # Calcolo del Sortino Ratio
    if downside_deviation == 0:
        return np.nan  # Evita divisione per zero, restituisce NaN
    sortino_ratio = np.mean(excess_returns) / downside_deviation

    return sortino_ratio

def Treynor_Ratio(returns, market_returns, risk_free_rate=0):
    """
        Calcola il Treynor Ratio.

        Parameters:
        returns (array-like): Array o lista dei rendimenti del portafoglio o dell'investimento.
        market_returns (array-like): Array o lista dei rendimenti del mercato di riferimento.
        risk_free_rate (float): Tasso di rendimento privo di rischio. Default è 0.

        Returns:
        float: Il Treynor Ratio.
        """
    # Calcolo del rendimento medio del portafoglio e del mercato
    portfolio_return = np.mean(returns)
    market_return = np.mean(market_returns)

    # Calcolo del beta (coefficiente di regressione tra rendimenti del portafoglio e del mercato)
    covariance = np.cov(returns, market_returns)[0, 1]
    variance_market = np.var(market_returns)
    beta = covariance / variance_market

    # Calcolo del Treynor Ratio
    treynor_ratio = (portfolio_return - risk_free_rate) / beta

    return treynor_ratio

def Profit_Factor(trades):
    """
        Calcola il Profit Factor.

        Parameters:
        trades (array-like): Lista dei profitti e delle perdite per ogni operazione.

        Returns:
        float: Il Profit Factor.
        """
    # Separare le operazioni vincenti e perdenti
    profits = [trade for trade in trades if trade > 0]
    losses = [-trade for trade in trades if trade < 0]

    # Calcolare il totale dei profitti e delle perdite
    total_profits = sum(profits)
    total_losses = sum(losses)

    # Calcolare il Profit Factor
    if total_losses == 0:
        return float('inf')  # Evita divisione per zero, restituisce infinito
    profit_factor = total_profits / total_losses

    return profit_factor

def Volatility(returns):
    """
        Calcola la volatilità di una strategia di trading.

        Parameters:
        returns (array-like): Lista o array dei rendimenti della strategia.

        Returns:
        float: La volatilità (deviazione standard) dei rendimenti.
        """
    # Calcolo della volatilità
    volatility = np.std(returns, ddof=1)  # ddof=1 per calcolare la deviazione standard campionaria

    return volatility

def Max_Drawdown(Historycal_Drawdowns):
    return max(Historycal_Drawdowns)

def Omega_Ratio(returns, threshold):
    """
    Calcola l'Omega Ratio.

    Parameters:
    returns (array-like): Lista o array dei rendimenti della strategia.
    threshold (float): La soglia di rendimento minimo accettabile (MAR).

    Returns:
    float: L'Omega Ratio.
    """
    # Calcolo delle parti superiore e inferiore della formula dell'Omega Ratio
    positive_part = np.sum(np.maximum(returns - threshold, 0))
    negative_part = np.sum(np.maximum(threshold - returns, 0))

    if negative_part == 0:
        return float('inf')  # Evita divisione per zero, restituisce infinito

    # Calcolo dell'Omega Ratio
    omega_ratio = positive_part / negative_part

    return omega_ratio

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

# Url of yahoo!finance ticker's list
url = "https://finance.yahoo.com/lookup/"
NomiMesi1 = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER",
                 "NOVEMBER", "DECEMBER"]  # Defining the names of the months

current_year = datetime.now().year  # Current year

st.markdown(f"""
    <style>
    .stRadio label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stMultiSelect label, .stToggle label {{
        color: {label_color};
    }}
    </style>
    """, unsafe_allow_html=True)
def Text(text):
    st.write(f"<p style='color: {text_color};'>" + text + "</p>", unsafe_allow_html=True)
def Text2(text):
    st.markdown(f"<h2 style='color: {text_color};'>{text}</h2>", unsafe_allow_html=True)
def Text3(text):
    st.markdown(f"<h1 style='color: {text_color};'>{text}</h1>", unsafe_allow_html=True)

def credits():
    # Some information about me
    st.sidebar.write("# Who built this web application?")
    st.sidebar.write(
        "My name is Nicola Chimenti.\nI'm currently pursuing a degree in \"Digital Economics\" and I program trading sotwares for traders who want to automatize their strategies.")
    st.sidebar.image(
        "https://i.postimg.cc/7LynpkrL/Whats-App-Image-2024-07-27-at-16-36-44.jpg")  # caption="My name is Nicola Chimenti.\nI'm currently pursuing a degree in \"Digital Economics\" and I love finance, programming and Data Science" , use_column_width=True)
    st.sidebar.write("\n# CONTACT ME")
    st.sidebar.write(
        "### ◾ [LinkedIn](https://www.linkedin.com/in/nicolachimenti?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)")
    st.sidebar.write("### ◾ Email: nicola.chimenti.work@gmail.com")
    st.sidebar.write("\n# RESOURCES")
    st.sidebar.write("◾ [GitHub Profile](https://github.com/TeknoTrader)")
    st.sidebar.write("◾ [MQL5 Profile](https://www.mql5.com/it/users/teknotrader) with reviews")
    st.sidebar.write(
        "◾ [MT4 free softwares](https://www.mql5.com/it/users/teknotrader/seller#!category=2) for trading")
    st.sidebar.write("\n### Are you interested in the source code? 🧾")
    st.sidebar.write("Visit the [GitHub repository](https://github.com/TeknoTrader/OrganizationTools)")

def main_page():

    # MANCA SOLO:
    # 1) Error handling SP500: deve identificare qual è la prima "data non corrotta" e dire all'utente che cosa sta succedendo
    # 2) Codice IN INGLESE!!!
    # 3) Formattazione colori overall average drawdown (i colori devono essere basati sulla media oscillazioni e sulla varianza)

    # Introduction for the user
    Text3("LET'S ANALYZE THE SEASONALITY OF AN ASSET 📊")
    Text2("You have just to set: when to start with the monitoration,when to end and which is the asset to see")
    Text(
        "Please, note that it has been used the YAHOO! FINANCE API, so you have to select the ticker of the asset based on the yahoo!finance database")
    st.markdown(f"""
    <style>
    .colored-text {{
      color: {text_color};
    }}
    .colored-text a {{
      color: {text_color};
    }}
    </style>
    <p class="colored-text">You can check the name of the asset you're searching at this <a href="{url}">link</a>.</p>
    """, unsafe_allow_html=True)

    AnnoPartenz = st.number_input("Starting year 📅: ", min_value=1850, max_value=current_year - 1, step=1)

    AnnoFin = st.number_input("End year 📅: ", value=current_year, min_value=1900, max_value=current_year, step=1)

    # First validation check
    if AnnoFin <= AnnoPartenz:
        st.warning(
            "# ⚠️ ATTENTION!!!\n### The starting year (" + str(
                AnnoPartenz) + ") mustn't be higher than the end year (" + str(AnnoFin) + ").")
        st.write("### Please, select another ending date for the relevation.")
        sys.exit(1)

    ticker = st.text_input("Insert the TICKER 📈: ", value="GOOG")

    # Verify the ticker
    try:
        asset = yf.Ticker(ticker)
        info = asset.info
        info.get('longName', 'N/A')
        if info and "error" in info:
            st.warning(f"# ⚠️ The asset {ticker} doesn't exist.")
            st.write(
                "### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
            sys.exit(1)
    except Exception as e:
        st.warning(f"# ⚠️ Error with the asset {ticker}.")
        st.write(
            "### Probably you didn't insert the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)\n")
        st.write(f"Fing here more details: \n{str(e)}")
        sys.exit(1)

    asset = yf.Ticker(ticker)
    info = asset.info
    asset_name = info.get('longName', 'N/A')

    def main():
        AnnoFine = int(AnnoFin)
        end = date(AnnoFine, 1, 1)
        Text(f"\nEnd of the relevation: {end}")
        year = 0
        try:
            data = yf.download(ticker)
            if not data.empty:
                # Find the first data avaible, to avoid errors
                first_date = data.index[0]
                Text(f"Data of  {ticker} avaible from: {first_date.date()}")
                year = int(first_date.strftime('%Y'))
            else:
                st.warning(f"# ⚠️ The asset {ticker} doesn't exist.")
                st.write(
                    "### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
                sys.exit(1)
        except Exception as e:
            # Se non ci sono dati disponibili, fornire un messaggio personalizzato
            st.warning(f"# ⚠️ The asset {ticker} doesn't exist.")
            st.write(
                "### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
            sys.exit(1)

        # Controls to do: there must be no invalid periods of time

        # 1)The starting year must be superior than the first date avaible in the database
        if year >= AnnoFine:
            st.warning("# ⚠️ ATTENTION!!!\n### You have to choose a data that is ABOVE ", year)
            sys.exit(1)

        end = date(AnnoFine, 1, 1)
        Text(f"\nEnd year at: {end}")

        if year < AnnoPartenz:
            AnnoPartenza = AnnoPartenz
        else:
            AnnoPartenza = year + 1

        # Inizialization
        Annate1 = list(range(AnnoPartenza, AnnoFine))
        NomiMesi = list(range(1, 13))
        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", "1️⃣1️⃣",
                         "1️⃣2️⃣"]  # There is no unicode for 2 decimals numbers

        Annate = []  # Conversion of Annate1 's elements in string type
        for i in Annate1:
            Annate.append(str(i))

        inizio = date(AnnoPartenza, 1, 1)
        # Now we download the serious data
        Text(f"\nStarting calculations from: {inizio}")

        df = yf.download(ticker, start=inizio, end=end, interval="1mo")

        df = pd.DataFrame(df["Open"])  # Riduciamo l'array alle sole aperture

        array = []

        # We start to create the list to keep in consideration
        WRComplessivi = []
        MesiComplessivi = []
        Months_to_consider = []
        NomiMesi2 = ["01-Jan", "02-Feb", "03-Mar", "04-Apr", "05-May", "06-JuN", "07-JuL", "08-Aug", "09-Sept",
                     "10-Oct",
                     "11-Nov",
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

        W = 400  # Chart
        H = 400  # Chart Height

        Text3("LET'S SEE THE RESULTS 📈")
        Months = st.radio("Output selection:", ("Choose manually the months", "Represent every month"))#st.toggle("Represent all months")

        first_representation_model = "Not longer"
        if (Months == "Choose manually the months"): #== False):
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
        else:
            options = NomiMesi1

        # Questo dovrebbe essere fuori dalla funzione Represent, all'inizio del tuo script
        if 'update_button' not in st.session_state:
            st.session_state.update_button = False

        # Questo pulsante dovrebbe essere posizionato una sola volta, prima del ciclo che chiama Represent
        if st.button("Update Visualization"):
            st.session_state.update_button = not st.session_state.update_button

        def Represent(Mese, i, selections, db_selections):
            # Se il pulsante è stato premuto, aggiorna i dati
            if st.session_state.update_button:
                colori = []
                for Y in Mese:
                    colori.append(Color("#FF0000", "#0000FF", Y, 0))

                # Defining a good title, to make everything more clear
                Text3(f" {number_emojis[i - 1]} MONTHLY RETURNS of {asset_name} on the month of: {NomiMesi1[i - 1]} \n")
                Text3(f"WIN RATE: {str(round(WinRate(Mese), 2))}%\n")
                Text3(f"AVERAGE RETURN: {str(round(np.mean(Mese), 2))} %\n")

                DevStd = math.sqrt(sum((x - np.mean(Mese)) ** 2 for x in Mese) / len(Mese))
                Text2(f"Standard deviation: {str(round(DevStd, 2))}%")

                Text(f"Better excursion: {round(max(Mese), 2)}%")
                Text(f"Worst excursion: {round(min(Mese), 2)} %")

                Graphical_options = ["Image", "Interactive"]
                key = f'select_{i + 1}'
                selections[key] = st.selectbox("### Type of chart", Graphical_options, key=key)

                # FIRST: THE CHART

                xsize = 10
                ysize = 10

                if selections[key] == "Image":
                    fig, ax = plt.subplots(figsize=(xsize, ysize))

                    # Disegna il grafico a barre
                    ax.bar(Annate, Mese, color=['blue' if x >= 0 else 'red' for x in Mese])

                    # Aggiungi la linea della media
                    ax.axhline(np.mean(Mese), color="red", linestyle='--', linewidth=2)
                    ax.axhline(0, color="green")

                    # Aggiungi le etichette degli assi
                    ax.set_xlabel("Years")
                    ax.set_ylabel("Returns")

                    # Crea il patch per la deviazione standard
                    band_patch = mpatches.Patch(color='gray', alpha=0.3,
                                                label=f"Average ± Standard Deviation ({round(DevStd, 2)}%)")

                    # Aggiungi la banda della deviazione standard
                    ax.fill_between(
                        Annate,
                        np.mean(Mese) + DevStd,
                        np.mean(Mese) - DevStd,
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
                        plt.Line2D([0], [0], color="red", linestyle='--', lw=2,
                                   label=str("Average returns (" + str(round(np.mean(Mese), 2)) + "%)")), band_patch],
                        loc='upper right'
                    )

                    # Ruota le etichette dell'asse x per una migliore leggibilità
                    plt.xticks(rotation=45, ha='right')

                    # Adatta il layout
                    plt.tight_layout()

                    # Mostra il grafico in Streamlit
                    st.pyplot(fig)

                    # Chiudi la figura per liberare memoria
                    plt.close(fig)

                else:  # if the chart is "Interactive"
                    avacac = 2
                    # Definisci gli array
                    Assex = Annate1
                    Assey = Mese

                    Valore_Media = np.mean(Mese)

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
                        'Chart elements': ['Standard Dev.', 'Positive Return', 'Negative Return', 'Zero Line',
                                           'Average Return']
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
                    # First of all let's define the format of the DB output
                    def format_value(val):
                        return f"{'+' if val > 0 else ''}{val:.2f}%"

                    # DB creation
                    MeseDF = pd.DataFrame({
                        "Year 📆": Annate,
                        "Lows 📉": [format_value(x) for x in Low(i, AnnoPartenza, AnnoFine)],
                        "Return 📊": [format_value(x) for x in Mese],
                        "Highs 📈": [format_value(x) for x in High(i, AnnoPartenza, AnnoFine)]
                    })
                    st.dataframe(MeseDF, hide_index=True)

                else:
                    Lows = Low(i, AnnoPartenza, AnnoFine)
                    Highs = High(i, AnnoPartenza, AnnoFine)

                    # Variabili booleane per controllare la visualizzazione delle colonne opzionali
                    mostra_highs = True
                    mostra_lows = True

                    # Funzione per colorare le celle e aggiungere il contorno
                    def style_numeric_column(val):
                        color = 'red' if val < 0 else 'blue'
                        return f'color: {color}; text-shadow: -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, 1px 1px 0 white; font-weight: bold;'

                    # Pandas dataframe creation
                    table1 = pd.DataFrame({
                        "Year": Annate,
                        "Monthly return": Mese,
                    })

                    # Aggiungi le colonne opzionali e riordina
                    if mostra_lows:
                        table1.insert(1, "Lows", Lows)  # Inserisce "Lows" come seconda colonna
                    if mostra_highs:
                        table1.insert(3, "Highs", Highs)

                    # Tentativo di conversione della colonna "Year" in numeri
                    table1['Year'] = pd.to_numeric(table1['Year'], errors='coerce')

                    # Funzione per aggiungere il segno + ai numeri positivi e formattare come percentuale
                    def format_percentage(val):
                        return f"{'+' if val > 0 else ''}{val:.2f}%"

                    # Stile della tabella
                    def style_table(styler):
                        styler.format({
                            'Lows': format_percentage,
                            'Monthly return': format_percentage,
                            'Highs': format_percentage,
                        })

                        numeric_columns = ['Lows', 'Monthly return', 'Highs']

                        for col in numeric_columns:
                            styler.applymap(style_numeric_column, subset=[col])
                            styler.bar(subset=[col], align="mid", color=['#d65f5f', '#5fba7d'])
                            styler.set_properties(**{'class': 'numeric-cell'}, subset=[col])

                        return styler

                    # CSS personalizzato
                    custom_css = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        .col0 {width: 20% !important;}
                        .col1, .col2, .col3 {width: 26.67% !important;}
                        .dataframe {
                            width: 100% !important;
                            text-align: center;
                        }
                        .dataframe td, .dataframe th {
                            text-align: center !important;
                            vertical-align: middle !important;
                        }
                        .numeric-cell {
                            position: relative;
                            z-index: 1;
                            display: flex !important;
                            justify-content: center !important;
                            align-items: center !important;
                            height: 100%;
                        }
                        .numeric-cell::before {
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

                    # Visualizza la tabella con lo stile applicato
                    st.write(
                        table1.style.pipe(style_table).to_html(classes=['dataframe', 'col0', 'col1', 'col2', 'col3'],
                                                               escape=False),
                        unsafe_allow_html=True)

                # End of the month's analysis
                st.divider()

        # Il resto del codice rimane invariato
        for i in range(1, 13):
            selections = {}
            db_selections = {}
            if (Months == True) or (NomiMesi1[i - 1] in options):
                Represent(Mensilit(i, AnnoPartenza, AnnoFine), i, selections, db_selections)

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

    def High(mese, startY, endY):
        array = []
        for i in range(startY, endY):
            if (mese != 12):  # Se è dicembre, il mese successivo è gennaio quindi si sta attenti
                strt = date(i, mese, 1)
                end = date(i, mese + 1, 1)
                dff = yf.download(ticker, start=strt, end=end, interval="1mo")
                dffc = pd.DataFrame(dff["High"])
                dffo = pd.DataFrame(dff["Open"])
                resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
                result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
                array.append(result)
            else:
                strt = date(i, mese, 1)
                end = date(i + 1, 1, 1)
                dff = yf.download(ticker, start=strt, end=end, interval="1mo")
                dffc = pd.DataFrame(dff["High"])
                dffo = pd.DataFrame(dff["Open"])
                resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
                result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
                array.append(result)
        return array

    def Low(mese, startY, endY):
        array = []
        for i in range(startY, endY):
            if (mese != 12):  # Se è dicembre, il mese successivo è gennaio quindi si sta attenti
                strt = date(i, mese, 1)
                end = date(i, mese + 1, 1)
                dff = yf.download(ticker, start=strt, end=end, interval="1mo")
                dffc = pd.DataFrame(dff["Low"])
                dffo = pd.DataFrame(dff["Open"])
                resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
                result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
                array.append(result)
            else:
                strt = date(i, mese, 1)
                end = date(i + 1, 1, 1)
                dff = yf.download(ticker, start=strt, end=end, interval="1mo")
                dffc = pd.DataFrame(dff["Low"])
                dffo = pd.DataFrame(dff["Open"])
                resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
                result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
                array.append(result)
        return array
    if (ticker != ""):
        main()

#Drawdown for BUY
def drawdown(min, close):
    act = 0
    drawdowns = []

    for m, c in zip(min, close):
        if (act >= 0):
            drawdowns.append(m)
        else:
            drawdowns.append(act + m)
        act += c
        if (act > 0):
            act = 0
        else:
            act = act
    return drawdowns

def Simple_strategy():
    AnnoPartenz = st.number_input("Starting year 📅: ", min_value=1850, max_value=current_year - 1, step=1)

    AnnoFin = st.number_input("End year 📅: ", value=current_year, min_value=1900, max_value=current_year, step=1)

    # First validation check
    if AnnoFin <= AnnoPartenz:
        st.warning(
            "# ⚠️ ATTENTION!!!\n### The starting year (" + str(
                AnnoPartenz) + ") mustn't be higher than the end year (" + str(AnnoFin) + ").")
        st.write("### Please, select another ending date for the relevation.")
        sys.exit(1)

    ticker = st.text_input("Insert the TICKER 📈: ", value="GOOG")

    # Verify the ticker
    try:
        asset = yf.Ticker(ticker)
        info = asset.info
        info.get('longName', 'N/A')
        if info and "error" in info:
            st.warning(f"# ⚠️ The asset {ticker} doesn't exist.")
            st.write(
                "### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
            sys.exit(1)
    except Exception as e:
        st.warning(f"# ⚠️ Error with the asset {ticker}.")
        st.write(
            "### Probably you didn't insert the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)\n")
        st.write(f"Fing here more details: \n{str(e)}")
        sys.exit(1)

    asset = yf.Ticker(ticker)
    info = asset.info
    asset_name = info.get('longName', 'N/A')

    AnnoFine = int(AnnoFin)
    end = date(AnnoFine, 1, 1)
    Text(f"\nEnd of the relevation: {end}")
    year = 0
    try:
        data = yf.download(ticker)
        if not data.empty:
            # Find the first data avaible, to avoid errors
            first_date = data.index[0]
            Text(f"Data of  {ticker} avaible from: {first_date.date()}")
            year = int(first_date.strftime('%Y'))
        else:
            st.warning(f"# ⚠️ The asset {ticker} doesn't exist.")
            st.write(
                "### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
            sys.exit(1)
    except Exception as e:
        # Se non ci sono dati disponibili, fornire un messaggio personalizzato
        st.warning(f"# ⚠️ The asset {ticker} doesn't exist.")
        st.write(
            "### Maybe you didn't select the right ticker.\n### You can find here the [Yahoo finance ticker's list](url)")
        sys.exit(1)

    # Controls to do: there must be no invalid periods of time

    # 1)The starting year must be superior than the first date avaible in the database
    if year >= AnnoFine:
        st.warning("# ⚠️ ATTENTION!!!\n### You have to choose a data that is ABOVE ", year)
        sys.exit(1)

    end = date(AnnoFine, 1, 1)
    Text(f"\nEnd year at: {end}")

    if year < AnnoPartenz:
        AnnoPartenza = AnnoPartenz
    else:
        AnnoPartenza = year + 1

    # Inizialization
    Annate1 = list(range(AnnoPartenza, AnnoFine))
    NomiMesi = list(range(1, 13))
    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", "1️⃣1️⃣",
                     "1️⃣2️⃣"]  # There is no unicode for 2 decimals numbers

    Annate = []  # Conversion of Annate1 's elements in string type
    for i in Annate1:
        Annate.append(str(i))

    inizio = date(AnnoPartenza, 1, 1)
    # Now we download the serious data
    Text(f"\nStarting calculations from: {inizio}")

    df = yf.download(ticker, start=inizio, end=end, interval="1mo")

    df = pd.DataFrame(df["Open"])  # Riduciamo l'array alle sole aperture

    array = []

    # We start to create the list to keep in consideration
    WRComplessivi = []
    MesiComplessivi = []
    Months_to_consider = []
    trades = []
    Sortin = []
    DD = []
    MaxDD = []
    NomiMesi2 = ["01-Jan", "02-Feb", "03-Mar", "04-Apr", "05-May", "06-JuN", "07-JuL", "08-Aug", "09-Sept",
                 "10-Oct",
                 "11-Nov",
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

    W = 400  # Chart
    H = 400  # Chart Height

    Text3("LET'S SEE THE RESULTS 📈")
    Months = st.radio("Output selection:",
                      ("Choose manually the months", "Represent every month"))  # st.toggle("Represent all months")

    first_representation_model = "Not longer"
    if (Months == "Choose manually the months"):  # == False):
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
    else:
        options = NomiMesi1

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

    def High(mese, startY, endY):
        array = []
        for i in range(startY, endY):
            if (mese != 12):  # Se è dicembre, il mese successivo è gennaio quindi si sta attenti
                strt = date(i, mese, 1)
                end = date(i, mese + 1, 1)
                dff = yf.download(ticker, start=strt, end=end, interval="1mo")
                dffc = pd.DataFrame(dff["High"])
                dffo = pd.DataFrame(dff["Open"])
                resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
                result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
                array.append(result)
            else:
                strt = date(i, mese, 1)
                end = date(i + 1, 1, 1)
                dff = yf.download(ticker, start=strt, end=end, interval="1mo")
                dffc = pd.DataFrame(dff["High"])
                dffo = pd.DataFrame(dff["Open"])
                resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
                result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
                array.append(result)
        return array

    def Low(mese, startY, endY):
        array = []
        for i in range(startY, endY):
            if (mese != 12):  # Se è dicembre, il mese successivo è gennaio quindi si sta attenti
                strt = date(i, mese, 1)
                end = date(i, mese + 1, 1)
                dff = yf.download(ticker, start=strt, end=end, interval="1mo")
                dffc = pd.DataFrame(dff["Low"])
                dffo = pd.DataFrame(dff["Open"])
                resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
                result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
                array.append(result)
            else:
                strt = date(i, mese, 1)
                end = date(i + 1, 1, 1)
                dff = yf.download(ticker, start=strt, end=end, interval="1mo")
                dffc = pd.DataFrame(dff["Low"])
                dffo = pd.DataFrame(dff["Open"])
                resultAbs = dffc.iat[0, 0] - dffo.iat[0, 0]  # Nominal return
                result = resultAbs * 100 / dffo.iat[0, 0]  # In percentage
                array.append(result)
        return array

    if 'data_calculated' not in st.session_state:
        st.session_state.data_calculated = False
    if 'MesiComplessivi' not in st.session_state:
        st.session_state.MesiComplessivi = []
    if 'WRComplessivi' not in st.session_state:
        st.session_state.WRComplessivi = []
    if 'Months_to_consider' not in st.session_state:
        st.session_state.Months_to_consider = []
    if 'Trades' not in st.session_state:
        st.session_state.Trades = []
    if 'Negative' not in st.session_state:
        st.session_state.Negative = []
    if 'Positive' not in st.session_state:
        st.session_state.Positive = []
    if 'Sortin' not in st.session_state:
        st.session_state.Sortin = []
    if 'MaxDD' not in st.session_state:
        st.session_state.MaxDD = []
    if 'DD' not in st.session_state:
        st.session_state.DD = []

    if st.button('Ready to go!'):
        st.session_state.MesiComplessivi = []
        st.session_state.WRComplessivi = []
        st.session_state.Months_to_consider = []
        st.session_state.Trades = []
        st.session_state.Sortin = []
        st.session_state.MaxDD = []
        st.session_state.DD = []
        st.session_state.Negative = []
        st.session_state.Positive = []

        for i in range(1, 13):
            if (Months == True) or (NomiMesi1[i - 1] in options):
                Mese = Mensilit(i, AnnoPartenza, AnnoFine)
                st.session_state.MesiComplessivi.append(round(np.mean(Mese), 2))
                st.session_state.WRComplessivi.append(round(WinRate(Mese), 2))
                st.session_state.Months_to_consider.append(NomiMesi2[i - 1])
                drawdowns = drawdown(Low(i, AnnoPartenza, AnnoFine), Mese)
                st.session_state.DD.append(drawdowns)
                st.session_state.Trades.append(round(Profit_Factor(Mese), 2))
                st.session_state.Sortin.append(round(Sortino_Ratio(Mese), 2))
                st.session_state.MaxDD.append(round(min(drawdowns), 2))
                st.session_state.Positive.append([High(i, AnnoPartenza, AnnoFine)])
                st.session_state.Negative.append([Low(i, AnnoPartenza, AnnoFine)])

        st.session_state.data_calculated = True

    # DATABASE
    representation_database = st.selectbox("Database Representation Method: ",
                                           ("User Friendly", "For CSV download"))

    if representation_database == "For CSV download":
        def format_value(val):
            return f"{'+' if val > 0 else ''}{val:.2f}%"

        Results = pd.DataFrame({
            "Month": st.session_state.Months_to_consider,
            "Average Win Rate": [format_value(x) for x in st.session_state.WRComplessivi],
            "Average Monthly Return": [format_value(x) for x in st.session_state.MesiComplessivi],
            "Max Drawdown": [x for x in st.session_state.MaxDD],
            "Profit Factor": [x for x in st.session_state.Trades],
            "Sortino Ratio": [x for x in st.session_state.Sortin]
        })
        st.dataframe(Results, hide_index=True)
    else:

        def format_value(val, include_sign=True, include_percent=True):
            if isinstance(val, str):
                return val
            sign = '+' if val > 0 and include_sign else ''
            percent = '%' if include_percent else ''
            return f"{sign}{val:.2f}{percent}"

        def style_cell(val, color):
            return f'color: {color}; font-weight: bold; text-shadow: -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, 1px 1px 0 white;'

        def color_win_rate(val):
            val = float(val.strip('%').strip('+'))
            return style_cell(val, 'red' if val < 50 else 'blue')

        def color_monthly_return(val):
            val = float(val.strip('%').strip('+'))
            return style_cell(val, 'red' if val < 0 else 'blue')

        def color_max_drawdown(val):
            val = float(val.strip('%').strip('+'))
            return style_cell(val, color)

        def color_profit_factor(val):
            val = float(val)
            return style_cell(val, 'red' if val < 1 else 'blue')

        # Pandas dataframe creation
        table1 = pd.DataFrame({
            "Month": st.session_state.Months_to_consider,
            "Average Win Rate": [format_value(x) for x in st.session_state.WRComplessivi],
            "Average Monthly Return": [format_value(x) for x in st.session_state.MesiComplessivi],
            "Max Drawdown": [format_value(x) for x in st.session_state.MaxDD],
            "Profit Factor": [format_value(x, include_percent=False) for x in st.session_state.Trades],
            "Sortino Ratio": [format_value(x, include_percent=False) for x in st.session_state.Sortin]
        })

        # Calculate mean and standard deviation for Max Drawdown
        max_drawdown_values = [float(x.strip('%').strip('+')) for x in table1["Max Drawdown"]]

        # Other representation "simpler"
        mean_drawdown = np.mean(max_drawdown_values)
        std_drawdown = np.std(max_drawdown_values)

        def color_max_drawdown(val):
            val = float(val.strip('%').strip('+'))
            if val < mean_drawdown - std_drawdown:
                color = 'red'
            elif val > mean_drawdown + std_drawdown:
                color = 'blue'
            else:
                color = 'black'
            return style_cell(val, color)

        # Apply styles
        styled_table = table1.style.applymap(color_win_rate, subset=['Average Win Rate']) \
            .applymap(color_monthly_return, subset=['Average Monthly Return']) \
            .applymap(color_max_drawdown, subset=['Max Drawdown']) \
            .applymap(color_profit_factor, subset=['Profit Factor', 'Sortino Ratio']) \
            .applymap(lambda x: style_cell(x, 'black'), subset=['Month'])

        # Display the styled table
        st.write(styled_table.to_html(escape=False), unsafe_allow_html=True)

    # CHARTS
    if st.session_state.data_calculated:
        rep = st.selectbox("Representation method: ", ("Image", "Interactive"))

        if rep == "Image":
            st.write("⚠️OVERALL AVERAGE RETURN MONTHS:")
            data = dict(zip(np.array(st.session_state.Months_to_consider), np.array(st.session_state.MesiComplessivi)))
            df = pd.DataFrame(list(data.items()), columns=['Months', 'Returns'])

            mean_value = df['Returns'].mean()

            fig, ax = plt.subplots(figsize=(12, 6))

            colors = ['red' if x < 0 else 'blue' for x in df['Returns']]
            bars = ax.bar(df['Months'], df['Returns'], color=colors)

            ax.axhline(y=mean_value, color='green', linestyle='--', label='Mean')
            ax.axhline(y=0, color='green', linewidth=0.8, label='Zero line')

            ax.set_xlabel('Months of the year')
            ax.set_ylabel('Returns')

            ax.bar(0, 0, color='blue', label='Average Returns are Positive')
            ax.bar(0, 0, color='red', label='Average Returns are Negative')

            ax.legend()

            plt.title('Average Monthly Returns')

            st.pyplot(fig)

            plt.figure(figsize=(10, 5))
            color = [Color2("red", "yellow", "blue", i, 40, 60) for i in st.session_state.WRComplessivi]
            plt.barh(st.session_state.Months_to_consider, st.session_state.WRComplessivi, color=color)
            plt.axvline(40, color="red")
            plt.axvline(50, color="yellow")
            plt.axvline(60, color="blue")
            plt.legend(
                ["Win Rate <= 40%", "40% <= Win Rate <= 60%", "Win Rate >= 60%"],
                loc='center left', bbox_to_anchor=(1, 0.5))
            plt.title("Overall months's WIN RATE chart")
            plt.xlabel("Win rate")
            plt.ylabel("Months")
            st.pyplot(plt.gcf())
            plt.close()

        else:
            data = dict(zip(np.array(st.session_state.Months_to_consider), np.array(st.session_state.MesiComplessivi)))
            df = pd.DataFrame(list(data.items()), columns=['Months', 'Returns'])

            if df['Returns'].max() > 1 or df['Returns'].min() < -1:
                df['Returns'] = df['Returns'] / 100

            mean_value = df['Returns'].mean()
            std_dev = df['Returns'].std()

            W = 400
            H = 400

            base = alt.Chart(df).encode(
                x=alt.X('Months:O', title='Months of the year')
            )

            fill_area = base.mark_area(opacity=0.2, color='gray').encode(
                y=alt.Y('y1:Q', title='Returns', axis=alt.Axis(format='%')),
                y2=alt.Y2('y2:Q'),
                tooltip=[
                    alt.Tooltip('y1:Q', title='Average - Standard Deviation', format='.2%'),
                    alt.Tooltip('y2:Q', title='Average + Standard Deviation', format='.2%'),
                    alt.Tooltip('mean:Q', title='Average Return', format='.2%')
                ]
            ).transform_calculate(
                y1=f"{mean_value - std_dev}",
                y2=f"{mean_value + std_dev}",
                mean=f"{mean_value}"
            )

            bars = base.mark_bar().encode(
                y=alt.Y('Returns:Q', axis=alt.Axis(format='%')),
                color=alt.condition(
                    alt.datum.Returns > 0,
                    alt.value('blue'),
                    alt.value('red')
                ),
                tooltip=[
                    alt.Tooltip('Months:O', title='Month'),
                    alt.Tooltip('Returns:Q', title='Return', format='.2%'),
                    alt.Tooltip('mean:Q', title='Average Return', format='.2%')
                ]
            ).transform_calculate(
                mean=f"{mean_value}"
            )

            zero_line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='green', size=2).encode(y='y')
            mean_line = alt.Chart(pd.DataFrame({'y': [mean_value]})).mark_rule(
                color='orange',
                strokeDash=[4, 4],
                size=2
            ).encode(y='y')

            final_chart = (fill_area + bars + zero_line + mean_line).properties(
                width=W,
                height=H,
                title='Average Monthly Returns'
            )

            legend_data = pd.DataFrame({
                'color': ['gray', 'blue', 'red', 'green', 'orange'],
                'Chart elements': ['Standard Dev.', 'Positive Return', 'Negative Return', 'Zero Line',
                                   'Average Return']
            })

            legend = alt.Chart(legend_data).mark_rect().encode(
                y=alt.Y('Chart elements:N', axis=alt.Axis(orient='right')),
                color=alt.Color('color:N', scale=None)
            ).properties(
                width=150,
                title='Legend'
            )

            combined_chart = alt.hconcat(final_chart, legend)

            st.altair_chart(combined_chart, use_container_width=True)

            # SECOND CHART
            df = pd.DataFrame({
                'Months': st.session_state.Months_to_consider,
                'WinRate': [wr / 100 for wr in st.session_state.WRComplessivi]
            })

            df['MonthOrder'] = range(len(df))

            def get_color(wr):
                if wr <= 0.4:
                    return 'red'
                elif wr <= 0.6:
                    return 'yellow'
                else:
                    return 'blue'

            df['Color'] = df['WinRate'].apply(get_color)

            base = alt.Chart(df).encode(
                y=alt.Y('Months:N', sort=alt.EncodingSortField(field='MonthOrder', order='ascending'),
                        title='Months'),
                x=alt.X('WinRate:Q', title='Win rate', axis=alt.Axis(format='%'))
            )

            bars = base.mark_bar().encode(
                color=alt.Color('Color:N', scale=None),
                tooltip=[
                    alt.Tooltip('Months:N', title='Month'),
                    alt.Tooltip('WinRate:Q', title='Win Rate', format='.2%')
                ]
            )

            line_40 = alt.Chart(pd.DataFrame({'x': [0.4]})).mark_rule(color='red').encode(x='x')
            line_50 = alt.Chart(pd.DataFrame({'x': [0.5]})).mark_rule(color='yellow').encode(x='x')
            line_60 = alt.Chart(pd.DataFrame({'x': [0.6]})).mark_rule(color='blue').encode(x='x')

            legend_data = pd.DataFrame({
                'color': ['red', 'yellow', 'blue'],
                'description': ['Win Rate <= 40%', '40% <= WR <= 60%',
                                'Win Rate >= 60%']
            })

            legend = alt.Chart(legend_data).mark_rect().encode(
                y=alt.Y('description:N', axis=alt.Axis(orient='right')),
                color=alt.Color('color:N', scale=None)
            ).properties(
                width=20,
                title='Legend'
            )

            chart = (bars + line_40 + line_50 + line_60).properties(
                width=400,
                height=400,
                title='Overall months\'s WIN RATE chart'
            )

            combined_chart = alt.hconcat(chart, legend)

            st.altair_chart(combined_chart, use_container_width=True)
    else:
        st.write("Please click 'Ready to go!' to calculate and display the data.")

def credits():
    Text3("Who built this web application?")
    Text2("I'm Nicola Chimenti and I love finance, programming and Data Science")
    Text2("My main goal is to break into a Quantitative Trading Firm")
    st.image("https://i.postimg.cc/7LynpkrL/Whats-App-Image-2024-07-27-at-16-36-44.jpg")  # caption="My name is Nicola Chimenti.\nI'm currently pursuing a degree in \"Digital Economics\" and I love finance, programming and Data Science" , use_column_width=True)
    Text2(
        "I'm currently pursuing a degree in \"Digital Economics\" and I program trading softwares (VAT Code: 02674000464) for traders who want to automatize their strategy or analyze certain data to find a better edge")
    st.write("\n# CONTACT ME")
    st.write(
        "### ◾ [LinkedIn](https://www.linkedin.com/in/nicolachimenti?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)")
    st.write("### ◾ Email: nicola.chimenti.work@gmail.com")
    st.write("\n# RESOURCES")
    st.write("◾ [GitHub Profile](https://github.com/TeknoTrader)")
    st.write("◾ [MQL5 Profile](https://www.mql5.com/it/users/teknotrader) with reviews")
    st.write("◾ [MT4 free softwares](https://www.mql5.com/it/users/teknotrader/seller#!category=2) for trading")
    st.write("\n### Are you interested in the source code? 🧾")
    st.write("Visit the [GitHub repository](https://github.com/TeknoTrader/OrganizationTools)")

def Home():
    Text3("Welcome to the \'Tekno Trader's Seasonality Application\'")
    Text2("Unlock the power of historical market analysis with the \'Tekno Trader's Seasonality Application\'. Whether you're a seasoned investor or just starting out, our web app provides the insights you need to make informed decisions in today's dynamic financial environment.")

    Text3("Analyze Market Behavior:")
    Text2("Dive deep into the historical performance of your chosen markets in specific months. With this web application, you can analyze how markets have behaved over specific time windows, identifying regularities and patterns. Curious if September is traditionally a tough month for the S&P 500? Our platform helps you uncover these insights, allowing you to predict market trends with greater accuracy.")

    Text3("Craft Winning Strategies:")
    Text2("Develop and test simple yet effective market entry and exit strategies. Choose a specific month to enter the market and another to exit, then evaluate the potential success of your strategy with a range of performance indicators. See how your strategy would have performed historically, and gain confidence in your trading decisions.")

    Text3("In-Sample and Out-of-Sample Analysis:")
    Text2("Measure the robustness of your strategy with our advanced in-sample and out-of-sample analysis tools. Understand not only how your strategy performs on historical data but also how it holds up in new, unseen data, helping you reduce the risk of overfitting and optimize your investment approach.")

    Text3("Why Choose MarketTrend Pro?")
    Text2("Comprehensive Data Access: Powered by the Yahoo Finance API, get accurate and up-to-date financial market data.")
    Text2("Customizable Analysis: Tailor your analysis to specific markets, time frames, and strategies.")
    Text2("User-Friendly Interface: Intuitive design that makes complex analysis accessible to all levels of investors.")
    Text3("Start exploring the markets like never before with this web app. Your strategic edge is just a few clicks away.")

pagine = ["Home", "Analysis", "Basic Strategy", "Credits"]

# Navigation menu
st.logo("https://i.postimg.cc/7LynpkrL/Whats-App-Image-2024-07-27-at-16-36-44.jpg")

def apply_custom_css(sidebar_color, main_bg_color, text_color, widget_color, header_color):
    custom_css = f"""
    <style>
    /* Colore della sidebar */
    [data-testid=stSidebar] {{
        background-color: {sidebar_color};
    }}

    /* Colore di sfondo principale */
    .stApp {{
        background-color: {main_bg_color};
    }}

    /* Colore del testo */
    .stApp {{
        color: {text_color};
    }}

    /* Colore dei widget */
    .stSelectbox, .stMultiSelect, .stSlider, .stDateInput, .stCheckbox, .stRadio, .stNumber, .stTextInput, .stTextArea {{
        accent-color: {widget_color};
    }}

    /* Colore del bordo dei widget */
    .stSelectbox [data-baseweb="select"], 
    .stMultiSelect [data-baseweb="select"], 
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border-color: {widget_color};
    }}

    /* Colore del testo dei widget */
    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {{
        color: {text_color};
    }}

    /* Colore di sfondo dei widget */
    .stSelectbox [data-baseweb="select"],
    .stMultiSelect [data-baseweb="select"],
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: {main_bg_color};
    }}

    /* Colore del bottone */
    .stButton > button {{
        color: {text_color};
        background-color: {widget_color};
        border-color: {widget_color};
    }}

    /* Colore dell'header */
    .stApp > header {{
        background-color: {header_color};
    }}

    /* Colore del testo nell'header */
    .stApp > header p {{
        color: {text_color};
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Definizione delle pagine e delle loro descrizioni
pagine = {
    "Home": "Welcome page and overview of the application",
    "Analysis": "Detailed analysis of financial data",
    "Basic Strategy": "Create and test basic trading strategies",
    "Credits": "Information about the creators and contributors"
}

# Funzioni di navigazione individuali
def go_to_home():
    st.session_state.selezione_pagina = "Home"
    st.experimental_rerun()

def go_to_analysis():
    st.session_state.selezione_pagina = "Analysis"
    st.experimental_rerun()

def go_to_basic_strategy():
    st.session_state.selezione_pagina = "Basic Strategy"
    st.experimental_rerun()

def go_to_credits():
    st.session_state.selezione_pagina = "Credits"
    st.experimental_rerun()
def nav_buttons():
    cols = st.columns(len(pagine))
    for idx, page in enumerate(pagine.keys()):
        if cols[idx].button(page, key=f"nav_{page}_{st.session_state.selezione_pagina}"):
            st.session_state.selezione_pagina = page
            st.experimental_rerun()


def sidebar_nav():
    st.sidebar.title("Web App Pages")
    for page, description in pagine.items():
        # Contenitore principale con flexbox
        with st.sidebar.container():
            st.markdown("""
            <div class="flex-container">
            """, unsafe_allow_html=True)

            # Botton & image
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.image("https://i.postimg.cc/7LynpkrL/Whats-App-Image-2024-07-27-at-16-36-44.jpg", width=30)
            with col2:
                if st.button(page, key=f"sidebar_{page}"):
                    st.session_state.selezione_pagina = page
                    st.experimental_rerun()

            # Closing
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)

            # Description
            st.markdown(f"""
            <style>
            .white-text {{
              color: white;
            }}
            .flex-container {{
                display: flex;
                align-items: center;
            }}
            </style>

            <p class="white-text">{description}</p>
            """, unsafe_allow_html=True)

# Inizializzazione della variabile di stato per la selezione della pagina
if 'selezione_pagina' not in st.session_state:
    st.session_state.selezione_pagina = "Home"

# Applica il CSS personalizzato
apply_custom_css(sidebar_color, main_bg_color, text_color, widget_color, header_color)

# Sidebar navigation
sidebar_nav()

# Main content
if st.session_state.selezione_pagina == "Home":
    Home()
    st.write("## Navigate to other pages:")
    nav_buttons()
#    if st.button("Create your basic strategy!"):
#        go_to_basic_strategy()

elif st.session_state.selezione_pagina == "Analysis":
    main_page()
    st.write("## Navigate to other pages:")
    nav_buttons()

elif st.session_state.selezione_pagina == "Basic Strategy":
    st.write("# Create a basic strategy")
    Simple_strategy()
    st.write("## Navigate to other pages:")
    nav_buttons()

elif st.session_state.selezione_pagina == "Credits":
    credits()
    st.write("## Navigate to other pages:")
    nav_buttons()
