#!/usr/bin/env python3

# A quick and dirty way to draw a pixel grid out

import pygame
 
def main():
    width, height = 40, 6
    pix_size = 15
    off_x, off_y = 1, 1
    screen_size = (
        (width + 2) * pix_size,
        (height + 2 + 2) * pix_size,
    )
    bits = set()

    def dump_bits():
        print("-" * 100)
        row = ""
        for x, y in sorted(bits):
            row += f"({x},{y}),"
            if len(row) >= 100:
                print(row)
                row = ""
        print(row)

    pygame.font.init()
    font = pygame.font.SysFont('Segoe UI', 10)
    buttons = [
        (1, height + 2, font.render("Dump grid", False, (255, 255, 255)), dump_bits),
    ]

    pygame.init()
    pygame.display.set_caption("Bits and Bits")

    screen = pygame.display.set_mode(screen_size)
    running = True

    set_to = None
    def toggle(x, y, force=None):
        if x >= pix_size and y >= pix_size and x < pix_size * (width + 1) and y < pix_size * (height + 1):
            x = (x // pix_size) - 1
            y = (y // pix_size) - 1
            if force is None:
                if (x, y) in bits:
                    bits.remove((x, y))
                    return False
                else:
                    bits.add((x, y))
                    return True
            else:
                if force:
                    if (x, y) not in bits:
                        bits.add((x, y))
                else:
                    if (x, y) in bits:
                        bits.remove((x, y))
                return force
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                set_to = toggle(event.pos[0], event.pos[1])
                if set_to is None:
                    for x, y, _, func in buttons:
                        if x * pix_size <= event.pos[0] <= (x + 10) * pix_size:
                            if y * pix_size <= event.pos[1] <= (y + 1) * pix_size:
                                func()
            elif event.type == pygame.MOUSEBUTTONUP:
                set_to = None
            elif event.type == pygame.MOUSEMOTION:
                if set_to is not None:
                    toggle(event.pos[0], event.pos[1], set_to)

        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_size[0], screen_size[1]))
        for x in range(width + 1):
            pygame.draw.line(screen, (128, 128, 128), ((x + off_x) * pix_size, off_y * pix_size), ((x + off_x) * pix_size, (height + off_y) * pix_size))
        for y in range(height + 1):
            pygame.draw.line(screen, (128, 128, 128), (off_x * pix_size, (y + off_y) * pix_size), ((width + off_x) * pix_size, (y + off_y) * pix_size))

        for x, y, text, _ in buttons:
            pygame.draw.rect(screen, (255, 255, 255), (x * pix_size, y * pix_size, (10) * pix_size, (1) * pix_size))
            pygame.draw.rect(screen, (92, 92, 92), (x * pix_size+1, y * pix_size+1, (10) * pix_size-2, (1) * pix_size-2))
            screen.blit(text, (x * pix_size+1, y * pix_size+1))

        for x, y in bits:
            pygame.draw.rect(screen, (255, 255, 255), ((x + off_x) * pix_size, (y + off_y) * pix_size, pix_size, pix_size))

        pygame.display.flip()

if __name__=="__main__":
    main()
