import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualizer")

# Define colors suitable for text visibility
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)  # Light blue color

# Fonts
FONT = pygame.font.SysFont('Arial', 20)
LARGE_FONT = pygame.font.SysFont('Arial', 40)

# Global variables
array = []
array_colors = []
num_elements = 10  # Number of elements
sorting = False
ascending = True
algorithm_name = "Bubble Sort"
sorting_algorithms = {}
algorithm_generator = None
input_mode = True  # Start in input mode

# TextBox class for input fields
class TextBox:
    def __init__(self, x, y, w, h, index):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = ''
        self.txt_surface = FONT.render(self.text, True, LIGHT_BLUE)
        self.active = False
        self.index = index  # Position in the array

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if the user clicked on the textbox
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Change the color of the textbox
            self.color = WHITE if self.active else GRAY

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # User pressed Enter
                    self.active = False
                    self.color = GRAY
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    self.text = self.text[:-1]
                else:
                    # Add character if it's a digit
                    if event.unicode.isdigit():
                        self.text += event.unicode
                # Re-render the text with light blue color
                self.txt_surface = FONT.render(self.text, True, LIGHT_BLUE)

    def draw(self, window):
        # Blit the rect
        pygame.draw.rect(window, self.color, self.rect, 2)
        # Blit the text
        window.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

# Sorting Algorithms
def bubble_sort(array, draw_array, delay):
    n = len(array)
    for i in range(n):
        for j in range(n - i - 1):
            num1 = array[j]
            num2 = array[j + 1]
            # Highlight the numbers being compared
            draw_array({j: RED, j + 1: RED}, True)
            yield True
            pygame.time.delay(int(delay * 1000))
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                array[j], array[j + 1] = array[j + 1], array[j]
                # Highlight the swap
                draw_array({j: GREEN, j + 1: GREEN}, True)
                yield True
                pygame.time.delay(int(delay * 1000))
    return array

def insertion_sort(array, draw_array, delay):
    for i in range(1, len(array)):
        current = array[i]
        j = i - 1
        while j >= 0 and ((array[j] > current and ascending) or (array[j] < current and not ascending)):
            array[j + 1] = array[j]
            draw_array({j + 1: RED, j: RED}, True)
            yield True
            pygame.time.delay(int(delay * 1000))
            j -= 1
        array[j + 1] = current
        draw_array({j + 1: GREEN}, True)
        yield True
        pygame.time.delay(int(delay * 1000))
    return array

def selection_sort(array, draw_array, delay):
    n = len(array)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_array({min_idx: RED, j: BLUE}, True)
            yield True
            pygame.time.delay(int(delay * 1000))
            if (array[j] < array[min_idx] and ascending) or (array[j] > array[min_idx] and not ascending):
                min_idx = j
                draw_array({min_idx: RED}, True)
                yield True
                pygame.time.delay(int(delay * 1000))
        array[i], array[min_idx] = array[min_idx], array[i]
        draw_array({i: GREEN, min_idx: GREEN}, True)
        yield True
        pygame.time.delay(int(delay * 1000))
    return array

def merge_sort(array, left, right, draw_array, delay):
    if left >= right:
        return
    mid = (left + right) // 2
    yield from merge_sort(array, left, mid, draw_array, delay)
    yield from merge_sort(array, mid + 1, right, draw_array, delay)
    yield from merge(array, left, mid, right, draw_array, delay)

def merge(array, left, mid, right, draw_array, delay):
    left_copy = array[left:mid + 1]
    right_copy = array[mid + 1:right + 1]
    left_idx = 0
    right_idx = 0
    sorted_idx = left

    while left_idx < len(left_copy) and right_idx < len(right_copy):
        if (left_copy[left_idx] <= right_copy[right_idx] and ascending) or (left_copy[left_idx] >= right_copy[right_idx] and not ascending):
            array[sorted_idx] = left_copy[left_idx]
            left_idx += 1
        else:
            array[sorted_idx] = right_copy[right_idx]
            right_idx += 1
        draw_array({sorted_idx: GREEN}, True)
        yield True
        pygame.time.delay(int(delay * 1000))
        sorted_idx += 1

    while left_idx < len(left_copy):
        array[sorted_idx] = left_copy[left_idx]
        left_idx += 1
        draw_array({sorted_idx: GREEN}, True)
        yield True
        pygame.time.delay(int(delay * 1000))
        sorted_idx += 1

    while right_idx < len(right_copy):
        array[sorted_idx] = right_copy[right_idx]
        right_idx += 1
        draw_array({sorted_idx: GREEN}, True)
        yield True
        pygame.time.delay(int(delay * 1000))
        sorted_idx += 1

def quick_sort(array, low, high, draw_array, delay):
    if low < high:
        pivot_idx = yield from partition(array, low, high, draw_array, delay)
        yield from quick_sort(array, low, pivot_idx - 1, draw_array, delay)
        yield from quick_sort(array, pivot_idx + 1, high, draw_array, delay)

def partition(array, low, high, draw_array, delay):
    pivot = array[high]
    i = low - 1
    draw_array({high: RED}, True)
    yield True
    pygame.time.delay(int(delay * 1000))
    for j in range(low, high):
        draw_array({j: BLUE, high: RED}, True)
        yield True
        pygame.time.delay(int(delay * 1000))
        if (array[j] <= pivot and ascending) or (array[j] >= pivot and not ascending):
            i += 1
            array[i], array[j] = array[j], array[i]
            draw_array({i: GREEN, j: GREEN}, True)
            yield True
            pygame.time.delay(int(delay * 1000))
    array[i + 1], array[high] = array[high], array[i + 1]
    draw_array({i + 1: GREEN, high: GREEN}, True)
    yield True
    pygame.time.delay(int(delay * 1000))
    return i + 1

