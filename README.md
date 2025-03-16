🏡💸 Mutuo vs Affitto, in Italia 🇮🇹
===================
Un tool python leggerissimo, completo e user-friendly che dà una risposta definitiva (almeno dal punto di vista finanziario) alla domanda "in Italia, conviene fare il mutuo o stare in affitto?", basandosi sull'analisi dei **costi irrecuperabili** di entrambe le soluzioni.
### Cosa sono i costi irrecuperabili?

Sono tutti quei costi che, una volta sostenuti, non si vanno a sommare al proprio patrimonio personale netto. (es. parcella notaio, IMU, affitto mensile, ecc.)

### Cosa NON sono i costi irrecuperabili?
Il rimborso di un prestito (escludendo la parte degli interessi) ad esempio non è un costo irrecuperabile, perchè va ad aumentare il nostro patrimonio netto, è da vedere più come un'accantonamento.
### Esempio pratico:
Gino paga 500€ al mese di affitto per 1 anno, alla fine avrà un patrimonio netto di -6000€. Andrea compra un orologio da 30000€ e lo paga in 1 anno a rate: ogni rata è 3000 euro, di cui 500€ sono interessi. Ipotizzando l'orologio abbia mantenuto il suo valore, dopo aver pagato le rate, avrà anche lui un patrimonio netto di -6000€ nonostante ne abbia pagati 36000! Questo perchè adesso ha anche un bene che vale 30000€ e che può vendere, infatti le uniche spese irrecuperabili che ha sostenuto sono state quelle relative agli interessi.
### Quali sono i costi irrecuperabili dell'affitto?
Oltre ovviamente alle bollette e alle spese ordinarie (che non considererò, dato che sono uguali sia per la casa di proprietà, che per una in affitto) l'unico costo irrecuperabile è l'affitto stesso.

### Quali sono i costi irrecuperabili del comprare casa?
Ce ne sono numerosi e qui sotto darò un accenno, per sapere quanto e come incidono **leggi il codice e i relativi commenti**.

#### Il tool tiene conto delle seguenti voci (comprese detrazioni e IVA ove applicabili):

Acquisto casa e/o Mutuo:
- Interessi sul capitale del mutuo
- Assicurazione sulla casa obbligatoria per legge
- Spese di istruttoria mutuo
- Imposta sostitutiva mutuo
- Altre imposte sul mutuo varie ed eventuali
- Imposta di registro immobile
- Spese di intermediazione dell'agenzia
- Imposte ipotecarie e catastali
- Parcella del notaio
- IMU (in affitto non si pagherebbe)
- Spese straordinarie casa (in affitto si pagano solo quelle ordinarie)
- (Solo versione Web) **EVENTUALI** mancati rendimenti finanziari derivanti dal fatto di aver comprato casa (ed eventualmente fatto il mutuo), non potendo investire il capitale impegnato o speso

Affitto:
- Affitto
- Aumento del canone di affitto per l'inflazione
- (Solo versione Web) **EVENTUALI** mancati rendimenti finanziari derivanti dal fatto di pagare un affitto maggiore rispetto alla rata del mutuo, non potendo investire il risparmio mensile che ne deriva
* * *

# Versione Web (no installazione)
## Ultimo aggiornamento: 16/03/2025
### Buon utilizzo :)

Ecco il sito: [Mutuo vs Affitto Web](https://contifinanziari.pythonanywhere.com)

***
# 📷 Screenshots della versione locale
![Interfaccia grafica (GUI) 1](/immagini/imm1.png)

![Interfaccia grafica (GUI) 2](/immagini/imm2.png)

***
# 🛠️ Installazione locale (richiede Git)
## Ultimo aggiornamento: 13/03/2025

## Clona il repository e crea un ambiente virtuale:
### Windows 🪟🪟
##### Apri il CMD ed esegui:
    git clone https://github.com/davide-sagona/Mutuo-vs-Affitto.git
    cd Mutuo-vs-Affitto
    python -m venv ambiente_mutuovsaffitto
    ambiente_mutuovsaffitto\Scripts\activate.bat
    pip install -r requirements.txt

### Linux/MacOS 🐧🍏
    git clone https://github.com/davide-sagona/Mutuo-vs-Affitto.git
    cd Mutuo-vs-Affitto
    python3 -m venv ambiente_mutuovsaffitto
    source ambiente_mutuovsaffitto/bin/activate
    pip install -r requirements.txt

### Eventuali comandi aggiuntivi necessari:
#### Per Ubuntu/Debian (linux)
    sudo apt-get update && sudo apt-get install python3-tk 

#### Per Fedora (linux)
    sudo dnf install python3-tkinter
    
## Infine, esegui il programma 🚀
### Windows 🪟🪟
    python main.py
    
### Linux/MacOS 🐧🍏
    python3 main.py

***
📜 Licenza
----------

MIT License - Copyright (c) 2025 Davide Sagona

[![Versione](https://img.shields.io/badge/Versione-0.7_beta-green)](https://github.com/davidesagona/Mutuo-vs-Affitto) [![Licenza](https://img.shields.io/badge/Licenza-MIT-blue)](LICENSE)
