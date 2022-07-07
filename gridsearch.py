import pygame as pg
from time import sleep


def find_shortest_path(start, end, block):
    cost = []
    prev_grid = []
    visited = []
    for __ in range(20):
        cost.append([0 for _ in range(20)])
        prev_grid.append([None for _ in range(20)])
        visited.append([False for _ in range(20)])
    for point in block:
        cost[point[0]][point[1]] = 400  # let 400 be infinite :)
        visited[point[0]][point[1]] = True  # because we have already visited it
    queue = []  # BFS queue
    point = start
    while point != end:
        if point[0] > 0 and not visited[point[0] - 1][point[1]]:
            queue.append((point[0] - 1, point[1]))
            cost[point[0] - 1][point[1]] = cost[point[0]][point[1]] + 1
            prev_grid[point[0] - 1][point[1]] = (point[0], point[1])
            visited[point[0] - 1][point[1]] = True

        if point[1] > 0 and not visited[point[0]][point[1] - 1]:
            queue.append((point[0], point[1] - 1))
            cost[point[0]][point[1] - 1] = cost[point[0]][point[1]] + 1
            prev_grid[point[0]][point[1] - 1] = (point[0], point[1])
            visited[point[0]][point[1] - 1] = True

        if point[0] < 19 and not visited[point[0] + 1][point[1]]:
            queue.append((point[0] + 1, point[1]))
            cost[point[0] + 1][point[1]] = cost[point[0]][point[1]] + 1
            prev_grid[point[0] + 1][point[1]] = (point[0], point[1])
            visited[point[0] + 1][point[1]] = True

        if point[1] < 19 and not visited[point[0]][point[1] + 1]:
            queue.append((point[0], point[1] + 1))
            cost[point[0]][point[1] + 1] = cost[point[0]][point[1]] + 1
            prev_grid[point[0]][point[1] + 1] = (point[0], point[1])
            visited[point[0]][point[1] + 1] = True

        if len(queue) == 0:
            break
        else:
            point = queue.pop(0)
    points = []
    if point == end:
        while True:
            point = prev_grid[point[0]][point[1]]
            if point != start:
                points.append(point)
            else:
                break
    for point in points:
        # nothing given as width implies to fill the circle with color
        pg.draw.circle(image_layer, (150, 100, 250), (35 * point[0] + 14, 35 * point[1] + 14), 10)
    display_window.update()
    sleep(3)


def draw_grid(start, end):
    image_layer.fill((20, 22, 24))
    for x in range(500):
        for y in range(500):
            rect = pg.Rect(x * 35, y * 35, 35, 35)  # 35 is the size of the rectangle
            pg.draw.rect(image_layer, (100, 255, 255), rect, 1)
    # nothing given as width implies to fill the rect with color
    pg.draw.rect(image_layer, (50, 200, 75), pg.Rect(35 * start[0], 35 * start[1], 35, 35))
    pg.draw.rect(image_layer, (200, 50, 75), pg.Rect(35 * end[0], 35 * end[1], 35, 35))


def project_loop():
    block = []
    mark_drag = False
    unmark_drag = False
    start = (0, 0)
    end = (19, 19)
    while True:
        draw_grid(start, end)
        for each in block:
            # nothing given as width implies to fill the rect with color
            pg.draw.rect(image_layer, (100, 255, 255), pg.Rect(each[0] * 35, each[1] * 35, 35, 35))
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()  # for system-exit
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                find_shortest_path(start, end, block)
            if event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
                block = []  # reset grids

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                ptr = pg.mouse.get_pos()
                ptr = (ptr[0] // 35, ptr[1] // 35)
                if clock.tick() < 500:  # detects double click if its not used for another issues of the program
                    start = ptr
                    if start in block:
                        block.remove(start)
                elif ptr != start and ptr != end and ptr not in block:
                    block.append(ptr)
                    mark_drag = True
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mark_drag = False
            if event.type == pg.MOUSEMOTION and mark_drag:
                ptr = pg.mouse.get_pos()
                ptr = (ptr[0] // 35, ptr[1] // 35)
                if ptr != (0, 0) and ptr != (19, 19) and ptr not in block:
                    block.append(ptr)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                ptr = pg.mouse.get_pos()
                ptr = (ptr[0] // 35, ptr[1] // 35)
                if clock.tick() < 500:  # detects double click if its not used for another issues of the program
                    end = ptr
                    if end in block:
                        block.remove(end)
                elif ptr != start and ptr != end and ptr in block:
                    block.remove(ptr)
                    unmark_drag = True
            if event.type == pg.MOUSEBUTTONUP and event.button == 3:
                unmark_drag = False
            if event.type == pg.MOUSEMOTION and unmark_drag:
                ptr = pg.mouse.get_pos()
                ptr = (ptr[0] // 35, ptr[1] // 35)
                if ptr != (0, 0) and ptr != (19, 19) and ptr in block:
                    block.remove(ptr)

        display_window.update()


pg.init()  # initiate PYGAME ...
clock = pg.time.Clock()
display_window = pg.display  # getting the background display,other layers of images
image_layer = display_window.set_mode((700, 700))
display_window.set_caption("GRID PATH")
project_loop()
