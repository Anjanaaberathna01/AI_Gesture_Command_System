
from scroll_controller import ScrollController

def main():

    scroll_controller = ScrollController(
        scroll_threshold=0.015,
        scroll_amount=3
    )

    print("\nTesting Scroll Up...")

    scroll_controller.scroll(0.60)
    scroll_controller.scroll(0.55)
    scroll_controller.scroll(0.50)

    print("\nTesting Scroll Down...")

    scroll_controller.scroll(0.50)
    scroll_controller.scroll(0.60)
    scroll_controller.scroll(0.70)

    print("\nTesting Small Movement...")

    scroll_controller.scroll(0.70)
    scroll_controller.scroll(0.705)

    print("\nScroll Controller Test Completed!")


if __name__ == "__main__":
    main()
