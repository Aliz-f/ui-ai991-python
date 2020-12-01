from smartAgent import SmartAgent
import time

if __name__ == '__main__':
    current_time = time.time()
    winner = SmartAgent().play()
    end_time = time.time()
    total = end_time - current_time
    print(f'the total execution time is {total}')
    print("WINNER: " + winner)
