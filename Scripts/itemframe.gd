extends Sprite

var item
var items = []
var itemdata
var itemno
var itemsprite = []
var score
var noitems
# class member variables go here, for example:
# var a = 2
# var b = "textvar"

func _ready():
	# load our sprites for our objects in the frame.
	itemsprite.append(load("res://purse.png"))
	itemsprite.append(load("res://pip.png"))
	itemsprite.append(load("res://flask.png"))
	
	score = get_parent().get_node("score")
	
	#items 
	#0	name
	#1 - value
	#2 - effect
	#3 - sprite
	itemdata = [["Pip",100,0,itemsprite[1],load("res://pipsmall.png")],["Purse",500,1,itemsprite[0],load("res://pursesmall.png")], ["Flask",150,2,itemsprite[2],load("res://flasksmall.png")]]
	
	
	# Called every time the node is added to the scene.
	# Initialization here

func _process(delta):
	noitems = items.size()
	
	if noitems > 0:
		var topitem = items[-1]
		$item.set_texture(topitem[3])
		$item.set_visible(true)
	else:
		$item.set_visible(false)

func get_itemsprites():
	return itemsprite

func item_left():
	if noitems > 0:
		var register = items.pop_front()
		items.push_back(register)

func item_right():
	if noitems > 0:
		var register = items.pop_back()
		items.push_front(register)

func get_item():
	
	if noitems > 0:
		return items[-1]
	else:
		return "none"
	
func use_item():

	var item_to_use = items.pop_back()

	return item_to_use

func newitem():
	# pick a number
	itemno = randi() % 3 + 0
	
	#use the number to read data from the databank
	var thisitem = itemdata[itemno]
	
	
	# add the data for this item to the itembank
	items.append(thisitem)
	
	# add the score amount to the score counter
	score.newitem(thisitem[1])
	