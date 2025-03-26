def calculate_image_data(path):
    with open(path, "rb") as f:
        return f.read()
