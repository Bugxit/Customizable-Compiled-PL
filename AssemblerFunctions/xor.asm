global _start

section .data
num1 dq 0, 4, 3
num2 dq 0, 5, 5

section .text
%macro __macroXor 3
	push %3
	push %2
	push %1
	call __xor
    add rsp, 24
%endmacro

_start:
	__macroXor num1, num2, 3

    mov rax, 60
	mov rdi, [num1+8]
	syscall

__xor:
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

__xorLoop:
	mov rcx, [rbx]
	xor [rax], rcx

	sub rax, 8
	sub rbx, 8

	cmp rax, [rsp+32]
	jge __xorLoop

	pop rcx
	pop rbx
	pop rax
	ret
