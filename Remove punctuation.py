
import string
def remove_punctuation(text):
return text.translate(str.maketrans('', '', string.punctuation))
# Example usage
text = "Hello, world! Let's remove punctuation."
clean_text = remove_punctuation(text)
print(clean_text)
output
Hello world Lets remove punctuation