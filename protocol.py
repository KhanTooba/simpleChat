def getProtocolID(name):
    if "REGISTER_TOSEND" in name:
        return 0
    elif "REGISTERED_TOSEND" in name:
        return 1
    elif "REGISTER_TORECV" in name:
        return 2
    elif "REGISTERED_TORECV" in name:
        return 3
    elif "ERROR_100" in name:
        return 100
    elif "ERROR_101" in name:
        return 101
    elif "ERROR_102" in name:
        return 102
    elif "ERROR_103" in name:
        return 103
    elif "SEND" in name:
        return 4
    elif "RECEIVED" in name:
        return 5
    elif "FORWARD" in name:
        return 6