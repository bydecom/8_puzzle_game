import pygame
import sys
import random
from Find_A import Find
import time
# import Cut_Image as cut
# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
screen_width, screen_height = 900, 600

screen = pygame.display.set_mode((screen_width, screen_height))
background_color = (0, 0, 0)
pygame.display.set_caption("8-Puzzle-A*")


# Màu cho các ô vuông
tile_color = (0, 0, 0)

# Kích thước của lưới và số ô vuông theo chiều ngang và dọc
grid_size = 3
tile_size = 600 // grid_size

#thay ảnh
def set_images(grid_size):
    if grid_size == 3:
        return [pygame.image.load(f'images/3x3/image{i}.png') for i in range(grid_size**2)]
    elif grid_size == 4:
        return [pygame.image.load(f'images/4x4/image{i}.png') for i in range(grid_size**2)]
    elif grid_size == 5:
        return [pygame.image.load(f'images/5x5/image{i}.png') for i in range(grid_size**2)]

def generate_winning_state(grid_size):
    winning_state = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            if i == grid_size - 1 and j == grid_size - 1:
                row.append(0)
            else:
                row.append(i * grid_size + j + 1)
        winning_state.append(row)
    return winning_state



# Hàm tạo trạng thái ban đầu ngẫu nhiên
def generate_random_state(grid_size):
    goal_state = generate_winning_state(grid_size)
    state = [row[:] for row in goal_state]  # Copy the winning state

    # Shuffle the puzzle by performing random valid moves
    for _ in range(50):
        possible_moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        move = random.choice(possible_moves)
        state = move_blank(state, move)

    return state


# Hàm vẽ lưới và các ô vuông
images = set_images(grid_size)

def draw_grid(state):
    images = set_images(grid_size)
    screen.fill(background_color)
    pygame.draw.rect(screen, (0, 128, 255), (600, 0, 300, 600))
    for row in range(grid_size):
        for col in range(grid_size):
            number = state[row][col]
            if number!=0:
                image = images[number]
                screen.blit(image, (col * tile_size, row * tile_size))
    exit_button.draw()
    random_button.clicked=False
    three_button.clicked = False
    four_button.clicked = False
    five_button.clicked = False
    random_button.draw()
    auto_button.draw()
    three_button.draw()
    four_button.draw()
    five_button.draw()
    pygame.display.flip()


class Button:
    def __init__(self, x, y, path, scale):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.visible = True

    def draw(self):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True



exit_button = Button(700, 500, "images/exit_btn.png",0.4)
auto_button = Button(700, 300, "images/auto_btn.png",0.4)
random_button = Button(700, 400, "images/random_btn.png",0.4)
three_button = Button(600, 50, "images/3x3.png",0.4)
four_button = Button(700, 50, "images/4x4.png",0.4)
five_button = Button(800, 50, "images/5x5.png",0.4)


# Hàm di chuyển ô trống
def move_blank(state, direction):
    x, y = get_blank_position(state)
    new_x, new_y = x, y

    if direction == "LEFT" and y > 0:
        new_x, new_y = x, y - 1
    elif direction == "RIGHT" and y < grid_size - 1:
        new_x, new_y = x, y + 1
    elif direction == "UP" and x > 0:
        new_x, new_y = x - 1, y
    elif direction == "DOWN" and x < grid_size - 1:
        new_x, new_y = x + 1, y

    state[x][y], state[new_x][new_y] = state[new_x][new_y], state[x][y]
    return state


# Hàm kiểm tra xem trò chơi đã chiến thắng chưa
def is_winning_state(state):
    winning_state = generate_winning_state(grid_size)
    return state == winning_state


# Hàm tìm vị trí của ô trống
def get_blank_position(state):
    for row in range(grid_size):
        for col in range(grid_size):
            if state[row][col] == 0:
                return row, col


# Trạng thái ban đầu
initial_state = generate_random_state(grid_size)
new_state=initial_state
o=0
# Vòng lặp chính
key_pressed = False
# Tạo biến để kiểm tra xem sự kiện phím đã xảy ra hay chưa
key_pressed = False


# Vòng lặp chính
running = True
draw_grid(initial_state)
while running:
    for event in pygame.event.get():
        move_map = []
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not key_pressed:  # Chỉ xử lý sự kiện phím nếu chưa có sự kiện phím trước đó
                key_pressed = True  # Đánh dấu sự kiện phím đã xảy ra
                if event.key == pygame.K_UP:
                    move_blank(initial_state, "UP")
                elif event.key == pygame.K_DOWN:
                    move_blank(initial_state, "DOWN")
                elif event.key == pygame.K_LEFT:
                    move_blank(initial_state, "LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_blank(initial_state, "RIGHT")
        else:
            key_pressed = False  # Đặt lại biến key_pressed khi không có sự kiện phím
        if exit_button.clicked == True:
            running = False
        if three_button.clicked == True:
            grid_size = 3
            tile_size = 600 // grid_size
            images = [pygame.image.load(f'images/3x3/image{i}.png') for i in range(grid_size ** 2)]
        if four_button.clicked == True:
            four_button.clicked == True
            grid_size = 4
            tile_size = 600 // grid_size
            images = [pygame.image.load(f'images/4x4/image{i}.png') for i in range(grid_size ** 2)]

            four_button.clicked == False
        if five_button.clicked == True:
            five_button.clicked == True
            grid_size = 5
            tile_size = 600 // grid_size
            images = [pygame.image.load(f'images/5x5/image{i}.png') for i in range(grid_size ** 2)]



        if random_button.clicked == True:
            random_button_clicked = True
            initial_state = generate_random_state(grid_size)
        if auto_button.clicked == True:
            auto_button_clicked = True
            o = 0
            print(True)
            map = initial_state.copy()
            size = grid_size
            x = None
            x = Find(map,size)
            move = x.move
            for _ in move:
                new_map = move_blank(map, _)
                time.sleep(0.25)
                draw_grid(new_map)
                move_map.append(new_map)
            auto_button.clicked = False
        if three_button.clicked or four_button.clicked or five_button.clicked == True:
            new_state = generate_random_state(grid_size)
            initial_state = new_state
            # draw_grid(initial_state)
    draw_grid(initial_state)

    if is_winning_state(initial_state):
        if o ==0:
            print("You won!")
            o = 1


# Kết thúc Pygame
pygame.quit()
sys.exit()



