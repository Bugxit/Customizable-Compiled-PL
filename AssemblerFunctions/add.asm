global _start

section .bss
temp resb 1

section .data
num1 dq 0, 0, 18446744073709551615

num2 dq 0, 0, 2

section .text
_start:
    call addNums

    mov rbx, [num1+8]
loop:
    mov rax, rbx
    and rax, 1
    add rax, '0'
    mov [temp], rax
    mov rax, 1
    mov rdi, 1
    mov rsi, temp
    mov rdx, 1
    syscall

    shr rbx, 1

    cmp rbx, 0
    jne loop

    mov rax, 60
    mov rdi, [num1+16]
    syscall

addNums:
    mov rdi, 0
    mov rsi, 0
    lea rax, [num1+16]
    lea rbx, [num2+16]

addNumsLoop:
    mov rcx, [rax]
    mov rdx, [rbx]
    xor [rax], rdx
    and [rbx], rcx

    rol qword [rbx], 1

    mov rsi, [rbx]
    and rsi, 1
    sub [rbx], rsi
    add [rbx], rdi
    mov rdi, rsi

    sub rax, 8
    sub rbx, 8
    
    cmp rax, num1
    jge addNumsLoop

    cmp qword [num2], 0
    jne addNums
    cmp qword [num2+8], 0
    jne addNums
    cmp qword [num2+16], 0
    jne addNums

    ret
