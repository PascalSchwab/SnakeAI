from game import Game
from agent import QAgent
import pygame
import os

def loadRecord():
    file = open("./model/data.txt", "r")
    record = int(file.read())
    file.close()
    return record

def saveRecord(record: int):
    file = open("./model/data.txt", "w")
    file.write(str(record))
    file.close()

def train():
    record = 0
    agent = QAgent()
    game = Game("Snake")

    # Load
    if os.path.exists("./model/data.txt"):
        record = loadRecord()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                agent.model.save()
                saveRecord(record)
                pygame.quit()
                quit()

        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.restart()
            agent.game_count += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()
                saveRecord(record)

            print('Game', agent.game_count, 'Score', score, 'Record:', record)

if __name__ == '__main__':
    train()
