import yaml


class PlayerDB:
    def __init__(self, file_path="db.yaml"):
        self.file_path = file_path
        self.db = self.__load_db()

    def __load_db(self):
        return yaml.safe_load(open(self.file_path, "r"))

    def save_db(self, db):
        yaml.safe_dump(db, open(self.file_path, "w"))

    def __str__(self):
        return str(self.db)


# db = PlayerDB()
# print(db.__str__())
