LOCATE  0
ADDI $1, $1, 123    ;$1=$1+123                  ;$1=123
ADDI $1, $2, 456    ;$2=$1+456                  ;$2=579
SW   $0, $2, 10     ;RAM($0+10)=$2              ;RAM(10)=579
LW   $0, $3, 10     ;$3=RAM($0+10)              ;$3=579
ADD  $1, $3, $4     ;$4=$1+$3                   ;$4=702
SUB  $4, $2, $5     ;$5=$4-$2                   ;$5=123
BEQ  $5, $1, 10     ;($5==$1)?(PC+=(10<<2)+4)   ;PC=68
NOP                 ;NOP                        ;NOP

LOCATE  68
SUB  $3, $1, $3     ;$3=$3-$1                   ;$3=456
SW   $0, $3, 256    ;BYTE($3)->terminal         ;terminal=200
NOP                 ;NOP                        ;NOP
NOP                 ;NOP                        ;NOP
NOP                 ;NOP                        ;NOP
NOP                 ;NOP                        ;NOP
NOP                 ;NOP                        ;NOP