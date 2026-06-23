def route_department(text):

    text = text.lower()

    if "grievance" in text:
        return "DEPT_CUSTOMER_SERVICE"

    elif "aggregator" in text:
        return "DEPT_DATA_GOVERNANCE"

    return "DEPT_COMPLIANCE"