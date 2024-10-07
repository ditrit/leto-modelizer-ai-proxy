import sys
from src.handlers.Factory import Factory


def main() -> None:
    """
    Main function to be called for initializing all AI
    """
    Factory.initialize_models()
    return 0


if __name__ == "__main__":
    sys.exit(main())
