import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
'''
    Spese relative al mutuo considerate:
        600 imposte, iva, varie
        366 perizia immobile + iva
        1% istruttoria
        imposta sostitutiva (0.25% se prima casa, se no 2%)
        assicurazione obbligatoria per legge (non è sulla vita) detraibile al 19%
    Spese notaio considerate:
        imposte di registro (2% se prima casa, 9% se non lo è), tetto minimo 1000 euro - detraibile se prima casa
        imposta ipotecaria e catastale, tot. 100 euro
        parcella notaio, circa 2000 euro IVA compresa
    Eventuali spese agenzia considerate:
        2% del prezzo di vendita + IVA 22%, con tetto minimo parcella 1000 euro + IVA
'''
#-------SEZIONE FUNZIONI---------
def calcola_mutuo(prezzo_casa, tasso, anni=20, percentuale=80, prima_casa=False, agenzia=True, rendita_catastale=490):
    # calcolo della rata mensile
    rata = prezzo_casa * percentuale/100 * tasso/100/12 / (1 - (1 + tasso/100/12) ** (-anni * 12))
    #-------------- SEZIONE SPESE INIZIALI UNA TANTUM --------------
    costi_irrecuperabili = 0
    if percentuale != 100:
        anticipo = prezzo_casa * (100 - percentuale) / 100
    else:
        anticipo = 0
    if percentuale:
        if prima_casa:
            imposte = 0.02
            spese_mutuo = 0.0025 * prezzo_casa * percentuale/100 + 600 + 366 + prezzo_casa * percentuale/100 * 0.01
        else:
            imposte = 0.09
            spese_mutuo = 0.02 * prezzo_casa * percentuale/100 + 600 + 366 + prezzo_casa * percentuale/100 * 0.01
    else:
        spese_mutuo = 0
        if prima_casa:
            imposte = 0.02
        else:
            imposte = 0.09
    baseline = spese_mutuo
    costi_irrecuperabili += spese_mutuo
    anticipo += spese_mutuo
    # Notaio e imposte
    if prezzo_casa * imposte >= 1000:
        anticipo += prezzo_casa * imposte + 2000 + 100
        costi_irrecuperabili += prezzo_casa * imposte + 2000 + 100
        baseline += prezzo_casa * imposte + 2000 + 100
    else:
        anticipo += 1000 + 2000 + 100
        costi_irrecuperabili += 1000 + 2000 + 100
        baseline += 1000 + 2000 + 100
    if agenzia:
        if prezzo_casa >= 50000:
            anticipo += prezzo_casa * 0.02 * 1.22
            costi_irrecuperabili += prezzo_casa * 0.02 * 1.22
            baseline += prezzo_casa * 0.02 * 1.22
        else:
            anticipo += 1000 * 1.22
            costi_irrecuperabili += 1000 * 1.22
            baseline += 1000 * 1.22
    #---------------------------------------------------------------

    #---------- SEZIONE DELLE SPESE ANNUALI ------------------------
    '''
    300 euro l'anno di spese straordinarie base, più 280 per un coefficiente che tiene conto del valore della casa:
    '''
    costo_annuo_spese = 300 + (280 * prezzo_casa/100000)
    interessi_totali = 0
    for i in range(anni):
        ris = calcola_quota_interessi(prezzo_casa * percentuale / 100, tasso, anni, i+1)
        '''
        Se è prima casa, possiamo detrarre gli interessi al 19% fino a 2582.25 euro annui di imponibile 
        (https://www.agenziaentrate.gov.it/portale/in-cosa-consiste-mutui-ristrutturazioni-edilizie),
        dò per scontato il fatto di avere abbastanza capienza fiscale
        '''
        if ris['interessi'] > 2582.25:
            interessi = ris['interessi'] - 2582.25 * 0.19
        else:
            interessi = ris['interessi'] * 0.81
        interessi_totali += interessi
        costi_irrecuperabili += costo_annuo_spese + 170*prezzo_casa/100000*0.81 # spese straordinarie e assicurazione
        if not prima_casa: # 0.009 è un'aliquota imu media
            costi_irrecuperabili += rendita_catastale * 1.05 * 160 * 0.009
    costi_irrecuperabili += interessi_totali

    # 170/12*prezzo_casa/100000 è un'assicurazione mensile sulla casa obbligatoria per legge col mutuo, detraibile al 19% anche se non è prima casa

    if percentuale:
        return rata + 170/12*prezzo_casa/100000*0.81, anticipo, costi_irrecuperabili, costo_annuo_spese, baseline
    else:
        anticipo -= spese_mutuo
        baseline -= spese_mutuo
        costi_irrecuperabili -= spese_mutuo
        return 0, anticipo, costi_irrecuperabili, costo_annuo_spese, baseline
