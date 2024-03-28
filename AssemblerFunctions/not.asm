global _start

section .data
num1 dq 0, 0, 5

section .text
%macro __macroNot 2
	push %2
	push %1
	call __not
    add rsp, 24
%endmacro

_start:
	__macroNot num1, 3

__not:
	push rax
	push rbx
	mov rax, [rsp+24]
	mov rbx, [rsp+32]
	dec rbx
	shl rbx, 3
	add rax, rbx

__notLoop:
	not qword [rax]

	sub rax, 8

	cmp rax, [rsp+24]
	jge __notLoop

	pop rbx
	pop rax
	ret
