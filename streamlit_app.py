import streamlit as st
import pandas as pd
import tempfile
import base64
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
from weasyprint import HTML
from datetime import date
from contextlib import contextmanager



# Düsseldorfer Tabelle als Dictionarys # Pflegebedarf
duesseldorfer_tabellen = {
    "2023": {
    '0-5': {
        'bis_1900': 437, '1901_2300': 459,
        '2301_2700': 481, '2701_3100': 503,
        '3101_3500': 525, '3501_3900': 560,
        '3901_4300': 595, '4301_4700': 630,
        '4701_5100': 665, '5101_5500': 700,
        '5501_6200': 735, '6201_7000': 770,
        '7001_8000': 805, '8001_9500': 840,
        '9501_11000': 874
    },
    
    '6-11': {
        'bis_1900': 502, '1901_2300': 528,
        '2301_2700': 553, '2701_3100': 578,
        '3101_3500': 603, '3501_3900': 643,
        '3901_4300': 683, '4301_4700': 723,
        '4701_5100': 764, '5101_5500': 804,
        '5501_6200': 844, '6201_7000': 884,
        '7001_8000': 924, '8001_9500': 964,
        '9501_11000': 1_004
    },
    
    '12-17': {
        'bis_1900': 588, '1901_2300': 618,
        '2301_2700': 647, '2701_3100': 677,
        '3101_3500': 706, '3501_3900': 753,
        '3901_4300': 800, '4301_4700': 847,
        '4701_5100': 894, '5101_5500': 941,
        '5501_6200': 988, '6201_7000': 1_035,
        '7001_8000': 1_082, '8001_9500': 1_129,
        '9501_11000': 1_176
    },
    '18+': {
        'bis_1900': 628, '1901_2300': 660,
        '2301_2700': 691, '2701_3100': 723,
        '3101_3500': 754, '3501_3900': 804,
        '3901_4300': 855, '4301_4700': 905,
        '4701_5100': 955, '5101_5500': 1_005,
        '5501_6200': 1_056, '6201_7000': 1_106,
        '7001_8000': 1_156, '8001_9500': 1_206,
        '9501_11000': 1_256
    },
},

"2024": {
    '0-5': {
        'bis_2100': 480, '2101_2500': 504,
        '2501_2900': 528, '2901_3300': 552,
        '3301_3700': 576, '3701_4100': 615,
        '4101_4500': 653, '4501_4900': 692,
        '4901_5300': 730, '5301_5700': 768,
        '5701_6400': 807, '6401_7200': 845,
        '7201_8200': 884, '8201_9700': 922,
        '9701_11200': 960
    },
    '6-11': {
        'bis_2100': 551, '2101_2500': 579,
        '2501_2900': 607, '2901_3300': 634,
        '3301_3700': 662, '3701_4100': 706,
        '4101_4500': 750, '4501_4900': 794,
        '4901_5300': 838, '5301_5700': 882,
        '5701_6400': 926, '6401_7200': 970,
        '7201_8200': 1_014, '8201_9700': 1_058,
        '9701_11200': 1_102
    },
    '12-17': {
        'bis_2100': 645, '2101_2500': 678,
        '2501_2900': 710, '2901_3300': 742,
        '3301_3700': 774, '3701_4100': 826,
        '4101_4500': 878, '4501_4900': 929,
        '4901_5300': 981, '5301_5700': 1_032,
        '5701_6400': 1_084, '6401_7200': 1_136,
        '7201_8200': 1_187, '8201_9700': 1_239,
        '9701_11200': 1_290
    },
    '18+': {
        'bis_2100': 689, '2101_2500': 724,
        '2501_2900': 758, '2901_3300': 793,
        '3301_3700': 827, '3701_4100': 882,
        '4101_4500': 938, '4501_4900': 993,
        '4901_5300': 1_048, '5301_5700': 1_103,
        '5701_6400': 1_158, '6401_7200': 1_213,
        '7201_8200': 1_268, '8201_9700': 1_323,
        '9701_11200': 1_378
    },
},

 "2025": {
    '0-5': {
        'bis_2100': 482, '2101_2500': 507,
        '2501_2900': 531, '2901_3300': 555,
        '3301_3700': 579, '3701_4100': 617,
        '4101_4500': 656, '4501_4900': 695,
        '4901_5300': 733, '5301_5700': 772,
        '5701_6400': 810, '6401_7200': 849,
        '7201_8200': 887, '8201_9700': 926,
        '9701_11200': 964
    },
    '6-11': {
        'bis_2100': 554, '2101_2500': 582,
        '2501_2900': 610, '2901_3300': 638,
        '3301_3700': 665, '3701_4100': 710,
        '4101_4500': 754, '4501_4900': 798,
        '4901_5300': 843, '5301_5700': 887,
        '5701_6400': 931, '6401_7200': 976,
        '7201_8200': 1_020, '8201_9700': 1_064,
        '9701_11200': 1_108
    },
    '12-17': {
        'bis_2100': 649, '2101_2500': 682,
        '2501_2900': 714, '2901_3300': 747,
        '3301_3700': 779, '3701_4100': 831,
        '4101_4500': 883, '4501_4900': 935,
        '4901_5300': 987, '5301_5700': 1_039,
        '5701_6400': 1_091, '6401_7200': 1_143,
        '7201_8200': 1_195, '8201_9700': 1_247,
        '9701_11200': 1_298
    },
    '18+': {
        'bis_2100': 693, '2101_2500': 728,
        '2501_2900': 763, '2901_3300': 797,
        '3301_3700': 832, '3701_4100': 888,
        '4101_4500': 943, '4501_4900': 998,
        '4901_5300': 1_054, '5301_5700': 1_109,
        '5701_6400': 1_165, '6401_7200': 1_220,
        '7201_8200': 1_276, '8201_9700': 1_331,
        '9701_11200': 1_386
    }
}
}

### Selbstbehalte aus der Düsseldorfer Tabelle # Pflegebedarf
SELBSTBEHALTE = {
    "2023": {"notwendig_nicht_erwerbstätig": 1120, "notwendig_erwerbstätig": 1370, "angemessen": 1650},
    "2024": {"notwendig_nicht_erwerbstätig": 1200, "notwendig_erwerbstätig": 1450, "angemessen": 1750},
    "2025": {"notwendig_nicht_erwerbstätig": 1200, "notwendig_erwerbstätig": 1450, "angemessen": 1750},
}

