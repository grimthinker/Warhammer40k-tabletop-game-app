import random

from logic.classes import DInt
from models.profile import RangedWeapon, MeleeWeapon, ModelProfile


def calculate_damage_chance(weapon: RangedWeapon | MeleeWeapon, target: ModelProfile):
    def _wound_on(S, T):
        if S < T:
            if 2 * S <= T: return 6
            else: return 5
        if S == T: return 4
        if S > T:
            if S < 2 * T: return 3
            else: return 2

    attack_nums = []
    damage_series = []
    hit_on = weapon.BS if isinstance(weapon, RangedWeapon) else weapon.WS
    wound_on = _wound_on(weapon.S, target.T)
    inv_save_on = target.InvSv if target.InvSv else 1000
    save_on = min(target.Sv - weapon.AP, inv_save_on)
    for _ in range(66500):
        attack_num = weapon.A.rand if isinstance(weapon.A, DInt) else weapon.A
        attack_nums.append(attack_num)
        full_damage = 0
        for attack in range(attack_num):
            hit_roll_res = random.randint(1, 6)
            if hit_roll_res >= hit_on:
                wound_roll_res = random.randint(1, 6)
                if wound_roll_res >= wound_on:
                    save_roll_res = random.randint(1, 6)
                    if save_roll_res < save_on:
                        FNP_on = 0
                        if target.abilities:
                            for ability in target.abilities:
                                if 'FNP' in ability.tags:
                                    FNP_on = ability.FNP

                        damage = weapon.D.rand if isinstance(weapon.D, DInt) else weapon.D
                        if FNP_on:
                            for wound in range(damage):
                                FNP_roll_res = random.randint(1, 6)
                                if FNP_roll_res >= FNP_on:
                                    damage -= 1
                        full_damage += damage
        damage_series.append(full_damage)
    success_damage_set = list(filter(None, damage_series))
    missed_damage_set = list(filter(lambda x: x == 0, damage_series))
    average_damage = sum(damage_series) / len(damage_series)
    average_success_damage = sum(success_damage_set) / len(success_damage_set)
    print(average_damage, average_success_damage, max(damage_series), max(attack_nums))









