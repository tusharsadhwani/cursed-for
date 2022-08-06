# coding: cursed_for

def main():
    for (i = 0; i < 10; i += 3):
        for (j = i; j < 10; j += 3):
            print(i, j)
    
    counter = 0
    for (;;):
        if counter > 5:
            break

        print('wat')
        counter += 1
