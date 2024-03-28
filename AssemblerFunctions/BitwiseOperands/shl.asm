global _start

section .data
num1 dq 0, 0, 1
num2 dq 0, 0, 5

section .text
%macro __macroShl 3
	push %3
	push %2
	push %1
	call __shl
    add rsp, 24
%endmacro

_start:
	__macroShl num1, 64, 3

    mov rax, 60
	mov rdi, [num1+8]
	syscall

__shl:
	push rax
	push rbx
	push rcx

    mov rbx, 1

	mov rax, [rsp+32]
	mov rcx, [rsp+48]
	dec rcx
	shl rcx, 3
	add rax, rcx

__shlLoop:
	rol qword [rax], 1

    push rcx
    mov rcx, [rax]
    and rcx, 1

    sub qword [rax], rcx
    push rcx
    mov rcx, [rsp+16]
    add [rax], rcx
    pop rcx
    mov [rsp+8], rcx
    pop rcx

	sub rax, 8

	cmp rax, [rsp+32]
	jge __shlLoop

	mov rax, [rsp+32]
	mov rcx, [rsp+48]
	dec rcx
	shl rcx, 3
	add rax, rcx
    
    inc rbx

    cmp rbx, [rsp+40]
    jle __shlLoop

	pop rcx
	pop rbx
	pop rax
	ret
