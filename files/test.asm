LOCATE 0
ADDI $0,$1,1        ; $1=1
SLL $1,$2,7
SW $0,$2,256        ; terminal   -> 128
SW $0,$2,257        ; uart_tx    -> 128
SW $0,$1,258        ; uart_tx_en -> 1
NOP
NOP
NOP
NOP
NOP
SW $0,$0,258        ; uart_tx_en <- 0
BEQ $0,$0,-0