def calcola_quota_interessi(capitale_iniziale, tasso_annuo, durata_anni, anno_desiderato):
    # converti il tasso annuo in tasso mensile e calcola il numero di rate
    tasso_mensile = (tasso_annuo / 100) / 12
    numero_rate = durata_anni * 12
    # calcola la rata mensile
    rata_mensile = capitale_iniziale * (tasso_mensile * (1 + tasso_mensile) ** numero_rate) / \
                   ((1 + tasso_mensile) ** numero_rate - 1)

    capitale_residuo = capitale_iniziale
    interessi_annuali = []
    capitale_residuo_iniziale_anno = capitale_iniziale
    for anno in range(1, int(durata_anni) + 1):
        interessi_anno = 0
        capitale_inizio_anno = capitale_residuo
        for mese in range(12):
            interesse_mese = capitale_residuo * tasso_mensile
            interessi_anno += interesse_mese
            capitale_pagato = rata_mensile - interesse_mese
            capitale_residuo -= capitale_pagato
        interessi_annuali.append({
            'anno': anno,
            'interessi': round(interessi_anno, 2),
            'capitale_iniziale': round(capitale_inizio_anno, 2),
            'capitale_residuo': round(capitale_residuo, 2)
        })
        # esci quando abbiamo raggiunto l'anno desiderato
        if anno == anno_desiderato:
            break
    for anno_data in interessi_annuali:
        if anno_data['anno'] == anno_desiderato:
            return anno_data
