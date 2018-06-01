extends Control

onready var timer = $fade_in
var timeleft = 0
var state = 0
var titletext = ""
var objectives = []
var nights = ["First Night", "Second Night", "Last Night"]
# class member variables go here, for example:
# var a = 2
# var b = "textvar"

func _ready():
	timer.start()
	
	# Called every time the node is added to the scene.
	# Initialization here
	pass
	
func get_time_perc():
	var total = timer.get_wait_time()
	var remaining = timer.get_time_left()
	
	return 1 - (remaining / total)
	
func init(gameinfo):
	
	$top/night_label.set_text(nights[gameinfo["nightnumber"]])
	
	
	pass
	
func _process(delta):
	print(get_time_perc())
	if get_time_perc() < 1:
		$top/night_label.set_modulate(Color(1, 1, 1, get_time_perc()))
	if get_time_perc() == 1:
		if state == 0:
			print("got here")
			$title.start()
			state = 1
	
	timeleft = timer.get_time_left()
	
#	# Called every frame. Delta is time since last frame.
#	# Update game logic here.
#	pass


func _on_title_timeout():
	$objectives/title.set_visible(true)

	$obj1.start()
	pass # replace with function body

func _on_obj1_timeout():
	$objectives/VBoxContainer/obj1.set_visible(true)
	$obj2.start()
	pass # replace with function body

func _on_obj2_timeout():
	$objectives/VBoxContainer/obj2.set_visible(true)
	$obj3.start()
	pass # replace with function body

func _on_obj3_timeout():
	$objectives/VBoxContainer/obj3.set_visible(true)
	pass # replace with function body
