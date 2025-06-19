#MST Delivery Route Optimization
#Boramey Oe
#sources: https://docs.google.com/document/d/13QRBvGFaoTtZY0_1JwKxtoTodXJ4O8hNaDwxqRVCqDA/edit?tab=t.0
#Date: 18/06/2025

import pygame

#code for classes
#define a class that stores all the nodes in the graph
class graph_nodes:
    def __init__(self, pos, node_text_color = (0,0,0)): 
        self.pos = pos
        self.node_text_color = node_text_color 

        #the colour of the nodes depend on the map that the user has selected.
        if selected_map == 1:
            self.color = (46,203,233)
        elif selected_map == 2:
            self.color = (26,167,236)  
            self.color = (62,150,244)
        elif selected_map == 3:
            self.color = (42,157,244) 

#stores the information of the edges
class graph_edges:
    def __init__(self, pos1, pos2, weight):
        self.pos1 = pos1 #we want it to be a tuple of coordinates
        self.pos2 = pos2
        self.weight = weight

        if selected_map == 1:
            self.color = (90, 176, 199)
        elif selected_map == 2:
            self.color = (75,138,220)   
        elif selected_map == 3:
            self.color = (1,143,199)  




#defining functions
#check which map the user selected
def user_selected_map(pos):
    if 120 <= pos[0] <= 325 and 210 <= pos[1] <= 510: #this is the location of the first map option
        return 1
    elif 360 <= pos[0] <= 602 and 210 <= pos[1] <= 510: #location of the second map option
        return 2
    elif 635 <= pos[0] <= 870 and 210 <= pos[1] <= 510: #location of the third map option
        return 3
    else:
        return 0

