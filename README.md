# Project moved / Progetto evoluto

This project has evolved into MolinaCrypto Web3 Shield.

New repository:
https://github.com/TUO-USERNAME/molinacrypto-web3-shield

MolinaCrypto Wallet Safety Check was the first experimental version focused on public wallet/address checks. The new Web3 Shield project expands the concept to wallet checks, suspicious Web3 links, EVM smart contracts and signature/approval risk checks.

# MolinaCrypto Wallet Safety Check

**MolinaCrypto Wallet Safety Check** is an open source desktop tool designed to inspect public Bitcoin and Ethereum/Web3 addresses without requesting seed phrases, private keys or wallet connection.

**MolinaCrypto Wallet Safety Check** è un tool desktop open source pensato per controllare indirizzi pubblici Bitcoin ed Ethereum/Web3 senza richiedere seed phrase, private key o collegamento del wallet.

Project connected to: https://www.molinacrypto.eu

---

## English

### Main features

- Public Bitcoin address check via mempool.space API
- BTC confirmed balance, unconfirmed/mempool balance, received/spent amount and transaction count
- Recent Bitcoin transactions
- Bitcoin network snapshot and recommended fees
- Wallet Hygiene Score
- Ethereum/EVM address format recognition
- Useful links to Etherscan, Revoke.cash, BaseScan, PolygonScan, Arbiscan and Optimism explorer
- Wallet security checklist
- TXT report export
- Italian / English interface
- No wallet custody
- No seed phrase input
- No private key input
- No transaction signing

### Important safety note

This tool does **not** create wallets, store funds, connect to wallets, sign transactions, manage private keys or ask for seed phrases.

Never enter a seed phrase, private key, password or recovery phrase into this or any other public tool.

### Windows portable download

Download the latest Windows portable ZIP archive from the **Releases** section:

`MolinaCryptoWalletSafetyCheck-windows-x86_64-v0.4.zip`

After downloading:

1. Extract the ZIP archive.
2. Open the extracted folder.
3. Double click:

`MolinaCryptoWalletSafetyCheck.exe`

No installation is required.

### Windows security warning

On some Windows systems, Microsoft Defender SmartScreen may display a warning because the executable is unsigned and not widely downloaded yet.

If you trust the source and downloaded the file from the official GitHub release page, you can start it by clicking:

1. **More info**
2. **Run anyway**

This warning does not necessarily mean that the program is malicious. It usually appears for new or unsigned applications. Users should always download the file only from the official repository/release page and verify that the project source code is available.

### Linux portable download

Download the latest Linux portable archive from the **Releases** section:

`MolinaCryptoWalletSafetyCheck-linux-x86_64-v0.4.tar.gz`

After downloading and extracting the archive:

```bash
cd MolinaCryptoWalletSafetyCheck-linux-x86_64
chmod +x avvia.sh
./avvia.sh
```

On some Linux file managers, you can also double click avvia.sh and choose Run.

Run from source

### Requirements:

Python 3
Tkinter
Internet connection

On Debian/Ubuntu/Linux Mint systems, Tkinter can usually be installed with:

sudo apt install python3-tk

Run:

`python3 MolinaCryptoWalletSafetyCheck.py`
Data sources and external resources

The application uses public data and public web resources, including:

mempool.space
Etherscan
Revoke.cash
BaseScan
PolygonScan
Arbiscan
Optimism Explorer
Wallet Hygiene Score

The Wallet Hygiene Score is an informational indicator based on public data and basic safety heuristics.

For Bitcoin addresses, it considers elements such as:

address reuse
confirmed balance
unconfirmed mempool activity
current Bitcoin network fees

For Ethereum/EVM addresses, the current version provides an educational safety score and directs the user to public explorers and approval-checking tools.

The score is not a guarantee of safety and must not be interpreted as financial, legal, tax or cybersecurity advice.

