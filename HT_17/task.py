"""
Автоматизувати процес замовлення робота за допомогою Selenium
"""

from process import OrderProcessPlacer


def main():
    """Main function"""
    with OrderProcessPlacer() as opp:
        opp.main_process_order()


if __name__ == '__main__':
    main()
