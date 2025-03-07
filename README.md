🏡 Mutuo vs Affitto 💸
===================
Tool python leggerissimo, completo e user-friendly che dà una risposta definitiva (almeno dal punto di vista finanziario) alla domanda "conviene fare il mutuo o stare in affitto?", basandosi sull'analisi dei **costi irrecuperabili** di entrambe le soluzioni.
### Cosa sono i costi irrecuperabili?

Sono tutti quei costi che, una volta sostenuti, non si vanno a sommare al proprio patrimonio personale netto. (es. parcella notaio, IMU, affitto mensile, ecc.)

### Cosa NON sono i costi irrecuperabili?
Il rimborso di un prestito (escludendo la parte degli interessi) ad esempio non è un costo irrecuperabile, perchè va ad aumentare il nostro patrimonio netto, è da vedere più come un'accantonamento.
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

Affitto:
- Affitto
- Aumento del canone di affitto per l'inflazione
* * *

# 📷 Screenshots
![Interfaccia grafica (GUI) 1](images/imm1.png)

![Interfaccia grafica (GUI) 2](/images/imm2.png)


# 🛠️ Installazione locale (richiede Git)

## Clona il repository:

    git clone https://github.com/davide-sagona/Mutuo-vs-Affitto.git
    cd Mutuo-vs-Affitto
## Crea un ambiente virtuale python
### Windows 🪟🪟
##### Apri il CMD ed esegui:
    python -m venv ambiente_mutuovsaffitto
    ambiente_mutuovsaffitto\Scripts\activate.bat
    pip install -r requirements.txt

### Linux/MacOS 🐧🍏
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

# Versione Web (no installazione)
### Dato che al momento non accetto donazioni, se vuoi supportare gratuitamente i prossimi progetti disattiva l'AdBlocker, ma solo se non ti è troppo di disturbo. Grazie e buon utilizzo :)
Ecco il sito: [Mutuo vs Affitto Web](contifinanziari.pythonanywhere.com)

***
📜 Licenza
----------

MIT License - Copyright (c) 2025 Davide Sagona

[![Versione](https://img.shields.io/badge/Versione-0.7_beta-green)](https://github.com/davidesagona/Mutuo-vs-Affitto) [![Licenza](https://img.shields.io/badge/Licenza-MIT-blue)](LICENSE)
