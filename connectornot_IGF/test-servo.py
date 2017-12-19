import serial, glob, time, servoclass


while True:
    servo = int(raw_input("which motor?\n"))
    servoToMove = servoclass.Servo(servo)
    movement = int(raw_input("input an angle (ccw:80 / stop:90 / cw:100)\n"))
    servoToMove.move(movement)

