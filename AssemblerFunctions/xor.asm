global _start

section .data
num1 dq 0, 0, 0
num2 dq 0, 0, 7

section .text
%macro 3
%endmacro
_start:
	push 3
	push num2
	push num1
	jmp __xor

__xor:
	push rax
	push rbx
	push rcx
	mov rax, [rsp+32]
	mov rbx, [rsp+40]
	mov rcx, [rsp+48]
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

	
