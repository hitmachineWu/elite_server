import unittest
from src.kg_gen.utils.chunk_text import chunk_text

class TestChunkText(unittest.TestCase):
    def test_single_short_sentence(self):
        """Test that a single short sentence fits in one chunk."""
        text = "Hello world."
        result = chunk_text(text, max_chunk_size=50)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Hello world.")

    def test_multiple_sentences_under_limit(self):
        """Test multiple short sentences that fit in a single chunk."""
        text = "Hello world. This is a test."
        # The total length is well under 50.
        result = chunk_text(text, max_chunk_size=50)
        # Expecting a single chunk, because together they're under 50 chars.
        self.assertEqual(len(result), 1)
        # They should remain combined (with a space in between).
        self.assertEqual(result[0], "Hello world. This is a test.")

    def test_multiple_sentences_exceed_limit(self):
        """Test multiple sentences that exceed the maximum chunk size."""
        text = (
            "Sentence number one is not too long. "
            "Sentence number two might push us over the limit. "
            "Short last sentence."
        )
        # Let's set a small max_chunk_size so chunking is forced.
        result = chunk_text(text, max_chunk_size=50)

        # We expect multiple chunks.
        self.assertTrue(len(result) > 1)

        # Check that no chunk exceeds 50 characters.
        for chunk in result:
            self.assertTrue(len(chunk) <= 50, f"Chunk too long: {chunk}")

    def test_long_sentence_fallback(self):
        """Test a single (extremely long) sentence to ensure it gets split by words."""
        # A single sentence with no internal punctuation. It must be split by words.
        text = " ".join(["word"] * 100) + "."  # 100 'word's in a row
        max_size = 20
        result = chunk_text(text, max_chunk_size=max_size)

        # Check that no chunk is longer than 20 characters
        for chunk in result:
            self.assertTrue(len(chunk) <= max_size, f"Chunk too long: {chunk}")

        # Ensure that all words reappear in the result (minus the final '.')
        combined = " ".join(result)
        # If your chunk_text keeps the final period in the last chunk, adjust accordingly.
        self.assertIn("word", combined)
        # We might also want to check the count of 'word' is correct
        # but that requires carefully handling the punctuation. 
        # This minimal check ensures fallback at least happened.

    def test_mixed_scenario(self):
        """Test a mix of short and long sentences in the same text."""
        text = (
            "Short sentence. " 
            + " ".join(["longword"] * 30) + ". "  # One long sentence
            + "Another short sentence."
        )
        max_size = 50
        result = chunk_text(text, max_chunk_size=max_size)

        # We expect at least 3 chunks:
        #   1) "Short sentence." 
        #   2) The long sentence split by words
        #   3) "Another short sentence."
        self.assertTrue(len(result) >= 3)

        # Check no chunk is over limit
        for chunk in result:
            self.assertTrue(len(chunk) <= max_size, f"Chunk too long: {chunk}")

        # Check the first chunk is "Short sentence."
        self.assertTrue(result[0].startswith("Short sentence."))

        # Check the last chunk contains "Another short sentence."
        self.assertTrue("Another short sentence." in result[-1])

if __name__ == "__main__":
    unittest.main()
