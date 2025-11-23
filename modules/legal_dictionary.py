LEGAL_TERMS = {
    "FIR": "First Information Report – the first step to report a crime to the police.",
    "bail": "Temporary release of an accused person before trial, sometimes requiring money as a guarantee.",
    "cognizance": "When a court takes official notice of an offence and starts proceedings.",
    "charge sheet": "The police report filed after investigation, listing evidence and witnesses.",
    "warrant": "A legal order issued by a court allowing police to arrest, search, or seize property.",
    "indemnity": "A promise to compensate someone for loss or damage.",
    "plaintiff": "The person who brings a case to court.",
    "defendant": "The person accused or sued in a case.",
    "contract": "A legal agreement enforceable by law.",
    "termination clause": "Part of a contract that explains how the agreement can be ended.",
    "jurisdiction": "The legal authority of a court to hear a case.",
    "negligence": "Failure to take proper care, resulting in damage or harm.",
    "penalty": "Punishment or fine for breaking a law or contract.",
    "probation": "Release of an offender under supervision instead of jail time.",
    "summons": "An official order to appear before a court."
}

def explain_terms(text: str) -> dict:
    """
    Scan the text and return dictionary of legal terms with explanations.
    """
    explanations = {}
    for term, definition in LEGAL_TERMS.items():
        if term.lower() in text.lower():
            explanations[term] = definition
    return explanations
