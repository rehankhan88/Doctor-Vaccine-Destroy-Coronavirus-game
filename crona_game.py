from ursina import *

# Initialize the Ursina app
app = Ursina()

# Game state variables
shoot = False
v = 0
score = 0
hit = False
over = False

# Update function is called every frame
def update():
    global doctor, shoot, vaccine_list, virus_list, score, over, hit, v
    if not over:
        # Move the doctor (player) left and right with arrow keys
        if held_keys['right arrow']:
            doctor.x += 0.007
        if held_keys['left arrow']:
            doctor.x -= 0.007
        
        # Handle shooting mechanics
        if shoot:
            vaccine_list[v].y += 0.015  # Move vaccine upward
            if vaccine_list[v].y > 0.2 or hit:  # If vaccine goes off screen or hits a virus
                destroy(vaccine_list[v])
                shoot = False 
                hit = False
            
            # Check for collision between vaccine and virus
            hit_info = vaccine_list[v].intersects()
            if hit_info.hit:
                hit = True
                score += 1
                if hit_info.entity in virus_list:
                    j = virus_list.index(hit_info.entity)
                    destroy(virus_list[j])
                    virus_list[j] = duplicate(virus, x=random.randint(-45, 45) / 100, y=random.randint(-3, -1) / 100)
        
        # Move viruses downward
        for i in virus_list:
            i.y -= 0.001
            if i.y < -0.8:
                over = True 
        
        # Display the score on the screen
        print_on_screen("REHAN KHAN SCORE: " + str(score), position=(-0.8, 0.5))
    else:
        # Game over: destroy all entities and display final score
        for i in vaccine_list:
            destroy(i)
        for i in virus_list: 
            destroy(i)
        destroy(doctor)
        print_on_screen("GAME OVER!", position=(-0.05, 0.2))
        print_on_screen("FINAL SCORE: " + str(score), position=(-0.07, 0.15))

# Handle input for shooting
def input(key):
    global shoot, vaccine_list, v
    st = -0.8
    if key == "space":
        shoot = True  
        v += 1
        vaccine_list.append(duplicate(vaccine, x=doctor.x, y=st))      

# Background entity
Entity(model="quad", scale=50, texture="back.png")

# Set the size for the background
back_size = 22

# Invisible entity to set up the game area
back = Entity(model='quad', color=color.rgba(255, 255, 255, 0), scale=(12, 18), position=(back_size // 2, back_size // 2, -0.01))

# Doctor (player) entity
doctor = Entity(model='cube', parent=back, scale=0.2, texture='rrrr.jpg', position=(0, -0.7, 0))

# Vaccine entity (projectile)
vaccine = Entity(model='quad', parent=back, scale=0.1, texture='vaccin.png', position=(2, 2), collider="box")
vaccine_list = [duplicate(vaccine, y=2, x=2)]

# Virus entity (enemy)
virus = Entity(model='quad', parent=back, scale=0.15, texture='virus.png', position=(2, 2), collider="box")
virus_list = []

# Initialize virus entities at random positions
for i in range(5):
    virus_list.append(duplicate(virus, x=random.randint(-45, 45) / 100, y=random.randint(-3, -1) / 100))

# Set camera position and rotation
camera.position = (back_size // 2, -15, -11)
camera.rotation_x = -60

# Run the Ursina app
app.run()