def berechne_regelbedarf(bereinigtes_einkommen_vater, bereinigtes_einkommen_mutter, alter, jahr):

    einkommen = bereinigtes_einkommen_vater + bereinigtes_einkommen_mutter

    # Bestimme die Altersgruppe anhand des Alters
    if alter <= 5:
        altersgruppe_key = '0-5'
    elif alter <= 11:
        altersgruppe_key = '6-11'
    elif alter <= 17:
        altersgruppe_key = '12-17'
    else:
        altersgruppe_key = '18+'

    
    tabelle = duesseldorfer_tabellen.get(jahr, {})
    print(f"Jahr ist {jahr}")
    print(f"Alter ist {alter}")
    print(f"Einkommen ist {einkommen}")
    print(f"Tabelle für Jahr {jahr}: {tabelle}")
    
    if altersgruppe_key not in tabelle:
        st.warning("Altersgruppe nicht gefunden")
        return 0  # Standardwert zurückgeben
    
    altersgruppe = tabelle[altersgruppe_key]
    print(f"Altersgruppe Daten: {altersgruppe}")
    
    # Durchsuche die Einkommensbereiche in der Altersgruppe
    for einkommensbereich, regelbedarf in sorted(altersgruppe.items(), key=lambda x: int(x[0].split('_')[-1])):
        # Bestimme den unteren und oberen Grenzwert
        if einkommensbereich.startswith("bis"):
            lower = 0
            upper = int(einkommensbereich.split('_')[-1])
        else:
            parts = einkommensbereich.split('_')
            lower = int(parts[0])
            upper = int(parts[1])
        print(f"Prüfe Einkommensbereich: {lower} - {upper} für Einkommen {einkommen}")
        if lower <= einkommen <= upper:
            print(f"Passende Einkommensgruppe gefunden: {einkommensbereich}, Regelbedarf: {regelbedarf}")
            return regelbedarf  # Rückgabe des Regelbedarfs
    return 0

def get_kindergeld(jahr):
    kindergeld_werte = {
        "2023": 250,
        "2024": 250,
        "2025": 255
    }
    return kindergeld_werte.get(str(jahr), 0)  # Standardwert 0, falls Jahr nicht vorhanden


def berechne_ausgleichsanspruch(monat, jahr, einkommen_mutter, einkommen_vater, abzug_mutter, abzug_vater,
                                regelbedarf, mehrbedarf, mehrbez, sonderbedarf, sonderbez, kindergeld, kindergeld_empfaenger):


    # Bereinigung der Einkommen
    bereinigtes_einkommen_mutter = einkommen_mutter - abzug_mutter
    bereinigtes_einkommen_vater = einkommen_vater - abzug_vater

    
    # Gesamteinkommen beider Eltern
    gesamtes_einkommen = bereinigtes_einkommen_mutter + bereinigtes_einkommen_vater

    st.session_state.sockelbetrag_mutter = st.session_state.get("sockel_amt_mutter", 0.0)
    st.session_state.adjektiv_sockelbetrag_mutter = st.session_state.get("sockel_lbl_mutter", "angemessene")
    st.session_state.sockelbetrag_vater = st.session_state.get("sockel_amt_vater", 0.0)
    st.session_state.adjektiv_sockelbetrag_vater = st.session_state.get("sockel_lbl_vater", "angemessene")

    
    verteilbarer_betrag_mutter = bereinigtes_einkommen_mutter - st.session_state.sockelbetrag_mutter
    verteilbarer_betrag_vater = bereinigtes_einkommen_vater - st.session_state.sockelbetrag_vater
    # Wenn der verteilbare Betrag negativ ist, setze ihn auf 0
    if verteilbarer_betrag_mutter < 0:
        verteilbarer_betrag_mutter = 0
    if verteilbarer_betrag_vater < 0:
        verteilbarer_betrag_vater = 0
    
    # Haftungsanteile in %
    verteilbarer_betrag_gesamt = verteilbarer_betrag_mutter + verteilbarer_betrag_vater
    anteil_mutter = verteilbarer_betrag_mutter / verteilbarer_betrag_gesamt
    anteil_vater = verteilbarer_betrag_vater / verteilbarer_betrag_gesamt
    
   # Kindergeldverrechnung (hälftig)
    betreuungsanteil = kindergeld / 2  # Der Betreuungsanteil ist die Hälfte des Kindergeldes
    baranteil = kindergeld / 2          # Der Baranteil ist die andere Hälfte
    
    # Verteilung des Betreuungsanteils (gleichmäßig)
    betreuungsanteil_mutter = betreuungsanteil / 2
    betreuungsanteil_vater = betreuungsanteil / 2
    
    # Verteilung des Baranteils (nach Haftungsanteil)
    baranteil_mutter = baranteil * anteil_mutter
    baranteil_vater = baranteil * anteil_vater
    
    # Gesamtbedarf des Kindes
    zusatzbedarf = mehrbedarf + sonderbedarf
    gesamtbedarf = regelbedarf + zusatzbedarf

    # Anteil der Eltern am Gesamtbedarf in Geldbetragshöhe
    anteil_mutter_gesamtbedarf = anteil_mutter * gesamtbedarf
    anteil_vater_gesamtbedarf = anteil_vater * gesamtbedarf

    if zusatz_allein_tragen == "Ja, vom Vater":
        anteil_mutter_gesamtbedarf = anteil_mutter * regelbedarf
        anteil_vater_gesamtbedarf = (anteil_vater * regelbedarf) + zusatzbedarf 
    elif zusatz_allein_tragen == "Ja, von der Mutter":
        anteil_mutter_gesamtbedarf = (anteil_mutter * regelbedarf) + zusatzbedarf
        anteil_vater_gesamtbedarf = anteil_vater * regelbedarf

    # Berechnung der Differenz der Anteile als absolute Differenz
    differenz_anteile = abs(anteil_mutter_gesamtbedarf - anteil_vater_gesamtbedarf)
    if zusatz_allein_tragen == "Ja, vom Vater":
        differenz_anteile = abs(anteil_mutter_gesamtbedarf - (anteil_vater * regelbedarf))
    elif zusatz_allein_tragen == "Ja, von der Mutter":
        differenz_anteile = abs((anteil_mutter * regelbedarf) - anteil_vater_gesamtbedarf)
        
    auszugleichender_betrag = differenz_anteile / 2     ### auszugleichender Betrag ist eigentlich DER Ausgleichsanspruch, der wird
                                                        ### wird aber noch durch die Verrechnungen korrigiert        
    st.session_state.basis_ausgleich = auszugleichender_betrag

    if anteil_vater_gesamtbedarf > anteil_mutter_gesamtbedarf:
        anspruchsberechtigt = "Mutter"
        nicht_anspruchsberechtigt = "Vater"
    else:
        anspruchsberechtigt = "Vater"
        nicht_anspruchsberechtigt = "Mutter"

     ### Verrechnung bereits getragener Zusatzbedarfe
        # Zusatzbedarf soll geteilt werden
    abzufuehrender_zusatz_an_vater = 0
    abzufuehrender_zusatz_an_mutter = 0
    if zusatz_allein_tragen == "Nein":
        if zusatzbedarf_getragen_mutter > 0:
            abzufuehrender_zusatz_an_mutter = 0.5 * zusatzbedarf_getragen_mutter
        if zusatzbedarf_getragen_vater > 0:
            abzufuehrender_zusatz_an_vater = 0.5 * zusatzbedarf_getragen_vater

    # Zusatzbedarf soll vom Vater allein getragen werden
    elif zusatz_allein_tragen == "Ja, vom Vater":
        if zusatzbedarf_getragen_mutter > 0:
            abzufuehrender_zusatz_an_mutter = zusatzbedarf_getragen_mutter  # voller Ausgleich
        # Vater hat gezahlt → kein Ausgleich nötig

    # Zusatzbedarf soll von der Mutter allein getragen werden
    elif zusatz_allein_tragen == "Ja, von der Mutter":
        if zusatzbedarf_getragen_vater > 0:
            abzufuehrender_zusatz_an_vater = zusatzbedarf_getragen_vater  # voller Ausgleich
        # Mutter hat gezahlt → kein Ausgleich nötig

    if anspruchsberechtigt == "Mutter":
        auszugleichender_betrag = (differenz_anteile / 2) - abzufuehrender_zusatz_an_vater + abzufuehrender_zusatz_an_mutter
        st.session_state.auszugleichender_betrag_nach_zusatzverrechnung = auszugleichender_betrag
    if anspruchsberechtigt == "Vater":
        auszugleichender_betrag = (differenz_anteile / 2) + abzufuehrender_zusatz_an_vater - abzufuehrender_zusatz_an_mutter
        st.session_state.auszugleichender_betrag_nach_zusatzverrechnung = auszugleichender_betrag
                
    # Berechnung des abzuführenden Kindergeldes
    if kindergeld_empfaenger == "Mutter":
        abzufuehrendes_kindergeld = betreuungsanteil_vater + baranteil_vater
    else:
        abzufuehrendes_kindergeld = betreuungsanteil_mutter + baranteil_mutter ##Also wenn der Vater das Kindergeld kriegt und er abführen muss

