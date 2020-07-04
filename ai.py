import actions


class AI(actions.Action):
    def perform(self) -> None:
        print(f"The {self.entity.name} wonders when it will get to take a real turn.")
