package internal

const base62Chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

func Base62Encode(num int) string {

	if num == 0 {
		return "0"
	}
	result := ""
	base := len(base62Chars)
	for num > 0 {
		remainder := num % base
		result = string(base62Chars[remainder]) + result
		num = num / base
	}
	return result
}
