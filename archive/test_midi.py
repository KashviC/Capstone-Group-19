
#Instruct the user to input the file name
import note_to_LED

print("Please input the name of the file")
input = input()

#if(input.split('.')[1].lower() == 'gp'): #identify if its a wav file
 #   print("woof")

if(input.split('.')[1].lower() == 'npy'):
        print("woof2")
        note_to_LED.npyFile(input)