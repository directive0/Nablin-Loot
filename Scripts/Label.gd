extends Label

# class member variables go here, for example:
# var a = 2
# var b = "textvar"
var hero

func _ready():
	hero = get_parent().get_node("YSort/Player")
	visible = false
	# Called every time the node is added to the scene.
	# Initialization here
	pass

func _process(delta):
	if hero.isdead():
		visible = true
#	# Called every frame. Delta is time since last frame.
#	# Update game logic here.
#	pass


func _on_timer_timesup():
	visible = true
	pass # replace with function body
