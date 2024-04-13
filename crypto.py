from stegano import lsb

def string_to_ascii_array(input_string):
    ascii_array = []
    for char in input_string:
        if 'A' <= char <= 'Z':
            ascii_array.append(ord(char))
    return ascii_array

def ascii_array_to_string(ascii_array):
    output_string = ""
    for ascii_value in ascii_array:
        output_string += chr(ascii_value)
    return output_string

def caesar_cipher_encrypt(plaintext, shift):
    arr = string_to_ascii_array(plaintext.upper())

    for i in range(len(arr)):
        if 'A' <= chr(arr[i]) <= 'Z':
            arr[i] = (arr[i] + shift - ord('A')) % 26 + ord('A')

    return ascii_array_to_string(arr)
def caesar_cipher_decrypt(ciphertext, shift):
    arr = string_to_ascii_array(ciphertext.upper())

    for i in range(len(arr)):
        arr[i] = (arr[i] - shift) % 26 + ord('A') if 'A' <= chr(arr[i]) <= 'Z' else arr[i]

    return ascii_array_to_string(arr)


def hide_text_in_image(input_image_path, text_to_hide, output_image_path):
    try:
        secret = lsb.hide(input_image_path, text_to_hide)
        secret.save(output_image_path)
        return "Text successfully hidden in the image."
    except Exception as e:
        return f"Error hiding text: {str(e)}"

def extract_text_from_image(input_image_path):
    try:
        secret = lsb.reveal(input_image_path)
        extracted_text = secret.decode()
        return extracted_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"