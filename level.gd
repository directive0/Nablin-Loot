extends Node2D

var difficulty
var luck = 10
var new_bush

var testloc = Vector2(200,200)
var lock = 0
var gameover = false
var timesup = false

func _ready():
	new_bush = load("res://Bush.tscn")

func _process(delta):
	if gameover == true:
		keycheck()
	pass

func set_luck(luckset):
	luck = luckset

func get_state():
	if gameover == true:
		return true
	else:
		return false
	
func add_bush(location):
	var bush = new_bush.instance()
	bush.set_position(location)
	$YSort.add_child(bush)

func keycheck():
# resets on gameover if you press "space"
	if Input.is_action_pressed("loot"):
		if gameover == true:
			get_tree().change_scene("res://Root.tscn")

func _on_Player_gameover():
	gameover = true

func _on_timer_timesup():
	timesup = true

func get_details():
	var items = $itemframe.items
	var score = $score.score
	var everwoke = $YSort/Barbarian.everwoke
	var health = $YSort/Player.health
	var details = {"items":items, "score":score,"everwok": everwoke, "health" : health}

	return details