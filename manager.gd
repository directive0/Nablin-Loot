extends Node

onready var titleframe = load("res://intertitle.tscn")
onready var level = load("res://level.tscn")
var current_frame
var state = "opening"
var gameinfo = {"nightnum" : 1, "obj1": "In 1 minute", "obj2" : "Get 5000 Points", "obj3" : "Take No Damage"}

var itemdata = [{"title": "Pip", "value" : 100, "ID" : 0, "sprite index" : 1, "small sprite": load("res://pipsmall.png")},
{"title": "Purse", "value" : 500, "ID" : 1, "sprite index" : 0, "small sprite": load("res://pursesmall.png")},
{"title": "Flask", "value" : 150, "ID" : 2, "sprite index" : 2, "small sprite": load("res://flasksmall.png")}]


# trying to define each objective programetrically,
# title decides what's printed
# type indicates condition type (item present in list of items, undamaged, no wakes, score)
var obj_item = {"title": "Loot a", "type": "item present", "item": "Flask"}
var obj_score = {"title" : "Get a score of ", "type" : "score", "amount" : "5000"}


func _ready():
	# load an intertitle
	add_title()
	# Called every time the node is added to the scene.
	# Initialization here
	
func _process(delta):
	if state == "opening":
		if Input.is_action_pressed("loot"):
			remove_title()
			add_level()
			$level.set_luck(4)
			state = "first night"
	if state == "first night":
		if $level.get_state() == true:
			get_tree().paused = true
			$fade.start()
			state = "first night over"
			var detail = get_node("level").get_details()
	
	if state == "first night over":
		
		pass
		
func add_title():
	current_frame = titleframe.instance()
	add_child(current_frame)
	
func add_level():
	current_frame = level.instance()
	add_child(current_frame)

func remove_level():
	remove_child($level)
	
func remove_title():
	var target = get_node("intertitle")
	remove_child(target)

func game_has_ended():
	var gameover = get_node("level").gameover
	
func item_got(type, items):
	if items.has(type):
		return true
	else:
		return false

func decide_objectives():
	pass


func get_time_perc(timer):
	var total = timer.get_wait_time()
	var remaining = timer.get_time_left()
	
	return 1 - (remaining / total)