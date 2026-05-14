import json
import re
import threading
import urllib.request
import urllib.parse
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


APP_TITLE = "molinacrypto.eu · Wallet Safety Check"
APP_VERSION = "0.4"
AUTHOR = "Paolo Molina"

URLS = {
    "site": "https://www.molinacrypto.eu",
    "resources": "https://www.molinacrypto.eu/risorse.html",
    "mempool_fees": "https://mempool.space/api/v1/fees/recommended",
    "mempool_stats": "https://mempool.space/api/mempool",
    "mempool_height": "https://mempool.space/api/blocks/tip/height",
}

BTC_PATTERNS = [
    re.compile(r"^(bc1)[a-z0-9]{25,90}$", re.IGNORECASE),
    re.compile(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"),
]

ETH_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")


LANG = {
    "it": {
        "language_label": "Lingua",
        "language_italian": "Italiano",
        "language_english": "English",

        "header_subtitle": "Wallet Safety Check · controlla indirizzi pubblici senza seed phrase",
        "input_title": "Inserisci un indirizzo pubblico Bitcoin o Ethereum",
        "input_warning": "Non inserire mai seed phrase, private key, password o dati personali. Questo tool lavora solo su indirizzi pubblici.",

        "btn_analyze": "Analizza",
        "btn_open_explorer": "Apri explorer",
        "btn_report": "Report .txt",
        "btn_clear": "Pulisci",
        "btn_site": "Apri molinacrypto.eu",
        "btn_resources": "Risorse",
        "btn_refresh_btc": "Aggiorna rete BTC",

        "tab_result": "Risultato",
        "tab_transactions": "Transazioni BTC",
        "tab_checklist": "Checklist sicurezza",
        "tab_links": "Link utili",
        "tab_network": "Bitcoin network",

        "status_ready": "Pronto.",
        "status_clean": "Pulito.",
        "status_loading_network": "Caricamento dati Bitcoin network...",
        "status_network_loaded": "Dati Bitcoin network caricati.",
        "status_network_loaded_warnings": "Dati rete caricati con {count} avvisi.",
        "status_btc_loading": "Analisi indirizzo Bitcoin in corso...",
        "status_btc_done": "Analisi Bitcoin completata.",
        "status_btc_error": "Errore analisi Bitcoin.",
        "status_eth_done": "Analisi Ethereum/Web3 completata.",
        "status_unknown": "Formato non riconosciuto.",
        "status_language_changed": "Lingua impostata: Italiano.",

        "popup_missing_title": "Indirizzo mancante",
        "popup_missing_msg": "Inserisci un indirizzo pubblico BTC o ETH.",
        "popup_no_address_title": "Nessun indirizzo",
        "popup_no_address_msg": "Inserisci o analizza prima un indirizzo.",
        "popup_unknown_title": "Formato non riconosciuto",
        "popup_unknown_msg": "Non posso generare un explorer per questo formato.",
        "popup_report_unavailable_title": "Report non disponibile",
        "popup_report_unavailable_msg": "Analizza prima un indirizzo.",
        "popup_report_saved_title": "Report salvato",
        "popup_report_saved_msg": "Report salvato correttamente:\n{path}",
        "popup_report_error_title": "Errore salvataggio",
        "popup_report_error_msg": "Non sono riuscito a salvare il report:\n{error}",

        "tx_date": "Data",
        "tx_type": "Movimento",
        "tx_amount": "Importo netto",
        "tx_fee": "Fee",
        "tx_status": "Stato",
        "tx_txid": "TXID",
        "tx_received": "Ricevuto",
        "tx_spent": "Speso",
        "tx_neutral": "Neutro",
        "tx_confirmed": "Confermata",
        "tx_unconfirmed": "Non confermata",
        "tx_in_mempool": "In mempool",
        "tx_none": "Nessuna transazione recente trovata",

        "default_result": (
            "Inserisci un indirizzo pubblico Bitcoin o Ethereum e premi Analizza.\n\n"
            "Questo programma non crea wallet, non custodisce fondi, non firma transazioni "
            "e non richiede seed phrase o private key.\n\n"
            "Uso consigliato:\n"
            "- controllare il formato base di un indirizzo pubblico;\n"
            "- leggere saldo e attività pubblica di un indirizzo Bitcoin;\n"
            "- aprire rapidamente explorer e strumenti di sicurezza;\n"
            "- consultare fee Bitcoin e note di igiene wallet;\n"
            "- generare un piccolo report .txt."
        ),

        "default_links": (
            "I link utili saranno generati dopo l’analisi di un indirizzo.\n\n"
            "Nota: per Ethereum/Web3 il tool non collega il wallet. Ti indirizza solo verso pagine pubbliche "
            "come explorer e strumenti di controllo autorizzazioni."
        ),

        "network_loading": "Caricamento dati Bitcoin network...",

        "checklist": (
            "Checklist sicurezza wallet\n\n"
            "1. Seed phrase\n"
            "- Non inserirla mai in siti, app, form, bot Telegram o strumenti non verificati.\n"
            "- Non fotografarla e non salvarla in cloud.\n"
            "- Chi ha la seed phrase controlla i fondi.\n\n"
            "2. Indirizzi pubblici\n"
            "- Un indirizzo pubblico può essere condiviso per ricevere fondi.\n"
            "- Però rivela attività e movimenti sulla blockchain.\n"
            "- Per privacy, evita di riutilizzare sempre lo stesso indirizzo quando possibile.\n\n"
            "3. Phishing e fake wallet\n"
            "- Scarica wallet solo dai siti ufficiali.\n"
            "- Controlla sempre dominio, estensioni browser e link sponsorizzati.\n"
            "- Diffida da messaggi urgenti, airdrop, assistenza finta e richieste di firma.\n\n"
            "4. Ethereum/Web3 approvals\n"
            "- Alcuni smart contract possono ricevere autorizzazioni a spendere token.\n"
            "- Le approval illimitate possono essere rischiose se concesse a contratti malevoli o compromessi.\n"
            "- Controlla periodicamente le autorizzazioni su strumenti noti come Revoke.cash o explorer ufficiali.\n\n"
            "5. Bitcoin fee\n"
            "- Prima di inviare BTC, controlla le fee di rete.\n"
            "- Se la transazione non è urgente, spesso conviene evitare momenti di congestione.\n"
            "- Fee troppo basse possono rallentare la conferma."
        ),

        "fee_unknown": "Fee non interpretabili al momento.",
        "fee_low": "Le fee sembrano basse. Se devi inviare BTC, la rete appare relativamente conveniente.",
        "fee_medium": "Le fee sembrano moderate. Per transazioni non urgenti puoi valutare se attendere.",
        "fee_high": "Le fee sembrano alte. Se la transazione non è urgente, valuta di aspettare una fase meno congestionata.",
        "fee_very_high": "Le fee sembrano molto alte. Per movimenti non urgenti è prudente aspettare o valutare con attenzione.",

        "report_default_name": "MolinaCrypto_Wallet_Safety_Check_Report.txt",
        "score_title": "Wallet Hygiene Score",
        "score_level_low": "Rischio basso",
        "score_level_medium": "Rischio medio",
        "score_level_high": "Rischio alto",
        "score_points": "Punteggio",
        "score_reasons": "Motivi principali",
        "report_header_note": (
            "Nota: report informativo. Non è consulenza finanziaria, fiscale, legale o di cybersecurity professionale.\n"
            "Il tool non gestisce wallet, seed phrase, private key o firma di transazioni.\n"
        ),
    },

    "en": {
        "language_label": "Language",
        "language_italian": "Italiano",
        "language_english": "English",

        "header_subtitle": "Wallet Safety Check · inspect public addresses without seed phrases",
        "input_title": "Enter a public Bitcoin or Ethereum address",
        "input_warning": "Never enter seed phrases, private keys, passwords or personal data. This tool only works with public addresses.",

        "btn_analyze": "Analyze",
        "btn_open_explorer": "Open explorer",
        "btn_report": "Report .txt",
        "btn_clear": "Clear",
        "btn_site": "Open molinacrypto.eu",
        "btn_resources": "Resources",
        "btn_refresh_btc": "Refresh BTC network",

        "tab_result": "Result",
        "tab_transactions": "BTC transactions",
        "tab_checklist": "Security checklist",
        "tab_links": "Useful links",
        "tab_network": "Bitcoin network",

        "status_ready": "Ready.",
        "status_clean": "Cleared.",
        "status_loading_network": "Loading Bitcoin network data...",
        "status_network_loaded": "Bitcoin network data loaded.",
        "status_network_loaded_warnings": "Network data loaded with {count} warnings.",
        "status_btc_loading": "Bitcoin address analysis in progress...",
        "status_btc_done": "Bitcoin analysis completed.",
        "status_btc_error": "Bitcoin analysis error.",
        "status_eth_done": "Ethereum/Web3 analysis completed.",
        "status_unknown": "Unrecognized format.",
        "status_language_changed": "Language set: English.",

        "popup_missing_title": "Missing address",
        "popup_missing_msg": "Enter a public BTC or ETH address.",
        "popup_no_address_title": "No address",
        "popup_no_address_msg": "Enter or analyze an address first.",
        "popup_unknown_title": "Unrecognized format",
        "popup_unknown_msg": "I cannot generate an explorer link for this format.",
        "popup_report_unavailable_title": "Report not available",
        "popup_report_unavailable_msg": "Analyze an address first.",
        "popup_report_saved_title": "Report saved",
        "popup_report_saved_msg": "Report saved successfully:\n{path}",
        "popup_report_error_title": "Save error",
        "popup_report_error_msg": "I could not save the report:\n{error}",

        "tx_date": "Date",
        "tx_type": "Movement",
        "tx_amount": "Net amount",
        "tx_fee": "Fee",
        "tx_status": "Status",
        "tx_txid": "TXID",
        "tx_received": "Received",
        "tx_spent": "Spent",
        "tx_neutral": "Neutral",
        "tx_confirmed": "Confirmed",
        "tx_unconfirmed": "Unconfirmed",
        "tx_in_mempool": "In mempool",
        "tx_none": "No recent transactions found",

        "default_result": (
            "Enter a public Bitcoin or Ethereum address and press Analyze.\n\n"
            "This program does not create wallets, does not custody funds, does not sign transactions "
            "and does not ask for seed phrases or private keys.\n\n"
            "Recommended use:\n"
            "- check the basic format of a public address;\n"
            "- read public balance and activity for a Bitcoin address;\n"
            "- quickly open explorers and security tools;\n"
            "- check Bitcoin fees and wallet hygiene notes;\n"
            "- generate a small .txt report."
        ),

        "default_links": (
            "Useful links will be generated after analyzing an address.\n\n"
            "Note: for Ethereum/Web3, the tool does not connect to your wallet. It only points you to public pages "
            "such as explorers and approval-checking tools."
        ),

        "network_loading": "Loading Bitcoin network data...",

        "checklist": (
            "Wallet security checklist\n\n"
            "1. Seed phrase\n"
            "- Never enter it into websites, apps, forms, Telegram bots or unverified tools.\n"
            "- Do not photograph it and do not store it in the cloud.\n"
            "- Whoever has the seed phrase controls the funds.\n\n"
            "2. Public addresses\n"
            "- A public address can be shared to receive funds.\n"
            "- However, it reveals blockchain activity and movements.\n"
            "- For privacy, avoid reusing the same address whenever possible.\n\n"
            "3. Phishing and fake wallets\n"
            "- Download wallets only from official websites.\n"
            "- Always check domains, browser extensions and sponsored links.\n"
            "- Be wary of urgent messages, airdrops, fake support and unclear signing requests.\n\n"
            "4. Ethereum/Web3 approvals\n"
            "- Some smart contracts can receive permissions to spend tokens.\n"
            "- Unlimited approvals may be risky if granted to malicious or compromised contracts.\n"
            "- Periodically check permissions with known tools such as Revoke.cash or official explorers.\n\n"
            "5. Bitcoin fees\n"
            "- Before sending BTC, check current network fees.\n"
            "- If the transaction is not urgent, it may be better to avoid congested periods.\n"
            "- Very low fees may delay confirmation."
        ),

        "fee_unknown": "Fees cannot be interpreted at the moment.",
        "fee_low": "Fees appear low. If you need to send BTC, the network currently looks relatively convenient.",
        "fee_medium": "Fees appear moderate. For non-urgent transactions, you may consider waiting.",
        "fee_high": "Fees appear high. If the transaction is not urgent, consider waiting for a less congested period.",
        "fee_very_high": "Fees appear very high. For non-urgent movements, it is prudent to wait or evaluate carefully.",

        "report_default_name": "MolinaCrypto_Wallet_Safety_Check_Report.txt",
        "score_title": "Wallet Hygiene Score",
        "score_level_low": "Low risk",
        "score_level_medium": "Medium risk",
        "score_level_high": "High risk",
        "score_points": "Score",
        "score_reasons": "Main reasons",
        "report_header_note": (
            "Note: informational report. This is not financial, tax, legal or professional cybersecurity advice.\n"
            "The tool does not manage wallets, seed phrases, private keys or transaction signing.\n"
        ),
    },
}


def fetch_text(url, timeout=15):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MolinaCryptoWalletSafetyCheck/0.3"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_json(url, timeout=15):
    return json.loads(fetch_text(url, timeout=timeout))


def detect_address_type(address):
    address = address.strip()

    if ETH_PATTERN.match(address):
        return "ETH"

    for pattern in BTC_PATTERNS:
        if pattern.match(address):
            return "BTC"

    return "UNKNOWN"


def sats_to_btc(sats):
    try:
        return float(sats) / 100_000_000
    except Exception:
        return 0.0


def fmt_btc_from_sats(sats):
    return f"{sats_to_btc(sats):.8f} BTC"


def fmt_sats(sats):
    try:
        return f"{int(sats):,}".replace(",", ".") + " sats"
    except Exception:
        return "—"


def safe(value, default="—"):
    if value is None:
        return default
    return str(value)


class WalletSafetyCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1120x820")
        self.root.minsize(1040, 760)

        self.bg = "#060e1f"
        self.panel = "#0b1220"
        self.panel2 = "#111827"
        self.text = "#d8e8fa"
        self.muted = "#8099be"
        self.accent = "#1e90ff"
        self.accent2 = "#00cfff"
        self.warn = "#ffb300"
        self.danger = "#ff3d5a"
        self.ok = "#00d4a0"

        self.lang = "it"
        self.language_var = tk.StringVar(value=LANG["it"]["language_italian"])

        self.current_address = ""
        self.current_type = "UNKNOWN"
        self.last_address_data = None
        self.last_txs_data = []
        self.network_data = {}
        self.last_report_text = ""

        self.setup_style()
        self.build_ui()
        self.load_network_snapshot()

    def t(self, key):
        return LANG.get(self.lang, LANG["it"]).get(key, key)

    def setup_style(self):
        self.root.configure(bg=self.bg)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background=self.bg, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=self.panel2,
            foreground=self.text,
            padding=(14, 8)
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.accent)],
            foreground=[("selected", "white")]
        )

        style.configure(
            "Treeview",
            background=self.panel,
            foreground=self.text,
            fieldbackground=self.panel,
            rowheight=30,
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=self.panel2,
            foreground=self.accent2,
            font=("Arial", 10, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", self.accent)],
            foreground=[("selected", "white")]
        )

    def build_ui(self):
        self.build_header()
        self.build_input_area()
        self.build_tabs()
        self.build_footer()

    def build_header(self):
        self.header = tk.Frame(self.root, bg=self.bg)
        self.header.pack(fill="x", padx=16, pady=(14, 8))

        row = tk.Frame(self.header, bg=self.bg)
        row.pack(fill="x")

        logo = tk.Label(
            row,
            text="M",
            bg="#0b3d91",
            fg="white",
            font=("Arial", 24, "bold"),
            width=3,
            height=1,
            relief="solid",
            bd=1
        )
        logo.pack(side="left", padx=(0, 14))

        brand = tk.Frame(row, bg=self.bg)
        brand.pack(side="left", fill="x", expand=True)

        self.brand_title = tk.Label(
            brand,
            text="molinacrypto.eu",
            bg=self.bg,
            fg=self.accent2,
            font=("Arial", 26, "bold")
        )
        self.brand_title.pack(anchor="w")

        self.header_subtitle_label = tk.Label(
            brand,
            text=self.t("header_subtitle"),
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 11)
        )
        self.header_subtitle_label.pack(anchor="w", pady=(2, 0))

        right_box = tk.Frame(row, bg=self.bg)
        right_box.pack(side="right", anchor="ne")

        self.version_label = tk.Label(
            right_box,
            text=f"v{APP_VERSION} · © 2026 {AUTHOR}",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 9)
        )
        self.version_label.pack(anchor="e", pady=(0, 6))

        lang_row = tk.Frame(right_box, bg=self.bg)
        lang_row.pack(anchor="e")

        self.language_label = tk.Label(
            lang_row,
            text=self.t("language_label") + ":",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 9)
        )
        self.language_label.pack(side="left", padx=(0, 6))

        self.language_combo = ttk.Combobox(
            lang_row,
            textvariable=self.language_var,
            values=[self.t("language_italian"), self.t("language_english")],
            state="readonly",
            width=10
        )
        self.language_combo.pack(side="left")
        self.language_combo.bind("<<ComboboxSelected>>", self.on_language_change)

        line = tk.Frame(self.header, bg=self.accent, height=1)
        line.pack(fill="x", pady=(10, 0))

        line2 = tk.Frame(self.header, bg=self.accent2, height=3, width=330)
        line2.pack(anchor="w")

    def build_input_area(self):
        self.input_box = tk.Frame(
            self.root,
            bg=self.panel,
            highlightbackground="#1e90ff",
            highlightthickness=1,
            padx=14,
            pady=12
        )
        self.input_box.pack(fill="x", padx=16, pady=(4, 8))

        self.input_title_label = tk.Label(
            self.input_box,
            text=self.t("input_title"),
            bg=self.panel,
            fg=self.accent2,
            font=("Arial", 13, "bold")
        )
        self.input_title_label.pack(anchor="w")

        self.input_warning_label = tk.Label(
            self.input_box,
            text=self.t("input_warning"),
            bg=self.panel,
            fg=self.warn,
            font=("Arial", 9)
        )
        self.input_warning_label.pack(anchor="w", pady=(4, 8))

        row = tk.Frame(self.input_box, bg=self.panel)
        row.pack(fill="x")

        self.address_var = tk.StringVar()

        self.address_entry = tk.Entry(
            row,
            textvariable=self.address_var,
            bg="#071021",
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            font=("Arial", 12),
            width=70
        )
        self.address_entry.pack(side="left", fill="x", expand=True, ipady=8)

        self.btn_analyze = self.button(row, self.t("btn_analyze"), self.analyze_address)
        self.btn_analyze.pack(side="left", padx=(8, 0))

        self.btn_open_explorer = self.button(row, self.t("btn_open_explorer"), self.open_current_primary_link)
        self.btn_open_explorer.pack(side="left", padx=(8, 0))

        self.btn_report = self.button(row, self.t("btn_report"), self.export_report)
        self.btn_report.pack(side="left", padx=(8, 0))

        self.btn_clear = self.button(row, self.t("btn_clear"), self.clear_all)
        self.btn_clear.pack(side="left", padx=(8, 0))

    def build_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=(0, 6))

        self.tab_result = self.make_tab(self.t("tab_result"))
        self.tab_transactions = self.make_tab(self.t("tab_transactions"))
        self.tab_checklist = self.make_tab(self.t("tab_checklist"))
        self.tab_links = self.make_tab(self.t("tab_links"))
        self.tab_network = self.make_tab(self.t("tab_network"))

        self.result_text = self.make_text(self.tab_result)
        self.transactions_tree = self.make_transactions_table(self.tab_transactions)
        self.checklist_text = self.make_text(self.tab_checklist)
        self.links_text = self.make_text(self.tab_links)
        self.network_text = self.make_text(self.tab_network)

        self.populate_default_texts()

    def build_footer(self):
        self.footer = tk.Frame(self.root, bg=self.bg)
        self.footer.pack(fill="x", padx=16, pady=(0, 8))

        self.status = tk.Label(
            self.footer,
            text=self.t("status_ready"),
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 9)
        )
        self.status.pack(side="left")

        self.btn_site = self.button(self.footer, self.t("btn_site"), lambda: webbrowser.open(URLS["site"]))
        self.btn_site.pack(side="right")

        self.btn_resources = self.button(self.footer, self.t("btn_resources"), lambda: webbrowser.open(URLS["resources"]))
        self.btn_resources.pack(side="right", padx=(0, 8))

        self.btn_refresh_btc = self.button(self.footer, self.t("btn_refresh_btc"), self.load_network_snapshot)
        self.btn_refresh_btc.pack(side="right", padx=(0, 8))

    def make_tab(self, title):
        frame = tk.Frame(self.tabs, bg=self.bg)
        self.tabs.add(frame, text=title)
        return frame

    def make_text(self, parent):
        text = tk.Text(
            parent,
            bg=self.panel,
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            wrap="word",
            font=("Arial", 11),
            padx=14,
            pady=14
        )
        text.pack(fill="both", expand=True, padx=8, pady=8)
        text.configure(state="disabled")
        return text

    def make_transactions_table(self, parent):
        frame = tk.Frame(parent, bg=self.bg)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        columns = ("date", "type", "amount", "fee", "status", "txid")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        tree.heading("date", text=self.t("tx_date"))
        tree.heading("type", text=self.t("tx_type"))
        tree.heading("amount", text=self.t("tx_amount"))
        tree.heading("fee", text=self.t("tx_fee"))
        tree.heading("status", text=self.t("tx_status"))
        tree.heading("txid", text=self.t("tx_txid"))

        tree.column("date", width=140, anchor="w")
        tree.column("type", width=100, anchor="w")
        tree.column("amount", width=160, anchor="w")
        tree.column("fee", width=120, anchor="w")
        tree.column("status", width=120, anchor="w")
        tree.column("txid", width=360, anchor="w")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)

        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tree.bind("<Double-1>", lambda event: self.open_selected_tx(tree))

        return tree

    def button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#0f766e",
            fg="white",
            activebackground="#14b8a6",
            activeforeground="white",
            relief="flat",
            padx=13,
            pady=7,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )

    def set_text(self, widget, content):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", content)
        widget.configure(state="disabled")

    def clear_transactions_table(self):
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

    def populate_default_texts(self):
        self.set_text(self.result_text, self.t("default_result"))
        self.set_text(self.checklist_text, self.t("checklist"))
        self.set_text(self.links_text, self.t("default_links"))
        self.set_text(self.network_text, self.t("network_loading"))
        self.clear_transactions_table()

    def on_language_change(self, event=None):
        selected = self.language_var.get()

        if selected == LANG["en"]["language_english"]:
            self.lang = "en"
        else:
            self.lang = "it"

        self.refresh_language_ui()

        if self.current_address and self.current_type == "BTC" and self.last_address_data is not None:
            self.render_btc_result(self.current_address, self.last_address_data, self.last_txs_data)
        elif self.current_address and self.current_type == "ETH":
            self.render_eth_result(self.current_address)
        elif self.current_address and self.current_type == "UNKNOWN":
            self.render_unknown_result(self.current_address)
        else:
            self.populate_default_texts()

        self.render_network_snapshot([])
        self.status.config(text=self.t("status_language_changed"))

    def refresh_language_ui(self):
        self.header_subtitle_label.config(text=self.t("header_subtitle"))
        self.language_label.config(text=self.t("language_label") + ":")

        self.language_combo.config(
            values=[self.t("language_italian"), self.t("language_english")]
        )

        if self.lang == "en":
            self.language_var.set(self.t("language_english"))
        else:
            self.language_var.set(self.t("language_italian"))

        self.input_title_label.config(text=self.t("input_title"))
        self.input_warning_label.config(text=self.t("input_warning"))

        self.btn_analyze.config(text=self.t("btn_analyze"))
        self.btn_open_explorer.config(text=self.t("btn_open_explorer"))
        self.btn_report.config(text=self.t("btn_report"))
        self.btn_clear.config(text=self.t("btn_clear"))

        self.btn_site.config(text=self.t("btn_site"))
        self.btn_resources.config(text=self.t("btn_resources"))
        self.btn_refresh_btc.config(text=self.t("btn_refresh_btc"))

        self.tabs.tab(self.tab_result, text=self.t("tab_result"))
        self.tabs.tab(self.tab_transactions, text=self.t("tab_transactions"))
        self.tabs.tab(self.tab_checklist, text=self.t("tab_checklist"))
        self.tabs.tab(self.tab_links, text=self.t("tab_links"))
        self.tabs.tab(self.tab_network, text=self.t("tab_network"))

        self.transactions_tree.heading("date", text=self.t("tx_date"))
        self.transactions_tree.heading("type", text=self.t("tx_type"))
        self.transactions_tree.heading("amount", text=self.t("tx_amount"))
        self.transactions_tree.heading("fee", text=self.t("tx_fee"))
        self.transactions_tree.heading("status", text=self.t("tx_status"))
        self.transactions_tree.heading("txid", text=self.t("tx_txid"))

    def clear_all(self):
        self.address_var.set("")
        self.current_address = ""
        self.current_type = "UNKNOWN"
        self.last_address_data = None
        self.last_txs_data = []
        self.last_report_text = ""
        self.populate_default_texts()
        self.render_network_snapshot([])
        self.status.config(text=self.t("status_clean"))

    def analyze_address(self):
        address = self.address_var.get().strip()

        if not address:
            messagebox.showwarning(self.t("popup_missing_title"), self.t("popup_missing_msg"))
            return

        self.current_address = address
        self.current_type = detect_address_type(address)
        self.last_address_data = None
        self.last_txs_data = []

        if self.current_type == "BTC":
            self.render_loading_btc(address)
            threading.Thread(target=self.load_btc_address_worker, args=(address,), daemon=True).start()
        elif self.current_type == "ETH":
            self.render_eth_result(address)
        else:
            self.render_unknown_result(address)

    def render_loading_btc(self, address):
        self.clear_transactions_table()

        if self.lang == "it":
            text = (
                "Analisi indirizzo Bitcoin in corso...\n\n"
                f"Indirizzo:\n{address}\n\n"
                "Sto leggendo dati pubblici da mempool.space."
            )
        else:
            text = (
                "Bitcoin address analysis in progress...\n\n"
                f"Address:\n{address}\n\n"
                "Reading public data from mempool.space."
            )

        self.set_text(self.result_text, text)
        self.tabs.select(self.tab_result)
        self.status.config(text=self.t("status_btc_loading"))

    def load_btc_address_worker(self, address):
        quoted = urllib.parse.quote(address, safe="")
        address_url = f"https://mempool.space/api/address/{quoted}"
        txs_url = f"https://mempool.space/api/address/{quoted}/txs"

        try:
            address_data = fetch_json(address_url, timeout=18)
            txs_data = fetch_json(txs_url, timeout=18)

            if not isinstance(txs_data, list):
                txs_data = []

            self.root.after(
                0,
                lambda: self.render_btc_result(address, address_data, txs_data)
            )
        except Exception as e:
            self.root.after(
                0,
                lambda: self.render_btc_error(address, str(e))
            )

    def render_btc_error(self, address, error):
        if self.lang == "it":
            text = (
                "Errore durante l’analisi Bitcoin\n\n"
                f"Indirizzo:\n{address}\n\n"
                f"Dettaglio errore:\n{error}\n\n"
                "Possibili cause:\n"
                "- connessione Internet non disponibile;\n"
                "- API mempool.space temporaneamente non raggiungibile;\n"
                "- indirizzo formalmente valido ma non gestito correttamente dall’endpoint;\n"
                "- timeout temporaneo.\n\n"
                "Puoi comunque aprire l’explorer manualmente dalla scheda Link utili."
            )
        else:
            text = (
                "Error during Bitcoin analysis\n\n"
                f"Address:\n{address}\n\n"
                f"Error detail:\n{error}\n\n"
                "Possible causes:\n"
                "- Internet connection not available;\n"
                "- mempool.space API temporarily unreachable;\n"
                "- formally valid address but not properly handled by the endpoint;\n"
                "- temporary timeout.\n\n"
                "You can still open the explorer manually from the Useful links tab."
            )

        self.set_text(self.result_text, text)
        self.set_text(self.links_text, self.build_btc_links(address))
        self.last_report_text = text + "\n\n" + self.build_btc_links(address)
        self.status.config(text=self.t("status_btc_error"))

    def render_btc_result(self, address, address_data, txs_data):
        self.last_address_data = address_data
        self.last_txs_data = txs_data

        fees = self.network_data.get("fees", {})
        stats = self.network_data.get("stats", {})
        height = self.network_data.get("height", "—")

        chain = address_data.get("chain_stats", {}) or {}
        mempool = address_data.get("mempool_stats", {}) or {}

        funded = int(chain.get("funded_txo_sum", 0) or 0)
        spent = int(chain.get("spent_txo_sum", 0) or 0)
        tx_count = int(chain.get("tx_count", 0) or 0)

        mem_funded = int(mempool.get("funded_txo_sum", 0) or 0)
        mem_spent = int(mempool.get("spent_txo_sum", 0) or 0)
        mem_tx_count = int(mempool.get("tx_count", 0) or 0)

        confirmed_balance = funded - spent
        mempool_delta = mem_funded - mem_spent
        total_balance = confirmed_balance + mempool_delta

        fastest = fees.get("fastestFee", "—")
        half = fees.get("halfHourFee", "—")
        minimum = fees.get("minimumFee", "—")
        mempool_tx_count = stats.get("count", "—")

        risk_notes = self.build_btc_risk_notes(tx_count, confirmed_balance, mempool_delta, fastest)
        hygiene_score, hygiene_reasons = self.calculate_btc_hygiene_score(
        tx_count,
        confirmed_balance,
        mempool_delta,
        fastest
        )
        score_block = self.build_score_block(hygiene_score, hygiene_reasons)

        if self.lang == "it":
            text = (
                "Risultato analisi\n\n"
                "Tipo rilevato: BITCOIN ADDRESS\n\n"
                f"Indirizzo:\n{address}\n\n"
                "Saldo e attività pubblica:\n"
                f"- Saldo confermato: {fmt_btc_from_sats(confirmed_balance)} ({fmt_sats(confirmed_balance)})\n"
                f"- Saldo non confermato/mempool: {fmt_btc_from_sats(mempool_delta)} ({fmt_sats(mempool_delta)})\n"
                f"- Saldo totale stimato: {fmt_btc_from_sats(total_balance)} ({fmt_sats(total_balance)})\n"
                f"- Totale ricevuto confermato: {fmt_btc_from_sats(funded)} ({fmt_sats(funded)})\n"
                f"- Totale speso confermato: {fmt_btc_from_sats(spent)} ({fmt_sats(spent)})\n"
                f"- Transazioni confermate: {tx_count}\n"
                f"- Transazioni non confermate: {mem_tx_count}\n\n"
                "Snapshot Bitcoin network:\n"
                f"- Blocco corrente: {height}\n"
                f"- Transazioni complessive in mempool: {mempool_tx_count}\n"
                f"- Fee fastest: {fastest} sat/vB\n"
                f"- Fee half hour: {half} sat/vB\n"
                f"- Fee minimum: {minimum} sat/vB\n\n"
                "Interpretazione fee:\n"
                f"{self.fee_interpretation(fastest)}\n\n"
                f"{score_block}\n\n"
                "Note operative:\n"
                f"{risk_notes}\n\n"
                "Cosa fare ora:\n"
                "- Apri il block explorer per verificare movimenti e conferme.\n"
                "- Prima di inviare BTC, valuta le fee attuali.\n"
                "- Non inserire mai seed phrase o private key in nessun tool."
            )
        else:
            text = (
                "Analysis result\n\n"
                "Detected type: BITCOIN ADDRESS\n\n"
                f"Address:\n{address}\n\n"
                "Public balance and activity:\n"
                f"- Confirmed balance: {fmt_btc_from_sats(confirmed_balance)} ({fmt_sats(confirmed_balance)})\n"
                f"- Unconfirmed/mempool balance: {fmt_btc_from_sats(mempool_delta)} ({fmt_sats(mempool_delta)})\n"
                f"- Estimated total balance: {fmt_btc_from_sats(total_balance)} ({fmt_sats(total_balance)})\n"
                f"- Total confirmed received: {fmt_btc_from_sats(funded)} ({fmt_sats(funded)})\n"
                f"- Total confirmed spent: {fmt_btc_from_sats(spent)} ({fmt_sats(spent)})\n"
                f"- Confirmed transactions: {tx_count}\n"
                f"- Unconfirmed transactions: {mem_tx_count}\n\n"
                "Bitcoin network snapshot:\n"
                f"- Current block: {height}\n"
                f"- Total mempool transactions: {mempool_tx_count}\n"
                f"- Fastest fee: {fastest} sat/vB\n"
                f"- Half hour fee: {half} sat/vB\n"
                f"- Minimum fee: {minimum} sat/vB\n\n"
                "Fee interpretation:\n"
                f"{self.fee_interpretation(fastest)}\n\n"
                f"{score_block}\n\n"
                "Operational notes:\n"
                f"{risk_notes}\n\n"
                "What to do now:\n"
                "- Open the block explorer to verify movements and confirmations.\n"
                "- Before sending BTC, evaluate current fees.\n"
                "- Never enter seed phrases or private keys into any tool."
            )

        self.set_text(self.result_text, text)
        self.set_text(self.links_text, self.build_btc_links(address))
        self.populate_btc_transactions(address, txs_data)

        self.last_report_text = (
            text
            + "\n\n"
            + self.build_transactions_report(address, txs_data)
            + "\n\n"
            + self.build_btc_links(address)
            + "\n\n"
            + self.t("checklist")
        )

        self.tabs.select(self.tab_result)
        self.status.config(text=self.t("status_btc_done"))

    def build_score_block(self, score, reasons):
        if score >= 80:
            level = self.t("score_level_low")
        elif score >= 55:
            level = self.t("score_level_medium")
        else:
            level = self.t("score_level_high")

        reason_lines = "\n".join(f"- {reason}" for reason in reasons)

        return (
            f"{self.t('score_title')}\n"
            f"- {self.t('score_points')}: {score}/100\n"
            f"- {'Livello' if self.lang == 'it' else 'Level'}: {level}\n\n"
            f"{self.t('score_reasons')}:\n"
            f"{reason_lines}"
        )

    def calculate_btc_hygiene_score(self, tx_count, confirmed_balance, mempool_delta, fastest_fee):
        score = 100
        reasons = []

        if self.lang == "it":
            reasons.append("Indirizzo Bitcoin pubblico analizzato senza richiedere seed phrase o private key.")

            if tx_count == 0:
                reasons.append("Indirizzo senza transazioni confermate: buona situazione lato privacy iniziale.")
            elif tx_count <= 5:
                score -= 5
                reasons.append("Indirizzo già usato poche volte: rischio privacy limitato ma presente.")
            elif tx_count <= 25:
                score -= 12
                reasons.append("Indirizzo riutilizzato più volte: la cronologia pubblica è più leggibile.")
            else:
                score -= 22
                reasons.append("Indirizzo molto riutilizzato: maggiore esposizione della cronologia pubblica.")

            if confirmed_balance > 0:
                score -= 8
                reasons.append("Saldo positivo rilevato: serve attenzione prima di eventuali movimenti.")
            else:
                reasons.append("Saldo confermato pari a zero: nessun fondo visibile sull’indirizzo al momento.")

            if mempool_delta != 0:
                score -= 12
                reasons.append("Sono presenti movimenti non confermati: attendere conferme prima di considerarli definitivi.")

            try:
                fee = float(fastest_fee)
                if fee > 50:
                    score -= 12
                    reasons.append("Fee Bitcoin molto alte: aumentano il rischio operativo di invii costosi o frettolosi.")
                elif fee > 20:
                    score -= 7
                    reasons.append("Fee Bitcoin elevate: meglio valutare il momento prima di inviare fondi.")
                else:
                    reasons.append("Fee Bitcoin non particolarmente critiche nel momento della verifica.")
            except Exception:
                score -= 3
                reasons.append("Fee non interpretabili: controllo rete non pienamente disponibile.")
        else:
            reasons.append("Public Bitcoin address analyzed without requesting seed phrase or private key.")

            if tx_count == 0:
                reasons.append("Address has no confirmed transactions: good initial privacy condition.")
            elif tx_count <= 5:
                score -= 5
                reasons.append("Address used only a few times: limited but present privacy risk.")
            elif tx_count <= 25:
                score -= 12
                reasons.append("Address reused several times: public history is easier to read.")
            else:
                score -= 22
                reasons.append("Heavily reused address: higher exposure of public transaction history.")

            if confirmed_balance > 0:
                score -= 8
                reasons.append("Positive balance detected: be careful before moving funds.")
            else:
                reasons.append("Confirmed balance is zero: no visible funds on the address at the moment.")

            if mempool_delta != 0:
                score -= 12
                reasons.append("Unconfirmed movements are present: wait for confirmations before treating them as final.")

            try:
                fee = float(fastest_fee)
                if fee > 50:
                    score -= 12
                    reasons.append("Bitcoin fees are very high: higher operational risk for expensive or rushed transfers.")
                elif fee > 20:
                    score -= 7
                    reasons.append("Bitcoin fees are elevated: evaluate timing before sending funds.")
                else:
                    reasons.append("Bitcoin fees are not especially critical at the time of this check.")
            except Exception:
                score -= 3
                reasons.append("Fees cannot be interpreted: network check is not fully available.")

        score = max(0, min(100, score))
        return score, reasons
    
    def build_btc_risk_notes(self, tx_count, confirmed_balance, mempool_delta, fastest_fee):
        notes = []

        if self.lang == "it":
            if tx_count == 0:
                notes.append("- L’indirizzo non mostra transazioni confermate. Potrebbe essere nuovo o non ancora usato.")
            else:
                notes.append("- L’indirizzo mostra attività pubblica sulla blockchain: movimenti e saldo sono consultabili da chiunque.")

            if confirmed_balance > 0:
                notes.append("- L’indirizzo ha saldo confermato positivo: prima di eventuali movimenti controlla bene destinatario e fee.")
            else:
                notes.append("- Il saldo confermato risulta pari a zero.")

            if mempool_delta != 0:
                notes.append("- Ci sono movimenti non confermati collegati all’indirizzo: attendi conferme prima di considerarli definitivi.")

            try:
                fee = float(fastest_fee)
                if fee >= 50:
                    notes.append("- Le fee risultano elevate: per movimenti non urgenti può essere prudente attendere.")
                elif fee <= 5:
                    notes.append("- Le fee risultano basse: la rete appare relativamente conveniente.")
            except Exception:
                notes.append("- Fee non interpretabili al momento.")
        else:
            if tx_count == 0:
                notes.append("- The address shows no confirmed transactions. It may be new or not yet used.")
            else:
                notes.append("- The address shows public blockchain activity: movements and balance can be viewed by anyone.")

            if confirmed_balance > 0:
                notes.append("- The address has a positive confirmed balance: before moving funds, carefully check recipient and fees.")
            else:
                notes.append("- The confirmed balance appears to be zero.")

            if mempool_delta != 0:
                notes.append("- There are unconfirmed movements linked to this address: wait for confirmations before treating them as final.")

            try:
                fee = float(fastest_fee)
                if fee >= 50:
                    notes.append("- Fees are high: for non-urgent movements, waiting may be prudent.")
                elif fee <= 5:
                    notes.append("- Fees are low: the network appears relatively convenient.")
            except Exception:
                notes.append("- Fees cannot be interpreted at the moment.")

        return "\n".join(notes)

    def populate_btc_transactions(self, address, txs_data):
        self.clear_transactions_table()

        if not txs_data:
            self.transactions_tree.insert(
                "",
                "end",
                values=("—", "—", self.t("tx_none"), "—", "—", "—")
            )
            return

        for tx in txs_data[:25]:
            txid = tx.get("txid", "")
            status = tx.get("status", {}) or {}
            confirmed = bool(status.get("confirmed", False))

            if confirmed:
                block_time = status.get("block_time")
                if block_time:
                    date = datetime.fromtimestamp(int(block_time)).strftime("%Y-%m-%d %H:%M")
                else:
                    date = self.t("tx_confirmed")
                status_label = self.t("tx_confirmed")
            else:
                date = self.t("tx_in_mempool")
                status_label = self.t("tx_unconfirmed")

            net_sats = self.calculate_tx_net_for_address(tx, address)

            if net_sats > 0:
                move_type = self.t("tx_received")
            elif net_sats < 0:
                move_type = self.t("tx_spent")
            else:
                move_type = self.t("tx_neutral")

            amount = fmt_btc_from_sats(net_sats)
            fee = fmt_sats(tx.get("fee", 0))

            self.transactions_tree.insert(
                "",
                "end",
                values=(
                    date,
                    move_type,
                    amount,
                    fee,
                    status_label,
                    txid
                )
            )

    def calculate_tx_net_for_address(self, tx, address):
        received = 0
        spent = 0

        for vout in tx.get("vout", []) or []:
            if vout.get("scriptpubkey_address") == address:
                received += int(vout.get("value", 0) or 0)

        for vin in tx.get("vin", []) or []:
            prevout = vin.get("prevout", {}) or {}
            if prevout.get("scriptpubkey_address") == address:
                spent += int(prevout.get("value", 0) or 0)

        return received - spent

    def build_transactions_report(self, address, txs_data):
        lines = []

        if self.lang == "it":
            lines.append("Ultime transazioni BTC")
            none_text = "Nessuna transazione recente trovata."
        else:
            lines.append("Latest BTC transactions")
            none_text = "No recent transactions found."

        lines.append("")

        if not txs_data:
            lines.append(none_text)
            return "\n".join(lines)

        for tx in txs_data[:15]:
            txid = tx.get("txid", "")
            status = tx.get("status", {}) or {}
            confirmed = bool(status.get("confirmed", False))
            net_sats = self.calculate_tx_net_for_address(tx, address)

            if net_sats > 0:
                move_type = self.t("tx_received")
            elif net_sats < 0:
                move_type = self.t("tx_spent")
            else:
                move_type = self.t("tx_neutral")

            fee = fmt_sats(tx.get("fee", 0))

            if confirmed and status.get("block_time"):
                date = datetime.fromtimestamp(int(status.get("block_time"))).strftime("%Y-%m-%d %H:%M")
            else:
                date = self.t("tx_unconfirmed")

            lines.append(f"- {date} · {move_type} · {fmt_btc_from_sats(net_sats)} · fee {fee} · {txid}")

        return "\n".join(lines)

    def render_eth_result(self, address):
        if self.lang == "it":
            eth_score_block = self.build_score_block(
                75,
                [
                    "Formato Ethereum/EVM valido.",
                    "Il tool non collega il wallet e non richiede firme.",
                    "Controllo approvals demandato a Revoke.cash/Etherscan.",
                    "Rischio residuo legato a eventuali firme già effettuate o autorizzazioni concesse in passato."
                ]
            )
        else:
            eth_score_block = self.build_score_block(
                75,
                [
                    "Valid Ethereum/EVM address format.",
                    "The tool does not connect to the wallet and does not request signatures.",
                    "Approval checks are delegated to Revoke.cash/Etherscan.",
                    "Residual risk depends on previous signatures or permissions already granted."
                ]
            )
        if self.lang == "it":
            text = (
                "Risultato analisi\n\n"
                "Tipo rilevato: ETHEREUM / EVM ADDRESS\n\n"
                f"Indirizzo:\n{address}\n\n"
                "Lettura sicurezza:\n"
                "- L’indirizzo sembra compatibile con un formato Ethereum/EVM pubblico.\n"
                "- Può essere usato su reti compatibili come Ethereum, Base, Polygon, Arbitrum, Optimism e altre EVM.\n"
                "- Il solo indirizzo pubblico non permette di spendere fondi.\n\n"
                "Attenzione Web3:\n"
                "- Il rischio principale non è il controllo dell’indirizzo pubblico, ma ciò che firmi con il wallet.\n"
                "- Controlla periodicamente token approvals e autorizzazioni concesse agli smart contract.\n"
                "- Diffida da airdrop, mint, claim, bridge e siti che chiedono firme non chiare.\n\n"
                f"{eth_score_block}\n\n"
                "Cosa fare ora:\n"
                "- Apri Etherscan per vedere attività pubbliche dell’indirizzo.\n"
                "- Apri Revoke.cash per controllare eventuali autorizzazioni token.\n"
                "- Non collegare il wallet a siti sconosciuti.\n\n"
                "Nota v0.3:\n"
                "La lettura saldo/transazioni ETH via API key opzionale sarà aggiunta in una versione successiva."
            )
        else:
            text = (
                "Analysis result\n\n"
                "Detected type: ETHEREUM / EVM ADDRESS\n\n"
                f"Address:\n{address}\n\n"
                "Security reading:\n"
                "- The address appears compatible with a public Ethereum/EVM format.\n"
                "- It can be used on compatible networks such as Ethereum, Base, Polygon, Arbitrum, Optimism and other EVM chains.\n"
                "- The public address alone cannot spend funds.\n\n"
                "Web3 caution:\n"
                "- The main risk is not viewing the public address, but what you sign with your wallet.\n"
                "- Periodically check token approvals and permissions granted to smart contracts.\n"
                "- Be wary of airdrops, mints, claims, bridges and websites asking for unclear signatures.\n\n"
                f"{eth_score_block}\n\n"
                "What to do now:\n"
                "- Open Etherscan to view public activity for the address.\n"
                "- Open Revoke.cash to check token approvals.\n"
                "- Do not connect your wallet to unknown websites.\n\n"
                "v0.3 note:\n"
                "ETH balance/transaction reading through an optional API key will be added in a later version."
            )

        self.set_text(self.result_text, text)
        self.set_text(self.links_text, self.build_eth_links(address))
        self.clear_transactions_table()
        self.transactions_tree.insert(
            "",
            "end",
            values=("—", "ETH/Web3", "Etherscan / Revoke.cash", "—", "—", "—")
        )

        self.last_report_text = text + "\n\n" + self.build_eth_links(address) + "\n\n" + self.t("checklist")
        self.tabs.select(self.tab_result)
        self.status.config(text=self.t("status_eth_done"))

    def render_unknown_result(self, address):
        if self.lang == "it":
            text = (
                "Risultato analisi\n\n"
                "Tipo rilevato: NON RICONOSCIUTO\n\n"
                f"Input inserito:\n{address}\n\n"
                "Il formato non sembra un indirizzo Bitcoin o Ethereum/EVM standard.\n\n"
                "Possibili cause:\n"
                "- indirizzo copiato male;\n"
                "- spazio o carattere mancante;\n"
                "- indirizzo di una blockchain non ancora supportata;\n"
                "- hai inserito per errore un dato che non è un indirizzo pubblico.\n\n"
                "Nota di sicurezza:\n"
                "- Se hai incollato una seed phrase o una private key, interrompi subito l’uso del tool.\n"
                "- Non condividere quel dato con nessuno.\n"
                "- Valuta di spostare i fondi su un wallet nuovo e sicuro, se la seed è stata esposta."
            )
            links_text = "Nessun link generato perché il formato non è stato riconosciuto."
        else:
            text = (
                "Analysis result\n\n"
                "Detected type: UNRECOGNIZED\n\n"
                f"Input:\n{address}\n\n"
                "The format does not look like a standard Bitcoin or Ethereum/EVM address.\n\n"
                "Possible causes:\n"
                "- address copied incorrectly;\n"
                "- missing space or character;\n"
                "- address from a blockchain not yet supported;\n"
                "- you accidentally entered data that is not a public address.\n\n"
                "Security note:\n"
                "- If you pasted a seed phrase or private key, stop using the tool immediately.\n"
                "- Do not share that data with anyone.\n"
                "- Consider moving funds to a new secure wallet if the seed was exposed."
            )
            links_text = "No link generated because the format was not recognized."

        self.set_text(self.result_text, text)
        self.set_text(self.links_text, links_text)
        self.clear_transactions_table()
        self.last_report_text = text
        self.tabs.select(self.tab_result)
        self.status.config(text=self.t("status_unknown"))

    def build_btc_links(self, address):
        mempool_url = f"https://mempool.space/address/{address}"
        blockstream_url = f"https://blockstream.info/address/{address}"

        if self.lang == "it":
            return (
                "Link utili per indirizzo Bitcoin\n\n"
                f"1. Mempool.space explorer:\n{mempool_url}\n\n"
                f"2. Blockstream explorer:\n{blockstream_url}\n\n"
                "Nota:\n"
                "Gli explorer mostrano dati pubblici della blockchain. Non inserire mai seed phrase."
            )

        return (
            "Useful links for Bitcoin address\n\n"
            f"1. Mempool.space explorer:\n{mempool_url}\n\n"
            f"2. Blockstream explorer:\n{blockstream_url}\n\n"
            "Note:\n"
            "Explorers show public blockchain data. Never enter seed phrases."
        )

    def build_eth_links(self, address):
        etherscan_url = f"https://etherscan.io/address/{address}"
        revoke_url = f"https://revoke.cash/address/{address}"
        basescan_url = f"https://basescan.org/address/{address}"
        polygonscan_url = f"https://polygonscan.com/address/{address}"
        arbiscan_url = f"https://arbiscan.io/address/{address}"
        optimistic_url = f"https://optimistic.etherscan.io/address/{address}"

        if self.lang == "it":
            return (
                "Link utili per indirizzo Ethereum / EVM\n\n"
                f"1. Etherscan:\n{etherscan_url}\n\n"
                f"2. Revoke.cash approvals:\n{revoke_url}\n\n"
                f"3. BaseScan:\n{basescan_url}\n\n"
                f"4. PolygonScan:\n{polygonscan_url}\n\n"
                f"5. Arbiscan:\n{arbiscan_url}\n\n"
                f"6. Optimism explorer:\n{optimistic_url}\n\n"
                "Nota:\n"
                "Questo tool non collega il wallet. I link servono per consultare dati pubblici "
                "e controllare manualmente eventuali autorizzazioni."
            )

        return (
            "Useful links for Ethereum / EVM address\n\n"
            f"1. Etherscan:\n{etherscan_url}\n\n"
            f"2. Revoke.cash approvals:\n{revoke_url}\n\n"
            f"3. BaseScan:\n{basescan_url}\n\n"
            f"4. PolygonScan:\n{polygonscan_url}\n\n"
            f"5. Arbiscan:\n{arbiscan_url}\n\n"
            f"6. Optimism explorer:\n{optimistic_url}\n\n"
            "Note:\n"
            "This tool does not connect to your wallet. Links are used to inspect public data "
            "and manually check possible permissions."
        )

    def fee_interpretation(self, fastest):
        try:
            fee = float(fastest)
        except Exception:
            return self.t("fee_unknown")

        if fee <= 5:
            return self.t("fee_low")
        if fee <= 20:
            return self.t("fee_medium")
        if fee <= 50:
            return self.t("fee_high")
        return self.t("fee_very_high")

    def load_network_snapshot(self):
        try:
            self.status.config(text=self.t("status_loading_network"))
        except Exception:
            pass

        threading.Thread(target=self.load_network_worker, daemon=True).start()

    def load_network_worker(self):
        errors = []

        try:
            self.network_data["fees"] = fetch_json(URLS["mempool_fees"])
        except Exception as e:
            errors.append(f"fee: {e}")
            self.network_data["fees"] = {}

        try:
            self.network_data["stats"] = fetch_json(URLS["mempool_stats"])
        except Exception as e:
            errors.append(f"mempool: {e}")
            self.network_data["stats"] = {}

        try:
            self.network_data["height"] = fetch_text(URLS["mempool_height"]).strip()
        except Exception as e:
            errors.append(f"height: {e}")
            self.network_data["height"] = "—"

        self.root.after(0, lambda: self.render_network_snapshot(errors))

    def render_network_snapshot(self, errors):
        fees = self.network_data.get("fees", {})
        stats = self.network_data.get("stats", {})
        height = self.network_data.get("height", "—")

        if self.lang == "it":
            text = (
                "Bitcoin network snapshot\n\n"
                f"Blocco corrente: {height}\n"
                f"Transazioni in mempool: {stats.get('count', '—')}\n"
                f"Dimensione virtuale mempool: {stats.get('vsize', '—')}\n"
                f"Fee totale mempool: {stats.get('total_fee', '—')}\n\n"
                "Fee consigliate:\n"
                f"- Fastest fee: {fees.get('fastestFee', '—')} sat/vB\n"
                f"- Half hour fee: {fees.get('halfHourFee', '—')} sat/vB\n"
                f"- Hour fee: {fees.get('hourFee', '—')} sat/vB\n"
                f"- Economy fee: {fees.get('economyFee', '—')} sat/vB\n"
                f"- Minimum fee: {fees.get('minimumFee', '—')} sat/vB\n\n"
                "Interpretazione:\n"
                f"{self.fee_interpretation(fees.get('fastestFee', '—'))}\n\n"
                "Fonte: mempool.space public API\n"
            )
            warning_label = "\nAvvisi:\n"
        else:
            text = (
                "Bitcoin network snapshot\n\n"
                f"Current block: {height}\n"
                f"Mempool transactions: {stats.get('count', '—')}\n"
                f"Virtual mempool size: {stats.get('vsize', '—')}\n"
                f"Total mempool fee: {stats.get('total_fee', '—')}\n\n"
                "Recommended fees:\n"
                f"- Fastest fee: {fees.get('fastestFee', '—')} sat/vB\n"
                f"- Half hour fee: {fees.get('halfHourFee', '—')} sat/vB\n"
                f"- Hour fee: {fees.get('hourFee', '—')} sat/vB\n"
                f"- Economy fee: {fees.get('economyFee', '—')} sat/vB\n"
                f"- Minimum fee: {fees.get('minimumFee', '—')} sat/vB\n\n"
                "Interpretation:\n"
                f"{self.fee_interpretation(fees.get('fastestFee', '—'))}\n\n"
                "Source: mempool.space public API\n"
            )
            warning_label = "\nWarnings:\n"

        if errors:
            text += warning_label + "\n".join(f"- {e}" for e in errors)

        self.set_text(self.network_text, text)

        if errors:
            self.status.config(text=self.t("status_network_loaded_warnings").format(count=len(errors)))
        else:
            self.status.config(text=self.t("status_network_loaded"))

    def open_current_primary_link(self):
        address = self.current_address.strip() or self.address_var.get().strip()
        address_type = self.current_type if self.current_address else detect_address_type(address)

        if not address:
            messagebox.showinfo(self.t("popup_no_address_title"), self.t("popup_no_address_msg"))
            return

        if address_type == "BTC":
            webbrowser.open(f"https://mempool.space/address/{address}")
        elif address_type == "ETH":
            webbrowser.open(f"https://etherscan.io/address/{address}")
        else:
            messagebox.showinfo(self.t("popup_unknown_title"), self.t("popup_unknown_msg"))

    def open_selected_tx(self, tree):
        selected = tree.selection()

        if not selected:
            return

        values = tree.item(selected[0], "values")

        if not values or len(values) < 6:
            return

        txid = values[5]

        if txid and txid != "—":
            webbrowser.open(f"https://mempool.space/tx/{txid}")

    def export_report(self):
        if not self.last_report_text:
            messagebox.showinfo(self.t("popup_report_unavailable_title"), self.t("popup_report_unavailable_msg"))
            return

        path = filedialog.asksaveasfilename(
            title=self.t("btn_report"),
            defaultextension=".txt",
            initialfile=self.t("report_default_name"),
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )

        if not path:
            return

        if self.lang == "it":
            header_title = "MolinaCrypto Wallet Safety Check\n"
            version_label = "Versione"
            author_label = "Autore"
            date_label = "Data report"
            site_label = "Sito"
        else:
            header_title = "MolinaCrypto Wallet Safety Check\n"
            version_label = "Version"
            author_label = "Author"
            date_label = "Report date"
            site_label = "Website"

        header = (
            header_title
            + f"{version_label}: {APP_VERSION}\n"
            + f"{author_label}: {AUTHOR}\n"
            + f"{date_label}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            + f"{site_label}: https://www.molinacrypto.eu\n"
            + "\n"
            + self.t("report_header_note")
            + "\n"
            + "=" * 72
            + "\n\n"
        )

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(header + self.last_report_text)

            messagebox.showinfo(
                self.t("popup_report_saved_title"),
                self.t("popup_report_saved_msg").format(path=path)
            )
        except Exception as e:
            messagebox.showerror(
                self.t("popup_report_error_title"),
                self.t("popup_report_error_msg").format(error=e)
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = WalletSafetyCheckApp(root)
    root.mainloop()