# Berechnung des Ausgleichsanspruchs unter Berücksichtigung des abzuführenden Kindergeldes
    
    if anspruchsberechtigt == "Mutter":
        # Wenn die Mutter anspruchsberechtigt ist, und das Kindergeld geht an den Vater:
        if kindergeld_empfaenger == "Vater":
            ausgleichsanspruch = auszugleichender_betrag + abzufuehrendes_kindergeld  # Kindergeld wird oben draufgerechnet
        else:
            ausgleichsanspruch = auszugleichender_betrag - abzufuehrendes_kindergeld  # Kindergeld wird abgezogen
    else:
        # Wenn der Vater anspruchsberechtigt ist, und das Kindergeld geht an die Mutter:
        if kindergeld_empfaenger == "Mutter":
            ausgleichsanspruch = auszugleichender_betrag + abzufuehrendes_kindergeld  # Kindergeld wird oben draufgerechnet
        else:
            ausgleichsanspruch = auszugleichender_betrag - abzufuehrendes_kindergeld  # Kindergeld wird abgezogen

    print(f"Ausgleichsanspruch: {ausgleichsanspruch} EUR")

    # für weitere Vorgänge bei streamlit übertragen
    st.session_state.verteilbarer_betrag_mutter = verteilbarer_betrag_mutter
    st.session_state.verteilbarer_betrag_vater = verteilbarer_betrag_vater
    st.session_state.verteilbarer_betrag_gesamt = verteilbarer_betrag_gesamt
    st.session_state.anteil_mutter = anteil_mutter
    st.session_state.anteil_vater = anteil_vater
    st.session_state.gesamtes_einkommen = gesamtes_einkommen
    st.session_state.regelbedarf = regelbedarf
    st.session_state.zusatzbedarf = zusatzbedarf
    st.session_state.mehrbedarf = mehrbedarf
    st.session_state.sonderbedarf = sonderbedarf
    st.session_state.gesamtbedarf = gesamtbedarf
    st.session_state.kindergeld = kindergeld
    st.session_state.betreuungsanteil_mutter = betreuungsanteil_mutter
    st.session_state.betreuungsanteil_vater = betreuungsanteil_vater
    st.session_state.baranteil_mutter = baranteil_mutter
    st.session_state.baranteil_vater = baranteil_vater
    st.session_state.anteil_mutter_gesamtbedarf = anteil_mutter_gesamtbedarf
    st.session_state.anteil_vater_gesamtbedarf = anteil_vater_gesamtbedarf
    st.session_state.differenz_anteile = differenz_anteile
    st.session_state.anspruchsberechtigt = anspruchsberechtigt
    st.session_state.nicht_anspruchsberechtigt = nicht_anspruchsberechtigt
    st.session_state.auszugleichender_betrag = auszugleichender_betrag
    st.session_state.abzufuehrendes_kindergeld = abzufuehrendes_kindergeld
    st.session_state.ausgleichsanspruch = ausgleichsanspruch
    
    ###RECHENWEG WEBSITE ANFANG###
    # Liste für Tabelleninhalte initialisieren
    werte_vater = [f"{st.session_state.einkommen_vater:.2f} €"]
    index_vater = ["Einkommen"]

    # Dynamische Abzugsposten einfügen (falls vorhanden)
    for i, abzug in enumerate(st.session_state.abzugsposten_vater):
        bezeichnung = abzug.get("bezeichnung", f"Abzugsposten {i + 1}")
        wert = float(abzug.get("wert", "0"))
        index_vater.append(f"  ./. Abzug: {bezeichnung}")
        werte_vater.append(f"{wert:.2f} €")

    # Restliche Werte zur Tabelle hinzufügen
    werte_vater.extend([
        f"{st.session_state.abzug_vater:.2f} €",
        f"{bereinigtes_einkommen_vater:.2f} €",
        f"{st.session_state.sockelbetrag_vater:.2f} €",
        f"{anteil_vater:.2%}",
        f"{baranteil_vater:.2f} €",
        f"{betreuungsanteil_vater:.2f} €"
    ])

    index_vater.extend([
        "Abzug Gesamt",
        "Bereinigtes Einkommen",
        f"{st.session_state.adjektiv_sockelbetrag_vater}r Selbstbehalt",
        "Haftungsanteil",
        "Baranteil",
        "Betreuungsanteil"
    ])

    # DataFrame erstellen
    df_vater = pd.DataFrame({
        "": werte_vater
    }, index=index_vater)

    # Liste für Tabelleninhalte initialisieren
    werte_mutter = [f"{st.session_state.einkommen_mutter:.2f} €"]
    index_mutter = ["Einkommen"]

    # Dynamische Abzugsposten einfügen (falls vorhanden)
    for i, abzug in enumerate(st.session_state.abzugsposten_mutter):
        bezeichnung = abzug.get("bezeichnung", f"Abzugsposten {i + 1}")
        wert = float(abzug.get("wert", "0"))
        index_mutter.append(f"  ./. Abzug: {bezeichnung}")
        werte_mutter.append(f"{wert:.2f} €")

    # Restliche Werte zur Tabelle hinzufügen
    werte_mutter.extend([
        f"{st.session_state.abzug_mutter:.2f} €",
        f"{bereinigtes_einkommen_mutter:.2f} €",
        f"{st.session_state.sockelbetrag_mutter:.2f} €",
        f"{anteil_mutter:.2%}",
        f"{baranteil_mutter:.2f} €",
        f"{betreuungsanteil_mutter:.2f} €"
    ])

    index_mutter.extend([
        "Abzug Gesamt",
        "Bereinigtes Einkommen",
        f"{st.session_state.adjektiv_sockelbetrag_mutter}r Selbstbehalt",
        "Haftungsanteil",
        "Baranteil",
        "Betreuungsanteil"
    ])

    # DataFrame erstellen
    df_mutter = pd.DataFrame({
        "": werte_mutter
    }, index=index_mutter)

    df_kind = pd.DataFrame({
        "": [
            f"{regelbedarf:.2f} EUR",
            f"{mehrbedarf:.2f} EUR" if mehrbedarf > 0 else "-",
            f"{sonderbedarf:.2f} EUR" if sonderbedarf > 0 else "-",
            f"{gesamtbedarf:.2f} EUR",
            f"{kindergeld:.2f} EUR",
            kindergeld_empfaenger
        ]
    }, index=[
        "Regelbedarf",
        "Mehrbedarf",
        "Sonderbedarf",
        "Gesamtbedarf",
        "Kindergeld",
        "Kindergeldempfänger"
    ])    

    col1, col2 = st.columns(2)
    with col1:
        st.write("### Vater")
        st.table(df_vater.style.hide(axis="index"))

    with col2:
        st.write("### Mutter")
        st.table(df_mutter.style.hide(axis="index"))

    st.write(f"### Bedarf Kind ({st.session_state.alter} Jahre alt)")
    st.table(df_kind.style.hide(axis="index"))

    st.write(f"### Ausgleichsanspruch von {st.session_state.anspruchsberechtigt} gegen {st.session_state.nicht_anspruchsberechtigt}:    {st.session_state.ausgleichsanspruch:.2f} EUR")

    if st.session_state.freitext_input.strip():
        st.markdown("### Erläuterungen und Anmerkungen:")
        st.markdown(st.session_state.freitext_input)
    ###RECHENWEG WEBSITE ENDE###


    return ausgleichsanspruch

