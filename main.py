"""The Self-Checkout Is Judging You — one funny line, deterministic.

Writes a single remark in the voice of a smug self-checkout machine
(79 characters, one line, no trailing newline) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output). Standard library only;
no network, no randomness, no clock — the same bytes on every run.
"""
import os

# The line is held as its three beats so the basket, the machine's
# verdict and the sting stay separately readable; the entry text is
# their join, unchanged.
BASKET = "Twelve yoghurts and a single banana."
VERDICT = "I ran the numbers."
STING = "This is a cry for help."
LINE = f"{BASKET} {VERDICT} {STING}"


def validate_entry(text: str) -> str:
    """Check *text* against the competition gate; return it unchanged.

    Raises ValueError with a specific reason instead of relying on
    module-level asserts, which Python strips under ``-O`` — the gate
    must hold on every run, optimised or not.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    text.encode("utf-8")  # raises UnicodeEncodeError if not UTF-8 encodable
    return text


def main() -> None:
    entry = validate_entry(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    # The grader collects the output as another user: leave it readable.
    try:
        os.chmod(path, 0o644)
        os.chmod(out_dir, 0o755)
    except OSError:
        pass


if __name__ == "__main__":
    main()
