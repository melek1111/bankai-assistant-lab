from datetime import datetime

KB = [
    {"id":"card_blocked","text":"If a card is blocked, the customer should verify the reason in the banking app or contact support. Never ask for a full card number or PIN.","source":"Card Safety FAQ"},
    {"id":"suspicious_transaction","text":"For a suspicious transaction, advise the customer not to share credentials, review the transaction, and contact the bank through an official channel if it is unauthorized.","source":"Fraud Prevention FAQ"},
    {"id":"transfer_failed","text":"For a failed transfer, check recipient details, available balance, limits, and transaction status. Escalate if the transaction remains pending or failed unexpectedly.","source":"Transfers FAQ"},
    {"id":"forgotten_pin","text":"A forgotten PIN should be reset through an official banking channel. The assistant must not request the existing PIN.","source":"Card Safety FAQ"},
    {"id":"branch_hours","text":"Branch hours vary by location. Ask for the branch or location before giving a location-specific answer.","source":"Branch FAQ"},
]

TOOLS = {
    "account_balance": {"description":"Returns a mock account balance.","result":"Mock balance: 2,450.00 GEL"},
    "transaction_lookup": {"description":"Looks up a mock transaction.","result":"Mock transaction: TX-2048 — 120.00 GEL — status: completed"},
    "card_status": {"description":"Checks a mock card status.","result":"Mock card status: active"},
    "branch_search": {"description":"Searches mock branch information.","result":"Mock result: central branch — Mon-Fri 10:00-18:00"},
}

def classify(message: str):
    m = message.lower()
    rules = [
        ("card_blocked", ["blocked card", "card blocked", "card is blocked"]),
        ("suspicious_transaction", ["suspicious", "fraud", "unauthorized", "unknown transaction"]),
        ("transfer_failed", ["transfer failed", "failed transfer", "transfer didn't", "transfer did not"]),
        ("forgotten_pin", ["forgot pin", "forgotten pin", "pin"]),
        ("branch_hours", ["branch", "opening hours", "working hours", "hours"]),
        ("account_balance", ["balance", "how much money"]),
        ("transaction_lookup", ["transaction", "payment"]),
        ("card_status", ["card status"]),
    ]
    for intent, keys in rules:
        if any(k in m for k in keys):
            return intent
    return "general_support"

def retrieve(intent):
    hits = [x for x in KB if x["id"] == intent]
    if hits:
        return [{**hits[0], "relevance": 0.97}]
    return []

def safety_check(message):
    sensitive = ["password", "full card number", "cvv", "cvc", "pin", "one-time code", "otp"]
    found = [x for x in sensitive if x in message.lower()]
    return {"status":"PASS" if not found else "CAUTION", "reason":"No sensitive credential request detected." if not found else "Sensitive authentication data detected; do not request or expose it.", "signals":found}

def response_for(intent, message):
    answers = {
        "card_blocked":"If your card is blocked, please check the reason in the official banking app or contact the bank through an official support channel. I would not ask you for your PIN or full card number here.",
        "suspicious_transaction":"If you do not recognize a transaction, avoid sharing credentials and contact the bank through an official channel. Review the transaction details and follow the bank's fraud-reporting process.",
        "transfer_failed":"For a failed transfer, first verify the recipient details, available balance, and transfer limits. If the transfer still fails or remains pending, it should be escalated to support.",
        "forgotten_pin":"For a forgotten PIN, use the bank's official app or support channel to reset it. Do not share your existing PIN with anyone.",
        "branch_hours":"Branch hours depend on the location. Tell me which branch or area you mean and I can use a branch-search tool in a real implementation.",
        "account_balance":TOOLS["account_balance"]["result"] + " (demo data only)",
        "transaction_lookup":TOOLS["transaction_lookup"]["result"] + " (demo data only)",
        "card_status":TOOLS["card_status"]["result"] + " (demo data only)",
        "general_support":"I can help with common banking-support scenarios such as blocked cards, suspicious transactions, transfers, PIN recovery, and branch information. This portfolio demo uses mock banking data.",
    }
    return answers[intent]

def run_agent(message: str):
    intent = classify(message)
    safety = safety_check(message)
    retrieved = retrieve(intent)
    tool_calls = []
    if intent in TOOLS:
        tool_calls.append({"tool":intent,"status":"mock_success","result":TOOLS[intent]["result"]})
    state = ["received","intent_router","knowledge_retrieval"]
    if tool_calls: state.append("tool_call")
    state += ["safety_check","response"]
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message,
        "intent": intent,
        "agent_state": state,
        "tool_calls": tool_calls,
        "retrieved_knowledge": retrieved,
        "safety_check": safety,
        "response": response_for(intent, message),
        "mode": "mock-demo",
    }