### PDF ANFANG ###
def erstelle_pdf():
    dateiname = f"Ausgleichsanspruch{monat}{jahr}.pdf"

    html_content = f"""
    <html>
    <head>
    <style>
        @page {{
            @bottom-center {{
                content: "Seite " counter(page) " von " counter(pages);
                font-size: 9pt;
                border-top: 1px solid #000;
                padding-top: 6px;
            }}
        }}
        body {{
            font-family: "Times New Roman", Times, serif;
            font-size: 12pt;
            margin: 40px;
            color: #000;
            background: #fff;
        }}
        h1 {{
            font-weight: bold;
            font-size: 14pt;
            margin-top: 80px;
            margin-bottom: 0.2em;
            text-align: left;
            font-family: Georgia, serif;
        }}
        hr {{
            border: none;
            border-top: 1px solid #000;
            margin-bottom: 0.6em;
        }}
        .stand {{
            font-size: 12pt;
            margin-top: 0;
            margin-bottom: 1.5em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.8em;
            margin-bottom: 1.5em;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 6px 10px;
        }}
        th {{
            font-weight: bold;
            background: #fff;
            text-align: left;
        }}
        td {{
            text-align: right;
        }}
        td.left {{
            text-align: left;
        }}
        p {{
            font-style: normal;
            font-size: 12pt;
            margin-top: 0;
            margin-bottom: 1em;
            color: #000;
        }}
        .footnote {{
            font-size: 9pt;
            border-top: 1px solid #000;
            padding-top: 6px;
            margin-top: 3em;
            text-align: center;
        }}
        .logo {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 100px;
        }}
    </style>
    </head>
    <body>
        <img src="logo.png" class="logo" alt="Logo"/>
        <h1>Berechnung Ausgleichsanspruch im Wechselmodell {monat} {jahr}</h1>
        <hr/>
        <p class="stand">Stand: {st.session_state.heute}</p>

        {erstelle_tabelle_html("Vater", erstelle_daten_vater())}
        {erstelle_tabelle_html("Mutter", erstelle_daten_mutter())}

        <p>Für den Kindsvater wurde der {st.session_state.adjektiv_sockelbetrag_vater} Selbstbehalt berücksichtigt.</p>
        <p>Für die Kindsmutter wurde der {st.session_state.adjektiv_sockelbetrag_mutter} Selbstbehalt berücksichtigt.</p>

        <p>Relevantes Gesamteinkommen für den Regelbedarf: {st.session_state.gesamtes_einkommen:.2f} €</p>
        <p>Verteilbarer Betrag Gesamt: {st.session_state.verteilbarer_betrag_gesamt:.2f} €</p>
        <p>Haftungsanteil Mutter: {st.session_state.anteil_mutter:.2%}</p>
        <p>Haftungsanteil Vater: {st.session_state.anteil_vater:.2%}</p>

        {erstelle_tabelle_html(f"Angaben zum Kind ({st.session_state.alter} Jahre alt)", erstelle_daten_kind())}

        <p>Anteil Mutter am Gesamtbedarf: {st.session_state.anteil_mutter_gesamtbedarf:.2f} €</p>
        <p>Anteil Vater am Gesamtbedarf: {st.session_state.anteil_vater_gesamtbedarf:.2f} €</p>

        {zusatzbedarf_text(zusatz_allein_tragen)}

        <p>Differenz: {st.session_state.differenz_anteile:.2f} €</p>
        <p>Auszugleichender Betrag (1/2) von {st.session_state.nicht_anspruchsberechtigt} zu leisten an {st.session_state.anspruchsberechtigt}: {st.session_state.basis_ausgleich:.2f} €</p>

        {zusatzbedarf_getragen_text(zusatz_allein_tragen)}

        {erstelle_tabelle_html("Kindergeldverrechnung", erstelle_daten_kindergeld())}

        {kindergeld_empfaenger_text(kindergeld_empfaenger)}

        <p>Ausgleichsanspruch von {st.session_state.anspruchsberechtigt} gegen {st.session_state.nicht_anspruchsberechtigt}: {st.session_state.ausgleichsanspruch:.2f} €</p>

        <h2>Erläuterungen und Anmerkungen:</h2>
        <p>{freitext_input}</p>

        <p>Diese Berechnung wurde mithilfe des ASGLA-Rechners (https://asgla-testversion.streamlit.app/) vom LegalTech Lab JTC der Martin-Luther-Universität Halle-Wittenberg erstellt.</p>

    </body>
    </html>
    """

    pdf_bytes = HTML(string=html_content, base_url=".").write_pdf()
    return BytesIO(pdf_bytes)


