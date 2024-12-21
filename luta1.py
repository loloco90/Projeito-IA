import random
import matplotlib.pyplot as plt

# Configuração básica
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, opponent):
        damage = random.randint(1, self.attack_power)
        opponent.health -= damage
        return damage

# IA simples que escolhe ações
def train_ai(num_episodes):
    win_count = 0
    results = []

    for episode in range(num_episodes):
        player = Character("AI", 100, 10)
        opponent = Character("Opponent", 100, 10)

        while player.health > 0 and opponent.health > 0:
            # IA decide atacar sempre no início (regra inicial)
            player.attack(opponent)
            if opponent.health <= 0:
                win_count += 1
                break

            # Oponente ataca
            opponent.attack(player)

        results.append(win_count / (episode + 1))  # Taxa de vitória até o momento

    return results

# Treinamento e visualização
results = train_ai(1000)
plt.plot(results)
plt.title("Progresso da IA")
plt.xlabel("Episódios")
plt.ylabel("Taxa de Vitória")
plt.show()
