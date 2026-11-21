"""A small greeting application for the Jenkins lab."""


def greet(name):
    """Return the personalized greeting required by the lab."""
    return f"Hello, {name} from Ali Naji!"


if __name__ == "__main__":
    print(greet("World"))