## Italiano
Funzioni principali
Controllo di indirizzi pubblici Bitcoin tramite API pubbliche mempool.space
Saldo BTC confermato, saldo non confermato/mempool, totale ricevuto/speso e numero transazioni
Transazioni Bitcoin recenti
Snapshot rete Bitcoin e fee consigliate
Wallet Hygiene Score
Riconoscimento formato indirizzi Ethereum/EVM
Link utili a Etherscan, Revoke.cash, BaseScan, PolygonScan, Arbiscan e Optimism explorer
Checklist sicurezza wallet
Esportazione report TXT
Interfaccia Italiano / English
Nessuna custodia wallet
Nessun inserimento seed phrase
Nessun inserimento private key
Nessuna firma transazioni
Nota importante di sicurezza

Questo tool non crea wallet, non custodisce fondi, non collega wallet, non firma transazioni, non gestisce private key e non chiede seed phrase.

Non inserire mai seed phrase, private key, password o recovery phrase in questo o in qualsiasi altro tool pubblico.

### Download Windows portable

Scaricare l’archivio ZIP Windows portable più recente dalla sezione Releases:

`MolinaCryptoWalletSafetyCheck-windows-x86_64-v0.4.zip`

Dopo il download:

1. Estrarre l’archivio ZIP.
2. Aprire la cartella estratta.
3. Fare doppio click su:

`MolinaCryptoWalletSafetyCheck.exe`

Non è richiesta installazione.

### Avviso di sicurezza Windows

Su alcuni sistemi Windows, Microsoft Defender SmartScreen potrebbe mostrare un avviso perché l’eseguibile non è firmato digitalmente e non è ancora molto scaricato.

Se ti fidi della fonte e hai scaricato il file dalla pagina ufficiale delle release GitHub, puoi avviarlo cliccando:

### Ulteriori informazioni
Esegui comunque

Questo avviso non significa necessariamente che il programma sia malevolo. Spesso compare per applicazioni nuove o non firmate. È comunque consigliato scaricare il file solo dal repository/release ufficiale e verificare che il codice sorgente del progetto sia disponibile.

## Download Linux portable

Scaricare l’archivio Linux portable più recente dalla sezione Releases:

`MolinaCryptoWalletSafetyCheck-linux-x86_64-v0.4.tar.gz`

Dopo aver scaricato ed estratto l’archivio:

```Bash
cd MolinaCryptoWalletSafetyCheck-linux-x86_64
chmod +x avvia.sh
./avvia.sh
```

Su alcuni file manager Linux è possibile fare doppio click su avvia.sh e scegliere Esegui.

### Avvio da sorgente

Requisiti:

Python 3
Tkinter
connessione Internet

Su Debian/Ubuntu/Linux Mint, Tkinter può normalmente essere installato con:

sudo apt install python3-tk

Avvio:

python3 MolinaCryptoWalletSafetyCheck.py
Fonti dati e risorse esterne

Il programma usa dati pubblici e risorse web pubbliche, tra cui:

mempool.space
Etherscan
Revoke.cash
BaseScan
PolygonScan
Arbiscan
Optimism Explorer
Wallet Hygiene Score

Il Wallet Hygiene Score è un indicatore informativo basato su dati pubblici e semplici criteri di igiene/sicurezza.

Per gli indirizzi Bitcoin considera elementi come:

riutilizzo dell’indirizzo
saldo confermato
attività non confermata in mempool
fee correnti della rete Bitcoin

Per gli indirizzi Ethereum/EVM, nella versione attuale fornisce uno score educativo e indirizza l’utente verso explorer pubblici e strumenti di controllo approvals.

Lo score non è una garanzia di sicurezza e non deve essere interpretato come consulenza finanziaria, legale, fiscale o professionale di cybersecurity.

### Disclaimer

The information displayed by this tool is for educational and informational purposes only.

This software does not provide financial, investment, tax, legal or professional cybersecurity advice. Users are responsible for their own decisions and should verify critical information using official sources and qualified professionals when needed.

Le informazioni mostrate da questo tool hanno finalità esclusivamente educative e informative.

Il software non fornisce consulenza finanziaria, di investimento, fiscale, legale o professionale di cybersecurity. L’utente resta responsabile delle proprie decisioni e dovrebbe verificare le informazioni critiche tramite fonti ufficiali e professionisti qualificati quando necessario.

### Author / Autore

© 2026 Paolo Molina
Website / Sito: https://www.molinacrypto.eu

License / Licenza

Distributed under the MIT License. See LICENSE.

Distribuito con licenza MIT. Vedi file LICENSE.
