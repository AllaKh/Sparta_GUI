
import msvcrt
print("Press q to exit")
while True:
    if msvcrt.kbhit():
        key = msvcrt.getch()
        print(key)   # just to show the result
        if key == b'q' :
            break
            
