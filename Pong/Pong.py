# Pong Game in Python
# Alec Gardiner


import turtle

win = turtle.Screen()  # initializes a window
win.title("Pong by Alec")  # Create a title for the window
win.bgcolor("black")  # change the background color
win.setup(width=800, height=600)
win.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)  # speed of animation, set to max
paddle_a.shape("square") # default 20 x 20 pizels
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()  # Turtle objects draw a line as they're moving, this disables that
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)  # speed of animation, set to max
paddle_b.shape("square") # default 20 x 20 pizels
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()  # Turtle objects draw a line as they're moving, this disables that
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)  # speed of animation, set to max
ball.shape("square") # default 20 x 20 pizels
ball.color("white")
ball.penup()  # Turtle objects draw a line as they're moving, this disables that
ball.goto(0, 0)


# Main game loop
while True:
    win.update()