#display the user's selected map as the background
def map_as_background(number): 
    global background
    if number == 1:
        background = pygame.image.load("assets/ontario map.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return background
    elif number == 2:
        background = pygame.image.load("assets/canada map.svg")
        #background = pygame.transform.scale(background, (800, 550))
        background = pygame.transform.scale(background, (800, 550))
        return background
    elif number == 3:
        background = pygame.image.load("assets/world map.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return background

#defining a function that draws rectangles around the products in the online shopping display. Even though it's already a built in function, I still needed to create the function to draw changing rectangles (whose position keeps changing).
def product_clicked(rect_location):
    pygame.draw.rect(screen, (245,245,245), rect_location, 0)
    return

#a function that makes sure the distance of the user's selected node is far enough (this also prevents the user from picking nodes at the same location)
def check_for_distance(pos): 
    for i in nodes.values():
        distance = round((i.pos[0] - pos[0])**2 + (i.pos[1] -  pos[1])**2)**(1/2)
        if distance < 50: 
            return False #we don't need to run the loop anymore since it has already violated the distance rule
    return True

#a function to make sure that the user doesn't create a node near the "DONE" and "RUN" buttons
def far_from_buttons(pos): #
    if pos[0] > 800 and pos[1] < 165: 
        return False 
    else:
        return True

#identify if the buttons are clicked on so we can change its colour
def button_change_colour(pos):
    global num_button1_pressed, num_button2_pressed
    if 862 <= pos[0] <= 968: 
        if 27 <= pos[1] <= 73: #checks if the "DONE" button is pressed
            num_button1_pressed += 1
            return 1
        elif 77 <= pos[1] <= 123: #checks for the "RUN" button
            num_button2_pressed += 1
            return 2
    else:
        return None

#retrieving and returning the colour of the edge
def edge_color(pos_node1, pos_node2):
    for key, value in edges.items(): 
        if value.pos1 == pos_node1 and value.pos2 == pos_node2:
            return value.color

    if selected_map == 1:
       return (90, 176, 199)
    elif selected_map == 2:
        return (75,138,220)    
    elif selected_map == 3:
        return (1,143,199)
    
#the color of the nodes light up once clicked when trying to form an edge
def change_node_color(pos):
    global node_text_color 
    for value in nodes.values(): 
        distance = round((pos[0] - value.pos[0])**2 + (pos[1] - value.pos[1])**2)**(1/2) #using the distance formula
        if distance <= 8 and forming_edges:
            value.node_text_color = (0,0,0)
            if selected_map == 1:
                value.color = (173,245,255)
            elif selected_map == 2:
                value.color = (255, 242, 175)
            elif selected_map == 3:
                value.color = (41,197,246)
            return value.color
        
        elif distance <= 8 and reset_node_color: #change the node back to its original colour
            value.node_text_color = (0,0,0)

            if selected_map == 1:
                value.color = (46,203,233)
            if selected_map == 2:
                value.color =  (26,167,236) 
                value.color = (62,150,244)
            if selected_map == 3:
                value.color = (42,157,244) 
            return value.color
        
#creating the edges of the graph. 
def clicked_on_nodes(pos):
    global edge_clicked, connected_edge, invalid_edge, reset_node_color, forming_edges  #asked GPT to debug and it said to make the variables and the list global
    for i in nodes.values():
        if i.pos[0] - 10 <= pos[0] <= i.pos[0] + 10: #check if the user is trying to click near a node
            if i.pos[1] - 10 <= pos[1] <= i.pos[1] + 10:
                edge_clicked += 1
                connected_edge.append(i.pos) #this keeps track of the nodes that are being clicked on so we can check if it forms a valid edge later
                if len(connected_edge) == 2:
                    if connected_edge[0] == connected_edge[1]: #if the two nodes are the same --> invalid
                        forming_edges = False
                        invalid_edge = True 
                        edge_clicked = 0 
                        #change it back to the original colour
                        reset_node_color = True 
                        change_node_color(connected_edge[0]) 
                        change_node_color(connected_edge[1])
                        connected_edge.clear()
                    elif (connected_edge[0], connected_edge[1]) in edges_list_pos or (connected_edge[1], connected_edge[0]) in edges_list_pos: #We check if the user is trying to form an edge that has already been formed. we check for both orderings of repeated edges.
                        invalid_edge = True
                        forming_edges = False
                        edge_clicked = 0
                        #change it back to the original colour
                        reset_node_color = True 
                        change_node_color(connected_edge[0])
                        change_node_color(connected_edge[1])
                        connected_edge.clear()
                    else:
                        return edge_clicked

#the merge sort algorithm
def merge_sort(a_list):
    #accounts for the base case
    if len(a_list) == 1 or len(a_list) == 0:
        return a_list
    else:
        split_index = len(a_list)//2
        left_side = a_list[:split_index]
        right_side = a_list[split_index:]

        #recursive code
        sorted_left = merge_sort(left_side)
        sorted_right = merge_sort(right_side)

        #this merges both of the left_side and right_side. If the two lists hasn't been sorted yet, this code won't apply to it.
        return merge(sorted_left, sorted_right)
def merge(list1, list2):
    merged_list = [] #this stores the final merged list

    #these are the indices that are used to compare the elements in both lists
    left_index = 0
    right_index = 0

    #there are still exisiting elements in both lists
    while left_index < len(list1) and right_index < len(list2):
        if list1[left_index][1] <= list2[right_index][1]:
            merged_list.append(list1[left_index])
            left_index += 1
        else:
            merged_list.append(list2[right_index])
            right_index += 1
    
    #list2 has ran out of elements
    while left_index < len(list1):
        merged_list.append(list1[left_index])
        left_index += 1
    
    #list1 has ran out of elements
    while right_index < len(list2):
        merged_list.append(list2[right_index])
        right_index += 1
    
    #after all the lists have been sorted, it will run this code below
    return merged_list

#Kruskal's algorithm that will get us the Minimum Spanning Tree
def kruskals_alg(edge_and_weight):
    checking_value = 0 

    while True:
        if len(tree_weight) == num_nodes - 1: #a spanning tree contains n-1 edges where n is the number of vertices
            return actual_tree_edge
        else:
            #split the tuple into two different nodes. Kruskal's alg starts with the lowest weight which has an index of 0
            first = edge_and_weight[0][0][0] #edge_and_weight[0][0] gives a the tuple of two nodes (node1, node2) but we want to split them so it's edge_and_weight[0][0][0]
            second = edge_and_weight[0][0][1]
            edge = edge_and_weight[0][0]

            for i in range(len(tree_edge)): #looping through the array to check which nodes have been visited and store the incremented number in our variable
                for j in range(len(tree_edge[i])):
                    if first == tree_edge[i][j]:
                        checking_value += 2 #we can increment any value as long as it is not the same as the value incremented in line 250
                        first_subgroup_index = i
                    elif second == tree_edge[i][j]:
                        checking_value += 5
                        second_subgroup_index = i

            #chcecking which nodes have been visited
            if checking_value == 2: #meaning only the first node is amongst the visited node
                tree_edge[first_subgroup_index].append(second)
                tree_weight.append(edge_and_weight[0][1]) #this appends the weight
                actual_tree_edge.append(edge)
            elif checking_value == 5: #meaning only the second node is amongst the visited node
                tree_edge[second_subgroup_index].append(first)
                tree_weight.append(edge_and_weight[0][1])
                actual_tree_edge.append(edge)
            elif checking_value == 7:
                if first_subgroup_index == second_subgroup_index: #if they're in the same subgroup, we continue
                    continue
                elif first_subgroup_index < second_subgroup_index: #comparing their indices from smallest to greatest to connect the subgroups
                    first_index = first_subgroup_index
                    second_index = second_subgroup_index
                else:
                    first_index = second_subgroup_index
                    second_index = first_subgroup_index
                    
                tree_weight.append(edge_and_weight[0][1])
                actual_tree_edge.append(edge)
                tree_edge[first_index] = tree_edge[first_index] + tree_edge[second_index] #merging/connecting the subgroups
                del tree_edge[second_index]
            elif checking_value == 0: #if none of the nodes have been visited
                tree_edge.append([first, second])
                tree_weight.append(edge_and_weight[0][1])
                actual_tree_edge.append(edge)
                        
            #we always delete the first index so we can continue checking for the next smallest weight
            del edge_and_weight[0]
            checking_value = 0 #resets checking value back to 0

#calculates the weight/distance of the MST
def MST_weight(tree_weight):
    total_weight = 0
    for i in tree_weight:
        total_weight += i
    
    return total_weight

#calculates the cost of the shipping process (did not add it to the price of the products bought yet)
def MST_cost(distance):
    cost = round(((distance/8)*0.65)*1.5) #the formula to find the cost
    return cost



pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#font to print texts onto the screen
main_font = pygame.font.SysFont(None, 30) 
weight_font = pygame.font.SysFont(None, 25) 



#everything needed to run the online shopping display
#setting up boolean values
shopping_display = True
buy_change_color = False #if the "BUY" button is pressed, we change its colour

#assigning variables
white_bg = (255,255,255)
user_scroll = 0 #how much the user scrolls
scrolling_speed = 12 
buy_pressed_time = 0
product_pressed_time = 0 #the time when the product image(s) was clicked

padding_x = 42 #from 55 to 0 CHANGE
padding_y = 50
product_width = 280
product_height = 280
clicked_on_rectangle = None #which product did the user select

total_price = 0
total_products = 0 #how many products have been purchased by the user
print_the_price = False
print_the_price_time = 0

loading_screen_time = pygame.time.get_ticks() 

#assigning variables to the product images
start_game = pygame.image.load("assets/start game.jpg")
start_game = pygame.transform.scale(start_game, (SCREEN_WIDTH, SCREEN_HEIGHT))
total_price_bg = pygame.image.load("assets/total price background.png")
total_price_bg = pygame.transform.scale(total_price_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

apple_watch = pygame.image.load("assets/apple watch.png")
backpack = pygame.image.load("assets/backpack.jpg")
chocolates = pygame.image.load("assets/chocolates.jpg")
gaming_chair = pygame.image.load("assets/gaming chair.jpg")
gaming_pc = pygame.image.load("assets/gaming pc.jpg")
cap = pygame.image.load("assets/hat.jpg")
chovy_jersey = pygame.image.load("assets/chovy jersey.jpg")
keyboard = pygame.image.load("assets/keyboard.jpg")
labubu = pygame.image.load("assets/labubu.png")
macbook = pygame.image.load("assets/macbook.png")
pencil_case = pygame.image.load("assets/pencil case.jpg")
water_bottle = pygame.image.load("assets/water bottle.png")

#put all the images into a list 
product_images = [apple_watch, macbook, keyboard, gaming_pc, gaming_chair, chovy_jersey, chocolates, cap, labubu, pencil_case, backpack, water_bottle]
for i in range(len(product_images)): 
    product_images[i] = pygame.transform.scale(product_images[i], (product_width,product_height)) #resize the images to fit in the online shopping display

#create two lists: one stores the name of the products and another stores the price
products = ['Apple Watch', 'Macbook Pro M4', 'Keyboard', 'Gaming PC', 'Secretlab Gaming Chair', 'GenG Chovy Jersey', 'Chocolates', 'Cap', 'Labubu', 'Pencil Case', 'Backpack', 'Water Bottle']
products_price = [float(549), float(2099), 249.99, 2386.67, 654.00, 98.00, 32.00, 91.98, 339.99, 16.69, 124.78, 32.18] #put float for the price that are integers 

products_rect = {} #the product name is the key. the value is a tuple with the zero index being the coordinates of the rectangles and the first index being its weight



#everything needed to run the "select a map" display
#the screen that prompts the user to select a map
def draw_maps():
    global map1, map2, map3

    map1 = pygame.image.load("assets/ontario map.png")
    map2 = pygame.image.load("assets/canada map.svg")
    map3 = pygame.image.load("assets/world map.png")
    
    #sizing of the maps
    map1 = pygame.transform.scale(map1, (250, 250)) 
    map2 = pygame.transform.scale(map2, (220, 220)) 
    map3 = pygame.transform.scale(map3, (250, 250))

    #display it onto the screen given the coordinate points
    screen.blit(map1, (95, 210)) 
    screen.blit(map2, (368, 216)) 
    screen.blit(map3, (620, 210))

    #the Ontario map. Code is copied from the "DONE" button code which was then copied from GPT
    rect_1 = pygame.Rect(85, 460, 250, 40) 
    text_1 = main_font.render("Ontario", True, (5, 5, 5))  
    text_rect_1 = text_1.get_rect(center=rect_1.center)
    screen.blit(text_1, text_rect_1)

    #the Canada map. The code is re-used from above
    rect_2 = pygame.Rect(350, 460, 250, 40) 
    text_2 = main_font.render("Canada", True, (5, 5, 5))  
    text_rect_2 = text_2.get_rect(center=rect_2.center)
    screen.blit(text_2, text_rect_2)

    #the World map  
    rect_3 = pygame.Rect(625, 460, 250, 40) 
    text_3 = main_font.render("World", True, (5, 5, 5))  
    text_rect_3 = text_3.get_rect(center=rect_3.center)
    screen.blit(text_3, text_rect_3)

    #printing the "select a map" text
    rect_4 = pygame.Rect(350, 20, 300, 200) 
    text_4 = pygame.font.SysFont(None, 70).render("Select a map", True, (5, 5, 5))  
    text_rect_4 = text_4.get_rect(center=rect_4.center)
    screen.blit(text_4, text_rect_4)

    #the outline of rectangle #1. 
    pygame.draw.line(screen, (0,0,0), (120,210), (325,210), 3) 
    pygame.draw.line(screen, (0,0,0), (120,210), (120,510), 3)
    pygame.draw.line(screen, (0,0,0), (120,445), (325,445), 3) 
    pygame.draw.line(screen, (0,0,0), (325,210), (325,510), 3)
    pygame.draw.line(screen, (0,0,0), (120,510), (325,510), 3)
    
    #the outline of rectangle #2
    pygame.draw.line(screen, (0,0,0), (360,210), (360,510), 3)
    pygame.draw.line(screen, (0,0,0), (360,210), (602,210), 3)
    pygame.draw.line(screen, (0,0,0), (602,210), (602,510), 3)
    pygame.draw.line(screen, (0,0,0), (360,445), (602,445), 3)
    pygame.draw.line(screen, (0,0,0), (360,510), (602,510), 3)

    #the outline of rectangle #3
    pygame.draw.line(screen, (0,0,0), (635,210), (870,210), 3)
    pygame.draw.line(screen, (0,0,0), (635,210), (635,510), 3)
    pygame.draw.line(screen, (0,0,0), (635,510), (870,510), 3)
    pygame.draw.line(screen, (0,0,0), (635,445), (870,445), 3)
    pygame.draw.line(screen, (0,0,0), (870,210), (870,510), 3)



#everything needed for the rest of the program (allows the user to place nodes, form edges, runs the MST, ...)
#assigning boolean values
allow_drawing = False 
done_pressed = False 
run_pressed = False 
invalid_edge = False #prints "Invalid Edge" on the screen if set to true
forming_edges = False #boolean that stores whether the user is trying to form an edge
reset_node_color = False #after lighting up the color of the nodes after being clicked, we want to reset it back. 
select_maps = False #controls the display of the screen that prompts the user to select a map
MST_display = False
MST_done = False #if this is true, we print the final price and the final distance
valid_amount = True #checks if the user place nodes that is less than or equal to the number of products purchased
shopping_display = True #displays the shopping_display
buy_change_color = False #change the colour of the buy button when clicked
print_the_price = False #this screen loads right after the shopping display

#defining the variables
num_nodes = 0 #count the total number of nodes in the graph
edge_clicked = 0 #this is always going to have a range between 0 to 2. It checks whether the user has formed an edge (by clicking on two nodes).
edge_weight = "" #this stores the user's inputted weight
#storing the time and the amount of times that the buttons are pressed 
button1_pressed_time = 0
button2_pressed_time = 0 
num_button1_pressed = 0 #could also use a flag but this also works fine
num_button2_pressed = 0

#creating dictionaries 
nodes = {} #key = num_nodes, value = instance of the graph_nodes class
edges = {} #key = node numbers of the two ndoes that are connected, value = isntance of the graph_edges class

#creating lists
connected_edge = [] #It notes down the locations of the two nodes that the user clicked and this information is later used to form an edge.
edges_list_pos = [] #stores the locations/positions of the two conencting nodes to draw an edge
draw_edge_list = [] #a list that contains tuples which stores (x position, y position, and the weight of the edge)
edge_and_weight = [] #a list that stores tuples of edges and weights
#final product of the MST is stored in these lists
tree_edge = [] #stores the subgroups of the edges
actual_tree_edge = [] #notes down the edges in the final MST    
tree_weight = [] #notes down the weight of the MST

#below is needed to create the animtion of the formation of the MST
update_edge_time = pygame.time.get_ticks() #I couldn't get it to work before but GPT said to put the assignment of these variables outside of the main pygame loop 
edge_index = 0



#we run the program now
run = True
while run:

    current_time = pygame.time.get_ticks() #copied from GPT. We want to know the time since the program starts to change the colour of buttons and such
    screen.fill(white_bg) #set it to a white background. 

    #showing the shopping display
    if shopping_display:
        if current_time - loading_screen_time < 1800: #blit an image of the loading screen before the user is allowed to shop
            screen.blit(start_game, (0,0))
            rect = pygame.Rect(380, 280, 250, 100) 
            text = pygame.font.SysFont("PressStart2P", 100).render("START", True, (255,222,33))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        else:
            screen.fill((255,255,255))
            for i in range(len(product_images)):
                row = i // 3 #because we only have 3 images in a row
                column = i % 3

                x_coord = column * (product_width + padding_x) + padding_x
                y_coord = (row * (product_height + padding_y)) - user_scroll + padding_y #minus user_scroll because we want to move the image down if we're scrolling down
                if -product_height < y_coord < SCREEN_HEIGHT: #GPT said to make it -product_height instead of 0 < y < 650 because it is more flexible and can stimulate the experience better
                    if current_time - product_pressed_time < 30:
                        product_clicked(clicked_on_rectangle)
                        screen.blit(product_images[i], (x_coord, y_coord))
                    else:
                        pygame.draw.rect(screen, (255,255,255), (x_coord, y_coord, product_width, product_height))
                    screen.blit(product_images[i], (x_coord, y_coord))

                    text = pygame.font.SysFont(None, 20).render(products[i], True, (0,0,0))
                    text_rect = text.get_rect(center=(x_coord + 140, y_coord + 280))
                    screen.blit(text, text_rect)

                    text_1 = pygame.font.SysFont(None, 18).render("$" + str(products_price[i]), True, (0,0,0))
                    text_rect_1 = text_1.get_rect(center=(x_coord + 140, y_coord + 300))
                    screen.blit(text_1, text_rect_1)

                    #create a rectangle to later check whether the user has clicked on it
                    rect = pygame.Rect(x_coord, y_coord, product_width, product_height) 
                    products_rect[products[i]] = (rect, products_price[i])
                
                if current_time - product_pressed_time < 15: #make it look as if the product has been pressed on by blitting a white background.
                    product_clicked(clicked_on_rectangle)
            
            #if the user scrolls to the bottom, the "BUY" button will show
            if user_scroll == 840: 

                rect = pygame.Rect(450, 560, 100, 40) 
                buy_button_color = (255,238,140)
                if current_time - buy_pressed_time < 30: 
                    buy_button_color = (245,245,245)
                pygame.draw.rect(screen, buy_button_color, rect, 0)
                text = pygame.font.SysFont(None, 36).render("BUY", True, (0, 0, 0))  
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    
    #the screen that prints the total price that the user has spent shopping
    elif print_the_price:
        if current_time - print_the_price_time < 1800:
            screen.blit(total_price_bg, (0,0))
            rect = pygame.Rect(375, 360, 250, 100) 
            text = pygame.font.SysFont(None, 200).render("$" + str(round(total_price)) + ".00", True, (255,255,255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        else: #after displaying that scree, we change the bool values
            shopping_display = False #the shopping_display should no longer appear
            print_the_price = False
            select_maps = True #should transition to the screen that allows the user to pick the map

    #display the different map options for the user to choose from 
    elif select_maps: 
        draw_maps()

    elif MST_display:
        background = map_as_background(selected_map)

        if selected_map == 1:
            screen.blit(background, (0, 0)) #the location of where the map should be displayed on
        elif selected_map == 2:
            screen.blit(background, (75, 60))
        elif selected_map == 3:
            screen.blit(background, (-20, 0)) 

        #if the done button hasn't been pressed yet, we allow the user to draw nodes onto the screen
        if not done_pressed:
            allow_drawing = True 
        
        #"DONE" button
        done_button_color = (232,183,255)
        if button1_pressed_time > 0 and current_time - button1_pressed_time < 100: 
            done_button_color = (99, 30, 95) #change its colour once pressed
        pygame.draw.rect(screen, done_button_color, (865, 30, 100, 40)) 
        #The "DONE" button code is copied from ChatGPT
        rect_1 = pygame.Rect(865, 30, 100, 40) #after "DONE" is pressed, the user can no longer add anymore nodes and they should start trying to form edges
        text_1 = pygame.font.SysFont(None, 36).render("DONE", True, (5, 5, 5))  
        text_rect_1 = text_1.get_rect(center=rect_1.center)
        screen.blit(text_1, text_rect_1)

        #"RUN" button
        run_button_color = (232,183,255)
        if button2_pressed_time > 0 and current_time - button2_pressed_time < 100: #change its colour once pressed
            run_button_color = (99, 30, 95)
        pygame.draw.rect(screen, run_button_color, (865, 80, 100, 40))
        #the "RUN" button which activates Kruskal's algorithm once pressed
        rect_2 = pygame.Rect(863, 80, 100, 40)
        text_2 = pygame.font.SysFont(None, 36).render("RUN", True, (5, 5, 5))  
        text_rect_2 = text_2.get_rect(center=rect_2.center)
        screen.blit(text_2, text_rect_2)  

        #the circle in the top left corner that tells the user how many more nodes they can draw
        pygame.draw.circle(screen, (0,0,0), [50,50], 20, 3)
        rect = pygame.Rect(48.5, 41, 40, 20)
        text = pygame.font.SysFont(None, 36).render(str(total_products), True, (0,0,0))
        text_rect = text_2.get_rect(center=rect.center)
        screen.blit(text, text_rect)

        #if the user forms an invalid edge, we print "Invalid Edge"
        if invalid_edge:
            inv_edge_rect = pygame.Rect(10, 640, 100, 40)
            inv_edge_text = main_font.render('Invalid Edge', True, (0,0,0))
            center_text = inv_edge_text.get_rect(center=inv_edge_rect.center)
            screen.blit(inv_edge_text, (25, 610))

        #if two valid nodes have been clicked, we display a prompt on the screen to allow the user to input the weight of the edge
        if edge_clicked == 2:
            main_font = pygame.font.SysFont(None, 36)
            prompt_rect = pygame.Rect(10, 640, 100, 40)
            enter_weight = main_font.render('Enter the weight: ', True, (0,0,0))
            text_input_rect = enter_weight.get_rect(center=prompt_rect.center)
            screen.blit(enter_weight, (20, 610))

            #prints the user's inputted weight next to the prompt
            input_rect = pygame.Rect(100, 640, 100, 40) 
            input_text = main_font.render(edge_weight, True, (0,0,0)) #asked GPT to debugg because it said text must be strings not bytes (I forgot to set edge_weight back to a string)
            input_text_rect = input_text.get_rect(center=input_rect.center)
            screen.blit(input_text, (230, 610))


    #checks for the user's movements/events
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False 
        elif event.type == pygame.MOUSEBUTTONDOWN: #check if the user clicked on something
            pos = pygame.mouse.get_pos() #gets the x,y coordinates of the user's click and stores it as a tuple
            
            if select_maps: #check which map the user selected
                selected_map = user_selected_map(pos)
                if selected_map != 0:
                    select_maps = False #we move on to the next screen and allow the user to place the nodes as along as the user selected a valid map
                    MST_display = True
            
            if shopping_display and not event.button == 4 and not event.button == 5: #sometimes, scrolling up and scrolling down would also activate the MOUSEBUTTONDOWN
                if user_scroll == 840:
                    rect = pygame.Rect(450, 560, 100, 40) #checks if the "BUY" button has been pressed
                    if rect.collidepoint(pos):
                        buy_pressed_time = current_time
                        shopping_display = False
                        print_the_price = True
                        print_the_price_time = current_time
                
                for key, value in products_rect.items(): #checks if the products are being pressed/bought
                    if value[0].collidepoint(pos):
                        clicked_on_rectangle = (value[0].x, value[0].y, value[0].width, value[0].height)
                        product_pressed_time = current_time
                        total_price += value[1]
                        total_products += 1

            #we first check if the buttons are being pressed
            if button_change_colour(pos) == 1 and num_button1_pressed == 1: #"DONE" button pressed
                allow_drawing = False 
                done_pressed = True
                button1_pressed_time = current_time
            elif button_change_colour(pos) == 2 and num_button2_pressed == 2: #"RUN" button pressed
                allow_drawing = False
                run_pressed = True 
                button2_pressed_time = current_time

            #we check that the nodes that the user wants to place meets all the criterias needed
            elif allow_drawing and check_for_distance(pos) and far_from_buttons(pos) and valid_amount: 
                new_node = graph_nodes(pos)
                nodes[num_nodes] = new_node #stores it into the nodes dictionary
                num_nodes += 1
                total_products -= 1
                if total_products <= 0:
                    valid_amount = False
                
            elif done_pressed and num_button1_pressed == 1:  
                forming_edges = True
                allow_drawing = False 
                change_node_color(pos) #we light up the nodes when clicked 

                #forms and stores the edge
                if clicked_on_nodes(pos) == 2: 
                    invalid_edge = False

                    edges_list_pos.append((connected_edge[0], connected_edge[1])) #stores the location of the edges (2 nodes) so we can draw the edge in the main loop

                    #this block finds the numbering of the nodes that the user chooses to form an edge. ex (2,3) means that there is an edge between nodes 2 and 3
                    for key, value in nodes.items(): #iterating through the dictionary 
                        if value.pos == connected_edge[0]:
                            node1 = key
                        elif value.pos == connected_edge[1]:
                            node2 = key

        #after the return button has been pressed after the user has typed the weight
        elif event.type == pygame.KEYDOWN and edge_clicked == 2: 
            if event.key == pygame.K_RETURN: #if the user presses on the return button, we store their input
                edge_weight = int(edge_weight)
                edge_and_weight.append(((node1, node2), edge_weight)) #the edge_and_weight list have elements like (((x1, y1), (x2, y2)), edge_weight)

                #create an instance of the graph_edges class
                new_edge = graph_edges(connected_edge[0], connected_edge[1], edge_weight)
                edges[(node1, node2)] = new_edge

                #reset the colour back to its original colour since it is not highlighted anymore
                reset_node_color = True
                forming_edges = False
                change_node_color(connected_edge[0])
                change_node_color(connected_edge[1])

                #append it to the draw_edge_list so the weight could be printed on the screen. we want the weight to be printed in the middle of the edge hence we divided the sum by 2.
                x_pos = (edges[(node1, node2)].pos1[0] + edges[(node1, node2)].pos2[0])//2 
                y_pos = (edges[(node1, node2)].pos1[1] + edges[(node1, node2)].pos2[1])//2
                draw_edge_list.append((x_pos, y_pos, edge_weight)) 
    
                #resets these two variable so it can be used again
                edge_clicked = 0
                connected_edge.clear()
                edge_weight =  "" #reset it to allow the user to add a new weight. It's also resetted as a string since the pygame's .render() function does not take ints.
            elif event.key == pygame.K_BACKSPACE:
                edge_weight = edge_weight[:-1]
            else:
                edge_weight += event.unicode #copied this line from GPT. It adds the user's typed input onto the string

        #if the user is scrolling through the schopping display
        elif shopping_display and event.type == pygame.MOUSEWHEEL: 
            user_scroll -= event.y * scrolling_speed
            user_scroll = max(0, min(user_scroll, 840)) #the minimum and maximum amount that we allow the user to scroll


    #the code in the main loop that draw things
    #draw the nodes of the graph
    for key, value in nodes.items(): 
        pygame.draw.circle(screen, (value.color), value.pos, 15) 
        circle_text = main_font.render(str(key), True, value.node_text_color) #give each node a number
        text_rect = circle_text.get_rect(center = value.pos)
        screen.blit(circle_text, text_rect) 
    
    #drawing the edges immediately after the user clicked on two nodes
    for edge in edges_list_pos:
        color_of_edge = edge_color(edge[0], edge[1]) #retrieve the colour of the edge
        pygame.draw.line(screen, color_of_edge, edge[0], edge[1], 4)
    
    #printing the weight of the edge onto the pygame window
    for weight_text in draw_edge_list:
        text = weight_font.render(str(weight_text[2]), True, (0,0,0))
        screen.blit(text, (weight_text[0], weight_text[1]))

    #calculate and colour the minimum spanning tree (final step of the program) when run is pressed
    if run_pressed: 
        the_merge_sort = merge_sort(edge_and_weight)
        kruskals_alg(the_merge_sort)    

        #change the colour of the nodes (MST)
        for node in nodes.keys():
            if selected_map == 1: #MST node colour
                nodes[node].node_text_color = (255,255,255)
                nodes[node].color = (32,82,92)
            elif selected_map == 2:
                nodes[node].color = (62,150,244)
                nodes[node].color = (70,102,255)
            elif selected_map == 3:
                nodes[node].color = (10,130,255) 
    
    #animate changing the edge colour if they are selected to form the minimum spanning tree. We stimulate this by colouring the edges of the MST one by one after the MST has been calculated.
    if edge_index < len(actual_tree_edge):
        if current_time - update_edge_time > 800:
            if selected_map == 1:
                edges[actual_tree_edge[edge_index]].color = (212,254,255)
            elif selected_map == 2:
                edges[actual_tree_edge[edge_index]].color = (250,245,241)
            elif selected_map == 3:
                edges[actual_tree_edge[edge_index]].color = (240,232,230)

            edge_index += 1
            update_edge_time = current_time
    elif edge_index >= len(actual_tree_edge) and len(actual_tree_edge) > 0:
        MST_done = True
    
    #the final step of the program is to print the total distances travelled and the total prices
    if MST_done: 
        total_weight = MST_weight(tree_weight)
        total_cost = round(total_price + MST_cost(total_weight))
        if selected_map == 1:
            rect = pygame.Rect(80, 475, 250, 40) 
            text = main_font.render("Total price = $" + str(total_cost) + ".00", True, (0,0,0))  
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

            rect = pygame.Rect(88, 515, 250, 40) 
            text = main_font.render("Total distance = " + str(total_weight) + "km", True, (0,0,0))  
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        elif selected_map == 2:
            rect = pygame.Rect(685, 200, 250, 40) 
            text = main_font.render("Total price = $" + str(total_cost) + ".00", True, (0,0,0))  
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

            rect = pygame.Rect(689, 240, 250, 40) 
            text = main_font.render("Total distance = " + str(total_weight) + "km", True, (0,0,0))  
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        elif selected_map == 3:
            rect = pygame.Rect(380, 520, 250, 40) 
            text = main_font.render("Total price = $" + str(total_cost) + ".00", True,  (0,0,0))  
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

            rect = pygame.Rect(380, 560, 250, 40) 
            text = main_font.render("Total distance = " + str(total_weight) + "km", True,  (0,0,0))  
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)        
        
    pygame.display.update()
    #determines the frame rate
    clock = pygame.time.Clock()
    clock.tick(60) #this controls the frames per second (how often it updates the program)

pygame.quit()