from race import Race

player = Race(
    char="@", color=(255, 255, 255), name="Player", max_hp=30, defense=2, power=5
)

orc = Race(char="o", color=(63, 127, 63), name="Orc", max_hp=10, defense=0, power=3)
troll = Race(char="T", color=(0, 127, 0), name="Troll", max_hp=16, defense=1, power=4)
