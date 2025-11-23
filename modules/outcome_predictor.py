def predict_outcome(fir_text):
    text = fir_text.lower()
    if "murder" in text or "assault" in text:
        return "High chance of arrest (serious crime)"
    elif "fraud" in text or "cheating" in text:
        return "Investigation may take months (financial crime)"
    elif "theft" in text or "burglary" in text:
        return "Likely recovery depends on police follow-up"
    elif "cyber" in text or "atm card" in text:
        return "Cyber cell involvement needed"
    return "Outcome unclear – depends on investigation"