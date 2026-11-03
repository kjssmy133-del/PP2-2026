import turtle
t = turtle.Turtle()
t.shape('turtle')

def square (lenght):
    for i in range(4):
        t.forward(lenght)
        t.left(90)

lenght = int(input('한 변의 길이: '))
square(lenght)
