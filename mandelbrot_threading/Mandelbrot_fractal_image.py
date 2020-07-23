import threading
import time
import cmath
import pygame
from random import randint, randrange, random

print( 'File:', __file__ )

pygame.init()


scr_w, scr_h = 500, 500
screen = pygame.display.set_mode( (scr_w, scr_h) )
pygame.display.set_caption('Fractal Image: Mandelbrot') 
clock = pygame.time.Clock()
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

first_create = True 
running = True

w2, h2 = scr_w/2, scr_h/2 

def mandelbrot(c,max_iters=100):
    i = 0
    z = complex(0,0)
    while abs(z) <= 2 and i < max_iters:
        z = z*z + c
        i += 1 
    return i

#################################### Threading ###############################
allow_threads_running = True 
thread_w,thread_h = 50,50

def thread_func(id,surface,lock,barrier,sem):
    global allow_threads_running,scr_h,scr_w,thread_w,thread_h,w2, h2

    # while allow_threads_running :

    if sem.acquire(timeout=0.1):

        # with lock :
        #     print('{} start.'.format( threading.currentThread().getName() ) )

        column = int (id % (scr_w/thread_w)) - 1           
        row = int (id / (scr_w/thread_w))  
        if column == -1 : 
            column = int((scr_w/thread_w) - 1)
            row -= 1

        for x in range(thread_w):
            for y in range(thread_h):

                x_plot = int(column*thread_w) +x
                y_plot = int(row*thread_h) +y

                re = scale*(x_plot-w2) + offset.real
                im = scale*(y_plot-h2) + offset.imag
                c = complex( re, im )
                color = mandelbrot(c, 63)
                
                r = (color << 6) & 0xc0
                g = (color << 4) & 0xc0
                b = (color << 2) & 0xc0

                with lock:
                    surface.set_at( (x_plot, y_plot), (255-r,255-g,255-b) )
                       

        try:
            barrier.wait()
        except threading.BrokenBarrierError:
            pass
    # with lock :
    #     # print("column :" ,column,"row",row,x,y)
    #     print('{} finished.'.format( threading.currentThread().getName() ) )


N = int( (scr_w * scr_h) / (thread_w*thread_h) )

lock = threading.Lock()
barrier = threading.Barrier(N+1)
list_sems = [threading.Semaphore(0) for i in range(N)]
list_threads =  []

for i in range(N):
    id = (i+1)
    sem = list_sems[i]
    thread = threading.Thread(target=thread_func,args=(id,surface,lock,barrier,sem))
    thread.setName( 'Thread-{:03d}'.format(id))
    list_threads.append(thread)
    
print("Threading : " + str(len(list_threads)) + " thread")

for t in list_threads:
    t.start()

###########################################################################################

########################################### Pygame ########################################

while running:

    clock.tick(10) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  

    if first_create:
        first_create = False
        scale = 0.006
        offset = complex(-0.55,0.0)

        for sem in list_sems:
            sem.release()
        try:
            barrier.wait()
        except threading.BrokenBarrierError:
            pass

        with lock:
            screen.blit( surface, (0,0) )


    pygame.display.flip()



barrier.reset()
pygame.quit()
print( 'PyGame done...')