def erstelle_tabelle_html(titel, daten):
    table_html = f"<h2>{titel}</h2><table><thead><tr><th>Bezeichnung</th><th>Betrag</th></tr></thead><tbody>"
    for row in daten:
        table_html += f"<tr><td class='left'>{row[0]}</td><td>{row[1]}</td></tr>"
    table_html += "</tbody></table>"
    return table_html


def erstelle_daten_vater():
    daten = [
        ["Einkommen", f"{st.session_state.einkommen_vater:.2f} €"],
    ]
    for i, eintrag in enumerate(st.session_state.abzugsposten_vater):
        if isinstance(eintrag, dict):
            bezeichnung = eintrag.get("bezeichnung", f"Abzugsposten {i + 1}")
            wert = eintrag.get("wert", "")
        else:
            bezeichnung = f"Abzugsposten {i + 1}"
            wert = eintrag
        try:
            zahl = float(wert)
            daten.append([bezeichnung, f"{zahl:.2f} €"])
        except ValueError:
            daten.append([bezeichnung, "ungültig"])
    daten.append(["Abzug Gesamt", f"{st.session_state.abzug_vater:.2f} €"])
    daten.extend([
        ["= bereinigtes Einkommen", f"{st.session_state.bereinigtes_einkommen_vater:.2f} €"],
        ["./. Selbstbehalt", f"{st.session_state.sockelbetrag_vater:.2f} €"],
        ["= verteilbarer Betrag", f"{st.session_state.verteilbarer_betrag_vater:.2f} €"],
    ])
    return daten


def erstelle_daten_mutter():
    daten = [
        ["Einkommen", f"{st.session_state.einkommen_mutter:.2f} €"],
    ]
    for i, eintrag in enumerate(st.session_state.abzugsposten_mutter):
        if isinstance(eintrag, dict):
            bezeichnung = eintrag.get("bezeichnung", f"Abzugsposten {i + 1}")
            wert = eintrag.get("wert", "")
        else:
            bezeichnung = f"Abzugsposten {i + 1}"
            wert = eintrag
        try:
            zahl = float(wert)
            daten.append([bezeichnung, f"{zahl:.2f} €"])
        except ValueError:
            daten.append([bezeichnung, "ungültig"])
    daten.append(["Abzug Gesamt", f"{st.session_state.abzug_mutter:.2f} €"])
    daten.extend([
        ["= bereinigtes Einkommen", f"{st.session_state.bereinigtes_einkommen_mutter:.2f} €"],
        ["./. Selbstbehalt", f"{st.session_state.sockelbetrag_mutter:.2f} €"],
        ["= verteilbarer Betrag", f"{st.session_state.verteilbarer_betrag_mutter:.2f} €"],
    ])
    return daten


def erstelle_daten_kind():
    daten = [["Regelbedarf", f"{st.session_state.regelbedarf:.2f} €"]]
    if st.session_state.zusatzbedarf > 0:
        daten.append(["Zusatzbedarf", f"{st.session_state.zusatzbedarf:.2f} €"])
    if st.session_state.mehrbedarf > 0:
        daten.append([f"davon Mehrbedarf ({st.session_state.mehrbez})", f"{st.session_state.mehrbedarf:.2f} €"])
    if st.session_state.sonderbedarf > 0:
        daten.append([f"davon Sonderbedarf ({st.session_state.sonderbez})", f"{st.session_state.sonderbedarf:.2f} €"])
    daten.append(["= Gesamtbedarf", f"{st.session_state.gesamtbedarf:.2f} €"])
    daten.append(["Kindergeld", f"{st.session_state.kindergeld:.2f} €"])
    return daten


def zusatzbedarf_text(zusatz_allein_tragen):
    if zusatz_allein_tragen == "Ja, vom Vater":
        return """
        <p>Haftungsanteil der KM bezieht sich nur auf Regelbedarf, da der Zusatzbedarf hier von KV allein zu tragen ist.</p>
        <p>Differenz für Ausgleich bezieht sich folglich nur auf den Regelbedarf.</p>
        """
    elif zusatz_allein_tragen == "Ja, von der Mutter":
        return """
        <p>Haftungsanteil des KV bezieht sich nur auf Regelbedarf, da der Zusatzbedarf hier von KM allein zu tragen ist.</p>
        <p>Differenz für Ausgleich bezieht sich folglich nur auf den Regelbedarf.</p>
        """
    else:
        return ""


def zusatzbedarf_getragen_text(zusatz_allein_tragen):
    texte = []
    if st.session_state.zusatzbedarf_getragen_vater > 0:
        texte.append(f"<p>Von KV bereits getragener Zusatzbedarf: {st.session_state.zusatzbedarf_getragen_vater:.2f} € ({st.session_state.zusatzbez_getragen_vater})</p>")
        if zusatz_allein_tragen == "Nein":
            texte.append(f"<p>Daher hälftig ({st.session_state.zusatzbedarf_getragen_vater / 2:.2f} €) bei KM zu verrechnen.</p>")
        if zusatz_allein_tragen == "Ja, vom Vater":
            texte.append("<p>Zusatzbedarf ist aufgrund der elterlichen Einkommensverhältnisse hier vom Kindsvater selbst zu tragen. Daher findet insoweit keine Verrechnung statt.</p>")
        if zusatz_allein_tragen == "Ja, von der Mutter":
            texte.append("<p>Die Kindsmutter hat aufgrund der elterlichen Einkommensverhältnisse Zusatzbedarfe allein zu tragen. Daher findet insoweit eine vollständige Erstattung statt.</p>")
    if st.session_state.zusatzbedarf_getragen_mutter > 0:
        texte.append(f"<p>Von KM bereits getragener Zusatzbedarf: {st.session_state.zusatzbedarf_getragen_mutter:.2f} € ({st.session_state.zusatzbez_getragen_mutter})</p>")
        if zusatz_allein_tragen == "Nein":
            texte.append(f"<p>Daher hälftig ({st.session_state.zusatzbedarf_getragen_mutter / 2:.2f} €) bei KV zu verrechnen.</p>")
        if zusatz_allein_tragen == "Ja, von der Mutter":
            texte.append("<p>Zusatzbedarf ist aufgrund der elterlichen Einkommensverhältnisse hier von der Kindsmutter selbst zu tragen. Daher findet insoweit keine Verrechnung statt.</p>")
        if zusatz_allein_tragen == "Ja, vom Vater":
            texte.append("<p>Der Kindsvater hat aufgrund der elterlichen Einkommensverhältnisse Zusatzbedarfe allein zu tragen. Daher findet insoweit eine vollständige Erstattung statt.</p>")
    if texte:
        texte.append(f"<p>Auszugleichender Betrag (1/2) nach Verrechnung des bereits getragenen Zusatzbedarfs: {st.session_state.auszugleichender_betrag_nach_zusatzverrechnung:.2f} €</p>")
    return "".join(texte)


