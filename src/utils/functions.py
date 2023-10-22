def convert_to_json(item):
    result = {}
    for key, value in item.items():
        if "S" in value:
            result[key] = value["S"]
        elif "N" in value:
            result[key] = int(value["N"])
        elif "SS" in value:
            result[key] = value["SS"]
        # Puedes agregar más conversiones para otros tipos de DynamoDB si es necesario
    return result