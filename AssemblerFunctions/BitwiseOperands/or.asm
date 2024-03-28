global _start

section .data
num1 dq 0, 4, 3
num2 dq 0, 5, 5

section .text
%macro __macroOr 3
	push %3
	push %2
	push %1
	call __or
    add rsp, 24
%endmacro

_start:
	__macroOr num1, num2, 3

    mov rax, 60
	mov rdi, [num1+16]
	syscall

__or:
	push rax
	push rbx
	push rcx
	mov rax, [rsp+32]
	mov rbx, [rsp+40]
	mov rcx, [rsp+48]
	dec rcx
	shl rcx, 3
	add rax, rcx
	add rbx, rcx

__orLoop:
	mov rcx, [rbx]
	or [rax], rcx

	sub rax, 8
	sub rbx, 8

	cmp rax, [rsp+32]
	jge __orLoop

	pop rcx
	pop rbx
	pop rax
	ret
