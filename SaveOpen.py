import pickle

def save_bin(automat, path):
    with open(path, "wb") as file:
        pickle.dump(automat, file)
    print("Done.")


def read_from_bin(path):
    with open(path, "rb") as file:
        return pickle.load(file)