def erstelle_daten_kindergeld():
    return [
        ["Kindergeldempfänger", st.session_state.kindergeld_empfaenger],
        ["Betreuungsanteil Mutter", f"{st.session_state.betreuungsanteil_mutter:.2f} €"],
        ["Baranteil Mutter", f"{st.session_state.baranteil_mutter:.2f} €"],
        ["Betreuungsanteil Vater", f"{st.session_state.betreuungsanteil_vater:.2f} €"],
        ["Baranteil Vater", f"{st.session_state.baranteil_vater:.2f} €"]
    ]


def kindergeld_empfaenger_text(empfaenger):
    if empfaenger == "Mutter":
        return f"<p>Daher von der Kindsmutter an den Kindsvater abzuführendes Kindergeld: {st.session_state.abzufuehrendes_kindergeld:.2f} €</p>"
    elif empfaenger == "Vater":
        return f"<p>Daher von dem Kindsvater an die Kindsmutter abzuführendes Kindergeld: {st.session_state.abzufuehrendes_kindergeld:.2f} €</p>"
    return ""
### PDF ENDE ###

def berechne_und_zeige():

    st.session_state.monat = monat
    st.session_state.jahr = jahr

    # Mutter
    st.session_state.haupttaetigkeit_mutter = get_float_or_zero(haupttaetigkeit_mutter_input)
    st.session_state.weitere_einkuenfte_mutter = get_float_or_zero(weitere_einkuenfte_mutter_input)
    st.session_state.einkommen_mutter = st.session_state.haupttaetigkeit_mutter + st.session_state.weitere_einkuenfte_mutter

    abzug_mutter = 0.0
    fehler_mutter = False

    for i, eintrag in enumerate(st.session_state.abzugsposten_mutter):
        wert = eintrag.get("wert", "")
        try:
            zahl = float(wert)
            if zahl < 0:
                st.error(f"Abzugsposten {i + 1} Mutter darf nicht negativ sein.")
                fehler_mutter = True
            else:
                abzug_mutter += zahl
        except ValueError:
            st.error(f"Abzugsposten {i + 1} Mutter ist keine gültige Zahl.")
            fehler_mutter = True

    if not fehler_mutter:
        st.session_state.abzug_mutter = abzug_mutter
        st.session_state.bereinigtes_einkommen_mutter = (
            st.session_state.einkommen_mutter - abzug_mutter
        )
        
    st.session_state.bereinigtes_einkommen_mutter = st.session_state.einkommen_mutter - st.session_state.abzug_mutter

    # Vater
    st.session_state.haupttaetigkeit_vater = get_float_or_zero(haupttaetigkeit_vater_input)
    st.session_state.weitere_einkuenfte_vater = get_float_or_zero(weitere_einkuenfte_vater_input)
    st.session_state.einkommen_vater = st.session_state.haupttaetigkeit_vater + st.session_state.weitere_einkuenfte_vater

    abzug_vater = 0.0
    fehler_vater = False

    for i, eintrag in enumerate(st.session_state.abzugsposten_vater):
        wert = eintrag.get("wert", "")
        try:
            zahl = float(wert)
            if zahl < 0:
                st.error(f"Abzugsposten {i + 1} Vater darf nicht negativ sein.")
                fehler_vater = True
            else:
                abzug_vater += zahl
        except ValueError:
            st.error(f"Abzugsposten {i + 1} Vater ist keine gültige Zahl.")
            fehler_vater = True

    if not fehler_vater:
        st.session_state.abzug_vater = abzug_vater
        st.session_state.bereinigtes_einkommen_vater = (
            st.session_state.einkommen_vater - abzug_vater
        )
        
    st.session_state.bereinigtes_einkommen_vater = st.session_state.einkommen_vater - st.session_state.abzug_vater

    # Bedarf Kind
    alter = alter_kind or 0  # Eingabe durch Nutzer
    st.session_state.alter = alter

    st.session_state.mehrbedarf = 0
    st.session_state.mehrbez = ''
    if zeige_mehrbedarf:
        st.session_state.mehrbedarf = get_float_or_zero(mehrbetrag)
        st.session_state.mehrbez = mehrbez or 'Mehrbedarf'

    st.session_state.sonderbedarf = 0
    st.session_state.sonderbez = ''
    if zeige_sonderbedarf:
        st.session_state.sonderbedarf = get_float_or_zero(sonderbetrag)
        st.session_state.sonderbez = sonderbez or 'Sonderbedarf'

    st.session_state.zusatzbedarf_getragen_vater = get_float_or_zero(zusatzbedarf_getragen_vater)
    st.session_state.zusatzbedarf_getragen_mutter = get_float_or_zero(zusatzbedarf_getragen_mutter)

    # Regelbedarf berechnen
    st.session_state.regelbedarf = berechne_regelbedarf(
        st.session_state.bereinigtes_einkommen_vater,
        st.session_state.bereinigtes_einkommen_mutter,
        alter,
        jahr
    )

    st.session_state.kindergeld = get_kindergeld(jahr)

    # Ausgleichsanspruch berechnen
    st.session_state.aktueller_anspruch = berechne_ausgleichsanspruch(
        monat,
        jahr,
        st.session_state.einkommen_mutter,
        st.session_state.einkommen_vater,
        st.session_state.abzug_mutter,
        st.session_state.abzug_vater,
        st.session_state.regelbedarf,
        st.session_state.mehrbedarf,
        st.session_state.mehrbez,
        st.session_state.sonderbedarf,
        st.session_state.sonderbez,
        st.session_state.kindergeld,
        kindergeld_empfaenger
    )

    st.session_state.aktuelle_eingaben = (
        monat,
        jahr,
        st.session_state.einkommen_mutter,
        st.session_state.einkommen_vater,
        st.session_state.regelbedarf,
        st.session_state.mehrbedarf,
        st.session_state.mehrbez,
        st.session_state.sonderbedarf,
        st.session_state.sonderbez,
        st.session_state.kindergeld,
        kindergeld_empfaenger
    )



# GUI ANFANG #
# Titel und feste "Fenstergröße" (Streamlit ist responsiv, aber wir können die Breite anpassen)
st.set_page_config(page_title="Ausgleichsanspruch Wechselmodell", layout="wide")
st.session_state.heute = date.today().strftime("%d.%m.%Y")

# Background # CSS mit Hintergrund einfügen

def get_base64_of_image(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_path):
    encoded = get_base64_of_image(image_path)
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Anwendung starten
set_background("background.png")

