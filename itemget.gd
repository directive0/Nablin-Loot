extends Node

var timer
# class member variables go here, for example:
# var a = 2
# var b = "textvar"

func _ready():
	timer = get_parent().get_parent().get_parent().get_node("boxtimer")
	# Called every time the node is added to the scene.
	# Initialization here
	pass

func _process(delta):
#	# Called every frame. Delta is time since last frame.
#	# Update game logic here.
	pass

func get_item(sprite):
	$Sprite.set_texture(sprite)
	set_visible(true)
	timer.start()
	
	

func _on_boxtimer_timeout():
	set_visible(false)
	timer.stop()
	pass # replace with function body
