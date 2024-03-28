global _start

section .bss
temp resb 1

section .data
num1 dq 0, 0, 32
num2 dq 0, 0, 3

section .text
%macro addI 3
    push 0
    push %3
    push %1
    push %2
    call addNums
    add rsp, 32
%endmacro
_start:
    addI num1, num2, 3

    mov rax, 60
    mov rdi, [num1+16]
    syscall

addNums:
    push r15
    push rdi
    push rsi
    push rax
    push rbx

    mov r15, 0

    mov rdi, [rsp+72]
    mov rsi, [rsp+64]
    dec rsi
    mov rax, [rsp+56]
    mov rbx, [rsp+48]

    shl rsi, 3
    add rax, rsi
    add rbx, rsi        

addNumsLoop:
    push rcx
    push rdx
    mov rcx, [rax]
    mov rdx, [rbx]
    xor [rax], rdx
    and [rbx], rcx
    pop rdx
    pop rcx

    rol qword [rbx], 1

    mov rsi, [rbx]
    and rsi, 1
    sub [rbx], rsi
    add [rbx], rdi
    mov rdi, rsi

    mov rcx, 1
    cmp qword [rbx], qword 0
    cmovne r15, rcx

    sub rax, 8
    sub rbx, 8
    
    cmp rax, num1
    jge addNumsLoop

    mov rsi, [rsp+24]
    shl rsi, 3
    mov rbx, [rsp+8]
    add rbx, rsi

    cmp r15, 1
    je addNums

    pop rbx
    pop rax
    pop rsi
    pop rdi
    pop r15
    ret
