import json

class Inventory:
    def __init__(self) -> None:
        self.items = {}

    def load_from_file(self, path:str, default_contents:dict|None=None) -> None:
        self.items = default_contents or {}

        try:
            with open(path, "r") as f:
                self.items = json.load(f)

        except ...:
            ... # fancy error handling (ben ik nu te gebrakt voor)

    def save_to_file(self, path:str) -> None:
        try:
            with open(path, "w") as f:
                json.dump(self.items, f)

        except ...:
            ... # nog meer fancy errors

    def __getitem__(self, item:str) -> int:
        return self.items.get(item, 0)
    
    def __setitem__(self, item:str, val:int) -> None:
        self.items.update({
            item: val
        })

if __name__ == "__main__":
    (inventory := Inventory()).load_from_file("een/random/save.json")

    inventory["zest"] = 999
    print(inventory["zest"])