# CSS laden
def load_css(path):
    with open(path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# HTML laden mit Platzhalter für base64 Logo
def load_html(path, logo_b64):
    with open(path, "r") as f:
        html = f.read()
    html = html.replace("{logo_base64}", logo_b64)
    st.markdown(html, unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_path = "./logo.png"
css_path = "./design.css"
html_path = "./design.html"

logo_base64 = get_base64_image(logo_path)

load_html(html_path, logo_base64)
load_css(css_path)


# Abstand nach oben für den restlichen Content
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)


# Jahr/Monat Auswahl
col_jahr, col_monat = st.columns(2)
with col_jahr:
    jahr = st.selectbox("📆 Jahr", list(SELBSTBEHALTE.keys()), index=0)
with col_monat:
    monat = st.selectbox("📅 Monat", [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ], index=0)

# Werte bei Nichteingabe auf 0 setzen
def get_float_or_zero(val):
    try:
        if isinstance(val, (int, float)):
            return float(val)
        val = val.strip()
        # deutsches Format: z. B. "1.234,56"
        if ',' in val:
            val = val.replace('.', '')    # Tausenderpunkt raus
            val = val.replace(',', '.')   # Komma → Punkt
        # englisches Format lassen wir durch
        return float(val)
    except (ValueError, AttributeError):
        return 0.0

# Session-State initialisieren
for p in ["vater", "mutter"]:
    if f"sockel_amt_{p}" not in st.session_state:
        st.session_state[f"sockel_amt_{p}"] = SELBSTBEHALTE[jahr]["angemessen"]
        st.session_state[f"sockel_lbl_{p}"] = "angemessene"
    if f"edit_{p}" not in st.session_state:
        st.session_state[f"edit_{p}"] = False

# Wenn Jahr gewechselt wurde: Sockel auf Standard zurücksetzen
if st.session_state.get("jahr_prev") != jahr:
    for p in ["vater","mutter"]:
        st.session_state[f"sockel_amt_{p}"] = SELBSTBEHALTE[jahr]["angemessen"]
        st.session_state[f"sockel_lbl_{p}"] = "angemessene"
    st.session_state["jahr_prev"] = jahr

# Helper-Funktion: Sockel-Auswahl-Expander

# Form innerhalb des Expanders, sorgt dafür, dass der Bestätigen-Button beim ersten Klick greift
def sockel_expander(elternteil):
    radio_key = f"rad_{elternteil}"
    checkbox_key = f"chk_{elternteil}_nicht"
    custom_key = f"num_{elternteil}_custom"

    # Radio und dynamische Felder außerhalb der Form, damit sie sofort reagieren
    col1, col2 = st.columns([3, 1])
    with col1:
        auswahl = st.radio(
            "Bitte Sockelbetrag auswählen:",
            ["angemessen", "notwendig", "benutzerdefiniert"],
            key=radio_key
        )
    with col2:
        flag = None
        if auswahl == "notwendig":
            flag = st.checkbox(
                "nicht erwerbstätig",
                key=checkbox_key
            )

    custom = None
    if auswahl == "benutzerdefiniert":
        custom = st.number_input(
            "Benutzerdefinierter Betrag (€):", min_value=0.0,
            key=custom_key
        )

    # Form nur für den Button
    with st.form(f"form_{elternteil}"):
        submitted = st.form_submit_button("Bestätigen")
        if submitted:
            if auswahl == "angemessen":
                amt = SELBSTBEHALTE[jahr]["angemessen"]
                lbl = "angemessene"
            elif auswahl == "notwendig":
                # Falls Checkbox noch nicht gesetzt wurde, auf False zurückfallen
                is_nicht = st.session_state.get(checkbox_key, False)
                key_sb = "notwendig_nicht_erwerbstätig" if is_nicht else "notwendig_erwerbstätig"
                amt = SELBSTBEHALTE[jahr][key_sb]
                lbl = f"notwendige ({'nicht ' if is_nicht else ''}erwerbstätig)"
            else:
                # Falls Feld noch leer: 0.0 verwenden
                amt = st.session_state.get(custom_key, 0.0)
                lbl = "benutzerdefinierte"
            st.session_state[f"sockel_amt_{elternteil}"] = amt
            st.session_state[f"sockel_lbl_{elternteil}"] = lbl
            st.session_state[f"edit_{elternteil}"] = False
            st.rerun()

##Obercontainer in dem die Tabs sind für Übersichtlichkeit
with st.container():
    tabs = st.tabs(["👨 Einkünfte Vater", "👩 Einkünfte Mutter", "👶 Bedarf Kind"])


    # --- TAB 1: EINKÜNFTE VATER ---
    with tabs[0]:
        st.subheader("Vater – Einkünfte und Abzüge")

        col_einkünfte, col_abzüge = st.columns(2)

        with col_einkünfte:
            st.markdown("### Einkünfte")
            haupttaetigkeit_vater_input = st.text_input("Haupttätigkeit Vater:", value="5000")
            weitere_einkuenfte_vater_input = st.text_input("Weitere Einkünfte Vater:", value="300")

        with col_abzüge:
            st.markdown("### Abzüge")
            # Initialisierung der Abzugsposten
            if "abzugsposten_vater" not in st.session_state:
                st.session_state.abzugsposten_vater = []

            # Funktion zum Hinzufügen eines neuen Abzugspostens
            def add_abzugsposten_vater():
                if len(st.session_state.abzugsposten_vater) < 5:
                    index = len(st.session_state.abzugsposten_vater) + 1
                    st.session_state.abzugsposten_vater.append({"bezeichnung": f"Abzugsposten {index}", "wert": "100"})
                else:
                    st.warning("Es können maximal 5 Abzugsposten hinzugefügt werden!")

            # Darstellung der Abzugsposten mit Eingabefeldern
            for i, abzug in enumerate(st.session_state.abzugsposten_vater):
                cols = st.columns([3, 2, 1])

                bezeichnung_key = f"bezeichnung_vater_{i}"
                wert_key = f"wert_vater_{i}"

                abzug["bezeichnung"] = cols[0].text_input(
                    f"Bezeichnung {i + 1}:", value=abzug.get("bezeichnung", ""), key=bezeichnung_key
                )
                abzug["wert"] = cols[1].text_input(
                    f"Wert {i + 1}:", value=abzug.get("wert", ""), key=wert_key
                )

                if cols[2].button("❌", key=f"remove_abzug_vater_{i}"):
                    st.session_state.abzugsposten_vater.pop(i)
                    st.rerun()
                    break

            # Button zum Hinzufügen
            if st.button("Weitere Abzugsposten Vater hinzufügen"):
                add_abzugsposten_vater()
                st.rerun()

        # Aktueller Sockelbetrag
        st.info(f"Für den Kindsvater wird der **{st.session_state['sockel_lbl_vater']}** Selbstbehalt "
                f"von **{st.session_state['sockel_amt_vater']:.2f} €** berücksichtigt. (Jahr: {jahr})")

        if st.button("Ändern", key="btn_edit_vater"):
            st.session_state["edit_vater"] = True
        if st.session_state["edit_vater"]:
            with st.expander("Sockelbetrag anpassen", expanded=True):
                sockel_expander("vater")

    # --- TAB 2: EINKÜNFTE MUTTER ---
    with tabs[1]:
        st.subheader("Mutter – Einkünfte und Abzüge")

        col_einkünfte, col_abzüge = st.columns(2)

        with col_einkünfte:
            st.markdown("### Einkünfte")
            haupttaetigkeit_mutter_input = st.text_input("Haupttätigkeit Mutter:", value="2500")
            weitere_einkuenfte_mutter_input = st.text_input("Weitere Einkünfte Mutter:", value="100")

        with col_abzüge:
            st.markdown("### Abzüge")
            # Initialisierung der dynamischen Abzugsposten für Mutter
            if "abzugsposten_mutter" not in st.session_state:
                st.session_state.abzugsposten_mutter = []

            # Funktion zum Hinzufügen eines neuen Abzugspostens
            def add_abzugsposten_mutter():
                if len(st.session_state.abzugsposten_mutter) < 5:
                    index = len(st.session_state.abzugsposten_mutter) + 1
                    st.session_state.abzugsposten_mutter.append({
                        "bezeichnung": f"Abzugsposten {index}",
                        "wert": "100"
                    })
                else:
                    st.warning("Es können maximal 5 Abzugsposten hinzugefügt werden!")

            # Eingabefelder mit Entfernen-Button
            for i, abzug in enumerate(st.session_state.abzugsposten_mutter):
                cols = st.columns([4, 3, 1])
                bezeichnung = cols[0].text_input(
                    f"Bezeichnung {i + 1} Mutter:", value=abzug["bezeichnung"], key=f"abzug_mutter_bez_{i}"
                )
                wert = cols[1].text_input(
                    f"Wert {i + 1} Mutter:", value=abzug["wert"], key=f"abzug_mutter_wert_{i}"
                )

                # Aktualisiere den Eintrag
                st.session_state.abzugsposten_mutter[i] = {"bezeichnung": bezeichnung, "wert": wert}

                # Entfernen-Button
                if cols[2].button("❌", key=f"remove_abzug_mutter_{i}"):
                    st.session_state.abzugsposten_mutter.pop(i)
                    st.rerun()
                    break

            # Button zum Hinzufügen
            if st.button("Weitere Abzugsposten Mutter hinzufügen"):
                add_abzugsposten_mutter()
                st.rerun()
        
        st.info(f"Für die Kindsmutter wird der **{st.session_state['sockel_lbl_mutter']}** Selbstbehalt "
                f"von **{st.session_state['sockel_amt_mutter']:.2f} €** berücksichtigt. (Jahr: {jahr})")

        if st.button("Ändern", key="btn_edit_mutter"):
            st.session_state["edit_mutter"] = True
        if st.session_state["edit_mutter"]:
            with st.expander("Sockelbetrag anpassen", expanded=True):
                sockel_expander("mutter")

    # --- TAB 3: BEDARF KIND ---
    with tabs[2]:
        st.subheader("Bedarf Kind")

        ### Zum Kind
        alter_kind = st.number_input("Alter des Kindes", value=10, step=1, min_value=0)

        st.markdown("### Kindergeld")
        kindergeld_empfaenger = st.radio("Kindergeldempfänger:", ("Mutter", "Vater"), key="kindergeld_empfaenger")

        st.markdown("### Zusatzbedarfe")
        # Checkbox: Mehrbedarf
        zeige_mehrbedarf = st.checkbox("Mehrbedarf hinzufügen", value=True)

        if zeige_mehrbedarf:
            mehrbez = st.text_input("Bezeichnung Mehrbedarf", value="Hort")
            mehrbetrag = st.number_input("Betrag Mehrbedarf (EUR)", value=60)

        # Checkbox: Sonderbedarf
        zeige_sonderbedarf = st.checkbox("Sonderbedarf hinzufügen", value=True)

        if zeige_sonderbedarf:
            sonderbez = st.text_input("Bezeichnung Sonderbedarf", value="Zahnspange")
            sonderbetrag = st.number_input("Betrag Sonderbedarf (EUR)", value=80)

        zusatzbedarf_getragen_vater = 0
        zusatzbedarf_getragen_mutter = 0
        if zeige_mehrbedarf or zeige_sonderbedarf:
            st.markdown("Wurde bereits ein Zusatzbedarf teilweise geleistet?")
            chk_gezahlt_zusatz_v = st.checkbox("Ja, vom Kindsvater", value=False)
            if chk_gezahlt_zusatz_v:
                zusatzbez_getragen_vater = st.text_input("Bezeichnung von KV geleisteter Zusatzbedarf", key="zusatzbez_getragen_vater", value="")
                zusatzbedarf_getragen_vater = st.number_input("Bereits bezahlter Zusatzbedarf (EUR)", key="zusatzbedarf_getragen_vater", value=0)
            chk_gezahlt_zusatz_m = st.checkbox("Ja, von der Kindsmutter", value=False)
            if chk_gezahlt_zusatz_m:
                zusatzbez_getragen_mutter = st.text_input("Bezeichnung von KM geleisteter Zusatzbedarf", key="zusatzbez_getragen_mutter", value="")
                zusatzbedarf_getragen_mutter = st.number_input("Bereits bezahlter Zusatzbedarf (EUR)", key="zusatzbedarf_getragen_mutter", value=0)
            zusatz_allein_tragen = st.radio("Ist der Zusatzbedarf von einem der Elternteile allein zu tragen?", ("Nein", "Ja, vom Vater", "Ja, von der Mutter"), key="zusatz_allein_tragen")
            # key trägt das sofort in sessionstate ein

st.markdown("### Freitext für Anmerkungen / Sonstiges")
freitext_input = st.text_area("Zusätzliche Informationen oder Anmerkungen:", height=150, key="freitext_input")

if "berechnet" not in st.session_state:
    st.session_state["berechnet"] = False

# Berechnen Button
if st.button("Berechnen"):
    berechne_und_zeige()
    st.session_state["berechnet"] = True  # Merken, dass gerechnet wurde

# Ergebnis-Label
label_ergebnis = st.empty()  # Platzhalter für das Ergebnis
label_ergebnis.text("")  # Anfangszustand leer

# PDF speichern Button
if st.session_state["berechnet"]:
    st.download_button(
        label="PDF herunterladen",
        data=erstelle_pdf(),
        file_name=f"Ausgleichsanspruch_{st.session_state.monat}_{st.session_state.jahr}.pdf",
        mime="application/pdf"
    )
