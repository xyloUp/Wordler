from random import choice, Random

class EditTxt:
    
    path = "./website/scripts/words.txt"

    @staticmethod
    def validate_word(word: str) -> bool:
        """
        checks whether a string contains any invalid characters or is an invalid Length
        """

        def check_symbols() -> bool:
            for char in word:
                if char in [*"!\\`¬$£%^&*()_+=-{]}[@'#~/?.>,<\""]:
                    return False
            
            return True

        return True if len(word) == 5 and check_symbols() is True else False

    @classmethod
    def get_words(cls) -> list[str]:
        """
        Gets All Available Words In words.txt
        """
        with open(cls.path, "r") as f:
            words = [word.strip().lower() for word in f.readlines()]
            return words

    @classmethod
    def get_random_word(cls) -> str:
        """
        gets a random word to use for session
        """
        return choice(cls.get_words()).strip()

    @classmethod
    def remove_word(cls, word: str) -> str:
        """
        Removes a word from words.txt
        """
        if word in (words := cls.get_words()):
            idx = words.index(word)
            words.pop(idx)
        return words

    @classmethod
    def write_words(cls, words):
        """
        Writes a list of words to words.txt
        """
        if words:
            with open(cls.path, "w") as f:
                for word in words:
                    f.write(f"{word}\n")