def calcola():
    try:
        prezzo_casa = float(ingresso_casa.get().replace(',', '.'))
        tasso = float(ingresso_tasso.get().replace(',', '.'))
        try:
            inflazione = float(inflazione_entry.get().replace(',', '.')) / 100
        except:
            inflazione = 0
        if tasso <= 0:
            etichetta_rata.config(text="Tasso <= 0 non supportato", foreground="red")
            etichetta_anticipo.config(text="")
            etichetta_costi.config(text="")
            return 
    except ValueError:
        etichetta_rata.config(text="Inserire tutti i valori (solo l'affitto può essere vuoto)", foreground="red")
        etichetta_anticipo.config(text="")
        etichetta_costi.config(text="")
        return 
    try:
        anni = int(float(ingresso_anni.get().replace(',', '.')))
    except:
        anni = 0
    try:
        percentuale = float(ingresso_percentuale.get().replace(',', '.'))
    except:
        percentuale = 0
    try:
        rendita_catastale = float(ingresso_rendita.get().replace(',', '.'))
    except:
        rendita_catastale = 0
    prima_casa = var_prima_casa.get()
    
    # calcolo del mutuo per aggiornare le etichette e ottenere i costi
    rata, anticipo, costi_irrecuperabili, costo_annuo_spese, baseline = calcola_mutuo(
        prezzo_casa=prezzo_casa,
        tasso=tasso,
        anni=anni,
        percentuale=percentuale,
        rendita_catastale=rendita_catastale,
        prima_casa=prima_casa,
        agenzia=var_agenzia.get()
    )
    etichetta_rata.config(text=f"Rata Mensile Mutuo: {rata:.2f}€", foreground="green")
    etichetta_anticipo.config(text=f"Anticipo Totale Mutuo: {int(anticipo)}€", foreground="green")
    etichetta_costi.config(text=f"Costi irrecuperabili Mutuo: {int(costi_irrecuperabili)}€", foreground="green")
    # se è presente un dato in "Prezzo Affitto", esegui i calcoli per il grafico
    affitto_testo = ingresso_affitto.get().strip()
    if affitto_testo != "":
        try:
            affitto_annuo = float(affitto_testo.replace(',', '.')) * 12
        except ValueError:
            return
        costo_mutuo = [baseline]
        anni_lista = [0]
        costo_affitto = [0]
        for i in range(anni):
            anni_lista.append(i+1)
        totale_pagato = 0
        for _ in range(anni):
            totale_pagato += affitto_annuo
            costo_affitto.append(totale_pagato)
            affitto_annuo *= (1 + inflazione)
        valore_aggiornato = baseline
        for i in range(len(anni_lista)):
            if not i:
                continue
            ris = calcola_quota_interessi(prezzo_casa * percentuale / 100, tasso, anni, anni_lista[i])
            # detrazioni del 19% fino a 2582.25 euro annui di imponibile, se è prima casa
            # https://www.agenziaentrate.gov.it/portale/in-cosa-consiste-mutui-ristrutturazioni-edilizie
            if prima_casa:
                if ris['interessi'] > 2582.25:
                    interessi = ris['interessi'] - 2582.25 * 0.19
                else:
                    interessi = ris['interessi'] * 0.81
            else:
                interessi = ris['interessi']
            valore_aggiornato += interessi + costo_annuo_spese + 170*prezzo_casa/100000 * 0.81
            costo_mutuo.append(valore_aggiornato)
            if not prima_casa:
                costo_mutuo[i] += rendita_catastale * 1.05 * 160 * 0.009


        #----------- seziona grafico -------------

        asse.clear()
        asse.plot(anni_lista, costo_mutuo, label="Costi irrecuperabili (Mutuo)", color="green")
        asse.plot(anni_lista, costo_affitto, label="Costi irrecuperabili (Affitto)", color="blue")
        mutuo = np.array(costo_mutuo)
        affitto = np.array(costo_affitto)
        anni = np.array(anni_lista)
        diff = mutuo - affitto
        indices = np.where(np.diff(np.sign(diff)) != 0)[0]
        
        intercette = []
        for i in indices:
            x0, x1 = anni[i], anni[i+1]
            y0_mutuo, y1_mutuo = mutuo[i], mutuo[i+1]
            y0_affitto, y1_affitto = affitto[i], affitto[i+1]
            m_mutuo = (y1_mutuo - y0_mutuo) / (x1 - x0)
            m_affitto = (y1_affitto - y0_affitto) / (x1 - x0)
            if m_mutuo != m_affitto:
                x_int = x0 + (y0_affitto - y0_mutuo) / (m_mutuo - m_affitto)
                y_int = y0_mutuo + m_mutuo * (x_int - x0)
                parte_intera, parte_decimale = str(x_int).split('.')
                parte_decimale = float('0.' + parte_decimale)
                if parte_decimale == 0:
                    scritta = f"{int(parte_intera)} anno" if int(parte_intera) == 1 else f"{int(parte_intera)} anni"
                else:
                    giorni = int(parte_decimale * 365)
                    if giorni == 0:
                        scritta = f"{int(parte_intera)} anni"
                    elif int(parte_intera) == 0:
                        scritta = f"{giorni} giorni"
                    elif int(parte_intera) == 1:
                        scritta = f"1 anno e {giorni} giorni"
                    else:
                        scritta = f"{int(parte_intera)} anni e {giorni} giorni"
                intercette.append(scritta)
                asse.plot(x_int, y_int, 'ko', markersize=6)
                asse.annotate(
                    scritta,                     
                    xy=(x_int, y_int),           
                    xytext=(-20, 15),             
                    textcoords='offset points',  
                    ha='left',                   
                    va='bottom',                 
                    fontsize=15,                 
                    color='black',               
                    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.4)
                )
        asse.set_title("Confronto: Costi irrecuperabili Mutuo vs Affitto")
        asse.set_xlabel("Anni")
        asse.set_ylabel("Euro")
        asse.legend()
        asse.set_ylim(bottom=0)
        asse.set_xlim(left=0)
        tela.draw()
        
        if intercette:
            msg = "Il mutuo ti conviene se lo tieni per almeno " + ", ".join(intercette)
            msg += ".\nSe pensi di chiuderlo prima, resta in affitto."
        else:
            msg = "Ti conviene stare in affitto."

        etichetta_intercetta.config(text=msg, foreground="green")

    else:
        etichetta_intercetta.config(text="")
def toggle_inflazione():
    for widget in placeholder_frame.winfo_children():
        widget.destroy()
    if var_inflazione.get():
        inflazione_label = ttk.Label(placeholder_frame, text="Inflazione annua media (%):")
        inflazione_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        global inflazione_entry
        inflazione_entry = ttk.Entry(placeholder_frame)
        inflazione_entry.insert(0, "2")
        inflazione_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    else:
        ttk.Label(placeholder_frame, text="").grid(row=0, column=0)

