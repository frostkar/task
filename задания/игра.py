# ================================================
# ИГРА «КАРАМЕЛЬНОЕ БОЛОТО»
# Автор: <Юрьева Алена>
# Дата: <28.10> 2026
#
# Пункт 4 — «попробовать карамель»: герой слизывает
# каплю сиропа со стены — сахар бодрит, здоровье
# прибавляется, но запас сил тает. Пункт 5 —
# «разломать леденец»: осматривает стены и находит
# проход глубже.
# ================================================

import random

# --- Заголовок ------------------------------------
title = "КАРАМЕЛЬНОЕ БОЛОТО"
frame = "=" * 24
print(frame)
print("   " + title + "   ")
print(frame)
print()

# --- Знакомство с героем --------------------------
print("Как зовут героя?")
hero_name = input()
print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в пещеру. Стены липкие от карамели, под ногами чавкает сироп, а в глубине довольно хлюпает желе.")
print()

# --- Настройка героя ------------------------------
print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость — по одному числу в строке:")

while True:
    try:
        raw = [input(), input(), input(), input()]
        health, strength, agility, endurance = map(int, raw)

        if health <= 0:
            raise ValueError(f"Здоровье должно быть положительным, а введено {health}")
        if strength < 0 or agility < 0 or endurance < 0:
            raise ValueError("Остальные характеристики не могут быть отрицательными")
        if agility > health * 2:
            raise ValueError("Ловкость не может превышать удвоенное здоровье")

        break
    except ValueError as e:
        print(f"Ошибка: {e}. Введите все четыре числа снова:")