# Helper Functions
def generate_array():
    global array_colors
    array_colors = [GRAY] * len(array)

def draw_array(color_positions={}, clear_bg=False):
    if clear_bg:
        window.fill(BLACK)
    else:
        pygame.draw.rect(window, BLACK, (0, 150, WIDTH, HEIGHT - 150))

    num_elements = len(array)
    gap = WIDTH / num_elements  # Space between numbers
    for i, val in enumerate(array):
        x = i * gap + gap / 2
        y = HEIGHT / 2
        color = array_colors[i]

        if i in color_positions:
            color = color_positions[i]

        # Render the number with light blue color if default, else use the color provided
        number_color = color if color != GRAY else LIGHT_BLUE

        # Render the number
        number_surface = LARGE_FONT.render(str(val), True, number_color)
        number_rect = number_surface.get_rect(center=(x, y))
        window.blit(number_surface, number_rect)

    pygame.display.update()

def draw_ui():
    window.fill(BLACK)
    if input_mode:
        title = LARGE_FONT.render("Enter 10 Numbers", True, WHITE)
        window.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

        instructions = FONT.render("Click on a box and type a number. Press Enter when done.", True, WHITE)
        window.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, 60))

        # Draw textboxes
        for textbox in textboxes:
            textbox.draw(window)
    else:
        title = LARGE_FONT.render("Sorting Algorithm Visualizer", True, WHITE)
        window.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

        instructions = FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", True, WHITE)
        window.blit(instructions, (10, 60))

        algorithms_text = FONT.render("B - Bubble | I - Insertion | S - Selection | M - Merge | Q - Quick", True, WHITE)
        window.blit(algorithms_text, (10, 90))

        current_algorithm = FONT.render(f"Current Algorithm: {algorithm_name}", True, WHITE)
        window.blit(current_algorithm, (10, 120))

# Main Function
def main():
    global sorting, ascending, algorithm_name, algorithm_generator, input_mode, array

    sorting_algorithms['Bubble Sort'] = lambda: bubble_sort(array, draw_array, 0.5)
    sorting_algorithms['Insertion Sort'] = lambda: insertion_sort(array, draw_array, 0.5)
    sorting_algorithms['Selection Sort'] = lambda: selection_sort(array, draw_array, 0.5)
    sorting_algorithms['Merge Sort'] = lambda: merge_sort(array, 0, len(array) - 1, draw_array, 0.5)
    sorting_algorithms['Quick Sort'] = lambda: quick_sort(array, 0, len(array) - 1, draw_array, 0.5)

    # Initialize TextBoxes
    global textboxes
    textboxes = []
    textbox_width = 60
    textbox_height = 40
    gap = 10
    start_x = (WIDTH - (textbox_width * num_elements + gap * (num_elements - 1))) // 2
    start_y = HEIGHT // 2 - 50

    for i in range(num_elements):
        x = start_x + i * (textbox_width + gap)
        y = start_y
        textbox = TextBox(x, y, textbox_width, textbox_height, i)
        textboxes.append(textbox)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        if input_mode:
            draw_ui()
            pygame.display.update()
        else:
            if sorting:
                try:
                    next(algorithm_generator)
                except StopIteration:
                    sorting = False
            else:
                draw_ui()
                draw_array()
                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if input_mode:
                for textbox in textboxes:
                    textbox.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Check if all textboxes have valid inputs
                        valid_input = True
                        user_array = []
                        for textbox in textboxes:
                            try:
                                value = int(textbox.text)
                                user_array.append(value)
                            except ValueError:
                                valid_input = False
                                break
                        if valid_input:
                            array = user_array
                            generate_array()
                            input_mode = False
                        else:
                            # Show error message
                            error_message = FONT.render("Invalid input! Press enter after ALL boxes are filled.", True, RED)
                            window.blit(error_message, (WIDTH // 2 - error_message.get_width() // 2, HEIGHT - 50))
                            pygame.display.update()
                            pygame.time.delay(2000)  # Pause to show the message
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        input_mode = True
                        sorting = False
                        # Clear textboxes for new input
                        for textbox in textboxes:
                            textbox.text = ''
                            textbox.txt_surface = FONT.render('', True, LIGHT_BLUE)
                    elif event.key == pygame.K_SPACE and not sorting:
                        sorting = True
                        algorithm_generator = sorting_algorithms[algorithm_name]()
                    elif event.key == pygame.K_a:
                        ascending = True
                    elif event.key == pygame.K_d:
                        ascending = False
                    elif event.key == pygame.K_b:
                        algorithm_name = "Bubble Sort"
                    elif event.key == pygame.K_i:
                        algorithm_name = "Insertion Sort"
                    elif event.key == pygame.K_s:
                        algorithm_name = "Selection Sort"
                    elif event.key == pygame.K_m:
                        algorithm_name = "Merge Sort"
                    elif event.key == pygame.K_q:
                        algorithm_name = "Quick Sort"

    pygame.quit()

if __name__ == "__main__":
    main()