#--------------------------------

root = ThemedTk(theme="arc")
root.title("Calcolatore Mutuo e Affitto")
root.geometry("1260x790")
contenitore = ttk.Frame(root, padding=20)
contenitore.grid(row=0, column=0, sticky="nsew")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
contenitore.columnconfigure(0, weight=1)
contenitore.columnconfigure(1, weight=6)
contenitore.rowconfigure(0, weight=1)

frame_sinistra = ttk.Frame(contenitore)
frame_sinistra.grid(row=0, column=0, sticky="nsew", padx=(0,10))
frame_sinistra.columnconfigure(0, weight=1)
frame_affitto = ttk.LabelFrame(frame_sinistra, text="Dati affitto", padding=10)
frame_affitto.grid(row=0, column=0, sticky="ew", pady=(0,10))
frame_affitto.columnconfigure(1, weight=1)

ttk.Label(frame_affitto, text="Affitto Mensile (€):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ingresso_affitto = ttk.Entry(frame_affitto)
ingresso_affitto.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

frame_mutuo = ttk.LabelFrame(frame_sinistra, text="Sezione Mutuo", padding=10)
frame_mutuo.grid(row=1, column=0, sticky="nsew")
frame_mutuo.columnconfigure(1, weight=1)

ttk.Label(frame_mutuo, text="Prezzo Casa (€):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ingresso_casa = ttk.Entry(frame_mutuo)
ingresso_casa.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame_mutuo, text="TAN mutuo (%):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
ingresso_tasso = ttk.Entry(frame_mutuo)
ingresso_tasso.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame_mutuo, text="Durata Mutuo (Anni):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
ingresso_anni = ttk.Entry(frame_mutuo)
ingresso_anni.insert(0, "20")
ingresso_anni.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame_mutuo, text="Percentuale Mutuo (%):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
ingresso_percentuale = ttk.Entry(frame_mutuo)
ingresso_percentuale.insert(0, "80")
ingresso_percentuale.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame_mutuo, text="Rendita catastale (€):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
ingresso_rendita = ttk.Entry(frame_mutuo)
ingresso_rendita.insert(0, "490")
ingresso_rendita.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

var_prima_casa = tk.BooleanVar(value=True)
var_agenzia = tk.BooleanVar(value=True)
var_inflazione = tk.BooleanVar(value=True)

ttk.Checkbutton(frame_mutuo, text="Prima Casa", variable=var_prima_casa).grid(
    row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

ttk.Checkbutton(frame_mutuo, text="Intermediazione agenzia", variable=var_agenzia).grid(
    row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")

ttk.Checkbutton(frame_mutuo, text="Rivaluta l'affitto per l'inflazione", variable=var_inflazione, command=lambda: toggle_inflazione()).grid(
    row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

placeholder_frame = ttk.Frame(frame_mutuo)
placeholder_frame.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

inflazione_entry = None
toggle_inflazione()

ttk.Button(frame_mutuo, text="Calcola", command=lambda: calcola()).grid(
    row=9, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

frame_risultato = ttk.Frame(frame_mutuo)
frame_risultato.grid(row=10, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

etichetta_rata = ttk.Label(frame_risultato, text="Rata mensile: ")
etichetta_rata.pack(pady=5, fill="x")

etichetta_anticipo = ttk.Label(frame_risultato, text="Anticipo totale mutuo: ")
etichetta_anticipo.pack(pady=5, fill="x")

etichetta_costi = ttk.Label(frame_risultato, text="Costi irrecuperabili mutuo: ")
etichetta_costi.pack(pady=5, fill="x")
etichetta_intercetta = ttk.Label(frame_risultato, text="")
etichetta_intercetta.pack(pady=5, fill="x")

# sezione di destra, il grafico all'inizio è vuoto
frame_destra = ttk.Frame(contenitore)
frame_destra.grid(row=0, column=1, sticky="nsew")
frame_destra.columnconfigure(0, weight=1)
frame_destra.rowconfigure(0, weight=1)
figura = Figure(figsize=(7,5), dpi=100)
asse = figura.add_subplot(111)
asse.set_title("Inserisci anche l'affitto per mostrare il grafico")
asse.set_ylim(bottom=0)
tela = FigureCanvasTkAgg(figura, master=frame_destra)
tela.draw()
tela.get_tk_widget().grid(row=0, column=0, sticky="nsew")
root.mainloop()