base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = (health // 5) + endurance

print("Характеристики героя:")
print(f"Здоровье: {health}")
print(f"Сила: {strength}")
print(f"Ловкость: {agility}")
print(f"Выносливость: {endurance}")
print()
print(f"Урон героя: {damage:.1f}")
print(f"Критический урон: {crit_damage:.1f}")
print(f"Запас сил: {stamina}")
print()

# --- ФУНКЦИИ --------------------------------------

def hero_hit(strike_n):
    """
    Урон героя в удар номер strike_n.
    Возвращает пару (hit, crit): урон и признак критического удара.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health):
    """
    Бой с enemy до гибели одного из двоих.
    Печатает строки раундов. Возвращает (rounds, won, hero_health).
    """
    enemy_hp = enemies[enemy]
    rounds = []
    round_n = 0
    print(f"Ты спускаешься по ступеням. Из сладкого тумана появляется {enemy}!")

    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        enemy_hp -= hit

        line = f"Раунд {round_n}: герой наносит {hit:.1f}"
        if crit:
            line += " — критический!"

        if enemy_hp <= 0:
            line += f" {enemy.capitalize()} {enemy_defeat[enemy]}."
            rounds.append([round_n, hit, 0])
        else:
            low, high = enemy_damage[enemy]
            blow = random.randint(low, high)
            hero_health -= blow
            line += (
                f" Здоровье врага: {enemy_hp:.1f}. "
                f"{enemy.capitalize()} {enemy_attacks[enemy]} — {blow} урона."
            )
            rounds.append([round_n, hit, blow])

        print(line)

    return rounds, enemy_hp <= 0, hero_health


def print_leaderboard(log_data):
    """
    Печатает топ-3 раундов по урону героя и рекорд врага.
    Возвращает None.
    """
    if not log_data:
        print("Ты еще не сражался.")
        return

    top = sorted(log_data, key=lambda r: r[1], reverse=True)[:3]
    print("Таблица лидеров (урон героя):")
    for i in range(len(top)):
        print(f"{i + 1}. Раунд {top[i][0]}: {top[i][1]:.1f}")
    worst = max(log_data, key=lambda r: r[2])
    print(f"Самый сильный удар врага: {worst[2]} (раунд {worst[0]}).")


def print_run_summary(log_data):
    """
    Печатает итог забега: суммарный и средний урон героя.
    Возвращает None. Безопасна на пустом журнале.
    """
    total = sum(r[1] for r in log_data)
    rounds = len(log_data)
    if rounds > 0:
        print(f"Урон: {total:.1f} за {rounds} раундов, в среднем {total / rounds:.1f}.")
    else:
        print("В этом забеге не было боев.")

# --- ГЛАВНЫЙ ЦИКЛ --------------------------------

running = True
actions = 0
outcome = "прерывание"

enemies = {
    "желейный слизень": 40,
    "шоколадный паук": 20,
    "засахаренный зомби": 65,
    "торт-великан": 180
}

# Как каждый враг атакует — подставляется в строку раунда
enemy_attacks = {
    "желейный слизень": "дрожит и шлёпает липким комком",
    "шоколадный паук": "плюёт какао-пылью",
    "засахаренный зомби": "бьёт застывшей корочкой",
    "торт-великан": "швыряет крошками и кремом"
}

# Сколько урона наносит каждый враг — (минимум, максимум)
enemy_damage = {
    "желейный слизень": (2, 5),
    "шоколадный паук": (1, 4),
    "засахаренный зомби": (3, 7),
    "торт-великан": (5, 10)
}

# Как каждый враг погибает
enemy_defeat = {
    "желейный слизень": "расползается сладкой лужей",
    "шоколадный паук": "рассыпается какао-крошкой",
    "засахаренный зомби": "осыпается сахарной пудрой",
    "торт-великан": "разваливается на коржи"
}

log = []

try:
    while running:
        print("Что делаешь?")
        print("1 - осмотреться")
        print("2 - идти вперёд")
        print("3 - отдохнуть")
        print("4 - попробовать карамель")
        print("5 - разломать леденец")
        print("6 - тренировка")
        print("7 - спуститься глубже")
        print("8 - таблица лидеров")
        print("0 - выйти из подземелья")
        print()

        while True:
            choice = input()
            try:
                menu_number = int(choice)
            except ValueError:
                print("Такого пункта нет. Введи номер пункта из меню:")
                continue

            if 0 <= menu_number <= 8:
                break
            print("Такого пункта нет. Введи номер пункта из меню:")

        match menu_number:
            case 0:
                print("Ты поднимаешься обратно к свету. Карамельное болото остаётся позади.")
                outcome = "выход"
                running = False
            case 1:
                print("Ты осмотрелся. Вокруг тянутся липкие сталактиты, а вдалеке виднеется проход.")
            case 2:
                cost = 2
                if stamina >= cost:
                    stamina -= cost
                    print("Ты осторожно идёшь вперёд. Сироп чавкает под ногами.")
                else:
                    health -= cost - stamina
                    stamina = 0
                    print("Сил больше нет — ты идёшь на одном упорстве.")
            case 3:
                stamina += 3
                print("Ты прислонился к липкой стене и перевёл дух. Карамельный воздух немного бодрит.")
            case 4:
                stamina -= 1
                health += 5
                print("Ты слизнул каплю карамели со стены. Сахар ударил в голову: здоровья прибавилось, но силы тают.")
            case 5:
                print("Ты разломал леденец. Внутри блеснула пустота — там начинается спуск глубже.")
            case 6:
                if stamina < 3:
                    print("Сил не хватает на тренировку. Отдохни немного.")
                else:
                    strikes = 6
                    total_damage = 0.0
                    crit_count = 0
                    stamina -= 3

                    print("Ты подходишь к застывшей карамельной глыбе, которая пока является твоим главным противником.")
                    print("Она стоит здесь с тех пор, как сюда приходил последний сладкоежка.")
                    print()
                    print(f"Наносишь {strikes} ударов.")

                    for i in range(1, strikes + 1):
                        hit_damage, crit = hero_hit(i)
                        if crit:
                            crit_count += 1
                            print(f"Удар {i}: {hit_damage:.1f} урона — критический!")
                        else:
                            print(f"Удар {i}: {hit_damage:.1f} урона")
                        total_damage += hit_damage

                    print()
                    print(f"Итог: {strikes} ударов, критических ударов: {crit_count}")
                    print(f"Общий урон: {total_damage:.1f}")
                    print(f"Средний урон: {total_damage / strikes:.1f}")
            case 7:
                if not enemies:
                    print("Ты спускаешься по ступеням, но подземелье пусто.")
                else:
                    enemy = random.choice(list(enemies.keys()))
                    rounds, won, health = fight(enemy, health)

                    for r in rounds:
                        log.append(r)

                    if won:
                        del enemies[enemy]
                        print(f"В подземелье осталось врагов: {len(enemies)}.")
                        print(f"Бой: {len(rounds)} раундов.")
            case 8:
                print_leaderboard(log)

        if health <= 0:
            print(f"{hero_name} падает без сил. Болото забирает ещё одного искателя сладостей.")
            outcome = "гибель"
            running = False

        if running:
            actions += 1

        print()
        print(f"Здоровье: {health} Запас сил: {stamina} Врагов осталось: {len(enemies)}")
        print()

except KeyboardInterrupt:
    print()
    print("Ты резко останавливаешься и решаешь покинуть эти места.")

finally:
    print(frame)
    if outcome == "гибель":
        print(f"Твое путешествие окончено, {hero_name}. Действий совершено: {actions}.")
    elif outcome == "выход":
        print(f"Ты благополучно выбрался из болота, {hero_name}! Действий совершено: {actions}.")
        print(f"Хорошего пути, искатель сладостей!")
    else:
        print(f"Сеанс прерван, {hero_name}. Действий совершено: {actions}.")

    print_run_summary(log)
    print(frame)