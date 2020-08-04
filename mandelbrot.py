import pygame
import numpy as np

class Mandelbrot:

    def __init__(self, width, height):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.canvas = pygame.display.set_mode((width, height))

        # canvas coordinate
        self.canvas_width = width
        self.canvas_height = height
        self.canvas_scale = 4

        # math coordinate
        self.center_x = 0
        self.center_y = 0

        self.max_iter = 50
        self.move_speed = 0.1
        self.dilation = 1
    
    # return -1 if stable, else return the iteration number
    # when the distance to origin is greater than 2
    def iterate(self, c):
        z = np.zeros(c.shape)
        count = np.zeros(c.shape)
        stable = np.tile(True, c.shape)
        for i in range(self.max_iter):
            z = (z * stable) ** 2 + c
            stable = stable * (z <= 2)
            count = count + stable
        return count == self.max_iter

    def canvas_to_math_coord(self, canvas_x, canvas_y):

        dist_per_pixel = self.canvas_scale / self.canvas_width
        canvas_dx = canvas_x - self.canvas_width / 2
        canvas_dy = canvas_y - self.canvas_height / 2
        x = self.center_x + canvas_dx * dist_per_pixel
        y = self.center_y - canvas_dy * dist_per_pixel

        return x, y

    def generate_mandelbrot_map(self):
        canvas_x = np.arange(0, self.canvas_width, self.dilation)
        canvas_y = np.arange(0, self.canvas_height, self.dilation)
        x, y = self.canvas_to_math_coord(canvas_x, canvas_y)
        x_len, y_len = len(x), len(y)
        x = np.tile(x, (y_len, 1))
        y = np.tile(y, (x_len, 1)).T * 1j
        mandelbrot_map = self.iterate(x + y)
        return mandelbrot_map

    def draw(self):
        
        mandelbrot_map = self.generate_mandelbrot_map()
        map_height, map_width = mandelbrot_map.shape
        self.canvas.fill((0, 0, 0))
        for y in range(map_height):
            for x in range(map_width):
                if mandelbrot_map[y][x]:
                    pygame.draw.circle(self.canvas, (255, 255, 255), (x * self.dilation, y * self.dilation), 0)
        pygame.display.update()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(6)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x, y = self.canvas_to_math_coord(mouse_x, mouse_y)
                    if event.button == 1: # left click centers view around cursor
                        self.center_x = x
                        self.center_y = y

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: # left arrow move view to the left
                        self.center_x -= self.canvas_scale * self.move_speed
                    elif event.key == pygame.K_RIGHT: # right arrow move view to the right
                        self.center_x += self.canvas_scale * self.move_speed
                    elif event.key == pygame.K_UP: # up arrow move view up
                        self.center_y += self.canvas_scale * self.move_speed
                    elif event.key == pygame.K_DOWN: # down arrwo move view down
                        self.center_y -= self.canvas_scale * self.move_speed
                    elif event.key == pygame.K_z: # z key zoom in by a factor of 2
                        self.canvas_scale /= 2
                    elif event.key == pygame.K_x: # x key zoom out by a factor of 2
                        self.canvas_scale *= 2
                    elif event.key == pygame.K_e: # e key print current x, y, zoom, iter, dilation
                        print(f"x: {self.center_x}, y: {self.center_y}, scale: {self.canvas_scale}, iter: {self.max_iter}, dilation: {self.dilation}")
                    elif event.key == pygame.K_a: # a key increase iteration by 10
                        self.max_iter += 10
                    elif event.key == pygame.K_s: # s key decrease iteration by 10 (min 50)
                        self.max_iter = max(50, self.max_iter - 10)
                    elif event.key == pygame.K_w: # w key increase dilation factor
                        self.dilation += 1
                    elif event.key == pygame.K_q: # q key decrease dilation factor
                        self.dilation = max(1, self.dilation - 1)
            self.draw()
            
if __name__ == "__main__":
    m = Mandelbrot(1000, 1000)
    m.run()