from stegano import lsb

def string_to_ascii_array(input_string):
    """
    Converts a string to an ASCII array containing only uppercase letters.

    Args:
        input_string (str): The input string to convert.

    Returns:
        list: The ASCII array containing ASCII values of uppercase letters.
    """
    ascii_array = []
    for char in input_string:
        if 'A' <= char <= 'Z':
            ascii_array.append(ord(char))
    return ascii_array

def ascii_array_to_string(ascii_array):
    """
    Converts an ASCII array back to a string.

    Args:
        ascii_array (list): The ASCII array containing ASCII values.

    Returns:
        str: The converted string.
    """
    output_string = ""
    for ascii_value in ascii_array:
        output_string += chr(ascii_value)
    return output_string

def caesar_cipher_encrypt(plaintext, shift):
    """
    Encrypts a plaintext using the Caesar cipher with a specified shift.

    Args:
        plaintext (str): The plaintext to encrypt.
        shift (int): The shift value for encryption.

    Returns:
        str: The encrypted ciphertext.
    """
    arr = string_to_ascii_array(plaintext.upper())

    for i in range(len(arr)):
        if 'A' <= chr(arr[i]) <= 'Z':
            arr[i] = (arr[i] + shift - ord('A')) % 26 + ord('A')

    return ascii_array_to_string(arr)

def caesar_cipher_decrypt(ciphertext, shift):
    """
    Decrypts a Caesar cipher ciphertext using a specified shift.

    Args:
        ciphertext (str): The ciphertext to decrypt.
        shift (int): The shift value for decryption.

    Returns:
        str: The decrypted plaintext.
    """
    arr = string_to_ascii_array(ciphertext.upper())

    for i in range(len(arr)):
        arr[i] = (arr[i] - shift) % 26 + ord('A') if 'A' <= chr(arr[i]) <= 'Z' else arr[i]

    return ascii_array_to_string(arr)

def hide_text_in_image(input_image_path, text_to_hide, output_image_path):
    """
    Hides text in an image using the LSB technique from the Stegano library.

    Args:
        input_image_path (str): The path to the input image.
        text_to_hide (str): The text to hide in the image.
        output_image_path (str): The path to save the output image with hidden text.

    Returns:
        str: A success message if text is hidden successfully, or an error message otherwise.
    """
    try:
        secret = lsb.hide(input_image_path, text_to_hide)
        secret.save(output_image_path)
        return "Text successfully hidden in the image."
    except Exception as e:
        return f"Error hiding text: {str(e)}"

def extract_text_from_image(input_image_path):
    """
    Extracts hidden text from an image using the LSB technique from the Stegano library.

    Args:
        input_image_path (str): The path to the input image.

    Returns:
        str: The extracted hidden text, or an error message if extraction fails.
    """
    try:
        secret = lsb.reveal(input_image_path)
        extracted_text = secret.decode()
        return extracted_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"
