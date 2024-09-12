def multiply(data):
    """Function that multiplied cols a and b"""

    data["product"] = data["a"] * data["b"]

    return data


if __env:  # indicates we are running on Taktile
    data = add(data)
