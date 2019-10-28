MOV R0, #0
MOV R3, #0

L1:
ADD R0, R0, #7
ADD R3, R3, #1
CMP R3, #10
JNE L1
; Jump back to self for stopping the control flow.
STUCK: JMP STUCK
