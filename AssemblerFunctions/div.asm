global _start

section .bss
tempP resb 1

section .data
num1 dq 0, 0, 8
num2 dq 0, 0, 2
_tempDiv dq 0, 0, 0
_tempDiv2 dq 0, 0, 0
temp2 dq 0, 0, 0 

section .text
%macro addI 3
    push 0
    push %3
    push %1
    push %2
    call addNums
    pop rbx
    pop rbx
    pop rbx
    pop rbx
%endmacro

%macro subI 3
    push 1
    push %3
    push %1
    push %2
    call subNums
    pop rbx
    pop rbx
    pop rbx
    pop rbx
%endmacro

%macro divI 3
    push %3
    push %1
    push %2
    call divNums
    pop rbx
    pop rbx
    pop rbx
%endmacro
_start:
    divI num1, num2, 3
    mov rbx, [_tempDiv2+16]
loop:
    mov rax, rbx
    and rax, 1
    add rax, '0'
    mov [tempP], rax
    mov rax, 1
    mov rdi, 1
    mov rsi, tempP
    mov rdx, 1
    syscall

    shr rbx, 1

    cmp rbx, 0
    jne loop

    mov rax, 60
    mov rdi, r14
    syscall

divNums:
    mov rax, [rsp+16]
    mov rbx, [rsp+8]
    lea rsi, [_tempDiv]

divCopy:
    mov rcx, [rax]
    cmp rcx, [rbx]
    jl end_func
    
    mov rcx, [rbx]
    mov [rsi], rcx 
    
    add rax, 8
    add rbx, 8
    add rsi, 8

    mov rcx, [rsp+24]
    shl rcx, 3
    add rcx, [rsp+16]
    cmp rcx, rax 
    jge divCopy

    push rbp
    subI qword [rsp+16], qword [rsp+8], qword [rsp+24]
    pop rbp

    mov rsi, [rsp+24]
    shl rsi, 3
    mov rax, [rsp+8]
    add rax, rsi
    mov qword [rax], 1
    sub rax, rsi

    push rbp
    addI _tempDiv2, rax, qword [rsp+24]
    pop rbp

    mov rsi, [rsp+24]
    shl rsi, 3
    mov rbx, [rsp+8]
    lea rax, [_tempDiv]
    add rax, rsi
    add rbx, rsi

divCopyBack:
    mov rcx, [rax]
    mov [rbx], rcx

    sub rax, 8
    sub rbx, 8

    cmp rax, _tempDiv
    jge divCopyBack
    
    jmp divNums


subNums:
    mov rsi, [rsp+24]
    shl rsi, 3
    mov rbx, [rsp+8]
    add rbx, rsi

subNumsNotLoop:
    not qword [rbx]

    sub rbx, 8

    cmp rbx, [rsp+8]
    jge subNumsNotLoop

addNums:
    mov r15, 0
    mov rdi, [rsp+32]
    mov qword [rsp+32], 0
    mov rsi, [rsp+24]
    shl rsi, 3
    mov rax, [rsp+16]
    mov rbx, [rsp+8]
    add rax, rsi
    add rbx, rsi

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

end_func:
    ret
