extends KinematicBody2D

var motion = Vector2()
var MoveSpeed = 200

# Create a list to store the motion information.
var actionlist = []
var stealth = 0
signal moving

var last_loot

var item
var itemframe
var itemsprites

var ismoving = false
var enemy
var hero
var direction
var footfall = 0
# state keeper.
var state 

# ticks for knockback. This should just be a timer object prolly
var knockcounter = 0
var health

# facing variables to monitor and control facing
var facing = "right"
var wasfacing = "right"

var default_box_pos 
var current_box_pos = Vector2()

var timer

# Specific variables for some actions outside of the state keeper
var knocking = false
var dead = false


var fire
signal gameover
var luck



func _ready():
	luck = get_parent().get_parent().luck
	var new_bush
	state = "idle"
	hero = self
	item = get_parent().get_parent().get_node("YSort/Player/item")
	itemframe = get_parent().get_parent().get_node("itemframe")
	itemsprites = itemframe.get_itemsprites()
	enemy = get_parent().get_parent().get_node("YSort/Barbarian")
	health = get_parent().get_parent().get_node("health")
	timer = get_parent().get_parent().get_node("gentimer")
	fire = get_parent().get_parent().get_node("YSort/Fire")
	
	default_box_pos = $lootcol.get_position()


func _physics_process(delta):
	keycheck()
	if state == "knockback":
		knocking_back()
	else:
		# check if dead, if not then check if looting, if not move around.
		if dead == false:
			if state == "loot":
				loot()
			else:
				moveplayer()
		else:
			dead()
	
		updatehitboxes()

func dead():
	$AnimatedSprite.set_animation("Death")
	$AnimatedSprite.playing = true
	emit_signal("gameover")

func knocking_back():
	$AnimatedSprite.set_animation("Knockback")
	if knockcounter < 10:
		if direction.x < 0.0:
			$AnimatedSprite.flip_h = true
			motion.x = 600
		else:
			$AnimatedSprite.flip_h = false
			motion.x = -600
		knockcounter += 1
	else:
		if dead == true:
			$AnimatedSprite.set_animation("Dead")
		motion.x = 0
		motion.y = 0
		knockcounter = 0
		state = "idle"
	
	move_and_slide(motion)

func isdead():
	return dead

func foot_fall():
	if footfall == 0:
		$leftfoot.play()
	if footfall == 1:
		$rightfoot.play()
	footfall += 1
	if footfall > 1:
		footfall = 0
	
func keycheck():
	#_checkstealth()
	actionlist = []

	
	if Input.is_action_pressed("ui_right"):
		actionlist.append("right")
	if Input.is_action_pressed("ui_left"):
		actionlist.append("left")
	if Input.is_action_pressed("ui_up"):
		actionlist.append("up")
	if Input.is_action_pressed("ui_down"):
		actionlist.append("down")
	if Input.is_action_pressed("ui_down"):
		actionlist.append("down")
	if Input.is_action_just_pressed("loot"):
		actionlist.append("loot")
	if Input.is_action_just_pressed("use_item"):
		actionlist.append("item")
	if Input.is_action_just_released("item_left"):
		itemframe.item_left()
	if Input.is_action_just_released("item_right"):
		itemframe.item_right()

	
func moveplayer():
	#print(actionlist)
	if not actionlist.has("loot"):
		
		$AnimatedSprite.set_animation("default")
		if actionlist.has("item"):
			item()
			
		if actionlist.has("left"):
			facing = "left"
			motion.x = -MoveSpeed
			ismoving = true
			$AnimatedSprite.flip_h = true
			$AnimatedSprite.playing = true
			
		elif actionlist.has("right"):
			facing = "right"
			ismoving = true
			motion.x = MoveSpeed
			$AnimatedSprite.flip_h = false
			$AnimatedSprite.playing = true
		
		if not actionlist.has("up") and not actionlist.has("down"):
			motion.y = 0
		
		if actionlist.has("up"):
			ismoving = true
			motion.y = -MoveSpeed
			$AnimatedSprite.playing = true
			
		elif actionlist.has("down"):
			ismoving = true
			$AnimatedSprite.playing = true
			motion.y = MoveSpeed
		
		if actionlist.size() == 0:
			ismoving = false
			motion.x = 0
			motion.y = 0
			$AnimatedSprite.playing = false
			$AnimatedSprite.frame = 1
		
		if ismoving:
			emit_signal("moving")
			
		move_and_slide(motion)
	else:
		state = "loot"
		
func distance_to_target(target):
	var data = (target.get_global_position() - self.get_global_position()).normalized()
	return data 

func updatehitboxes():
	if facing == "right" and wasfacing == "left":
		wasfacing = "right"

		current_box_pos.y = default_box_pos.y
		current_box_pos.x = -default_box_pos.x

		$lootcol.set_position(current_box_pos)
	elif facing == "left" and wasfacing == "right":

		wasfacing = "left"
		$lootcol.set_position(default_box_pos)

func roll():
	var this_roll = randi() % 10 + 0
	print(luck)
	if this_roll <= luck:
		return true
	else:
		return false

func item():
	item.use()
	
func loot():
	var this_loot = get_global_transform().origin
	
	print(luck)
	emit_signal("moving")
	$AnimatedSprite.set_animation("Loot")
	$AnimatedSprite.playing = true
	
	var LapList = $stand.get_overlapping_areas()
	var hero
	var object
	var thisobject
	var listlength
	this_loot = get_global_position() 
	var hit = false

	if $AnimatedSprite.get_frame() == 1:

		object = enemy.find_node("sleepcol")
		thisobject = object.get_instance_id()

		LapList = $lootcol.get_overlapping_areas()

		listlength = LapList.size()
		for i in range(listlength):
			# and this_loot != last_loot 
			if LapList[i].get_instance_id() == thisobject and roll() == true:
				
				#register a succesful loot internally for the item bubble
				hit = true
				
				# remember where we found it, so you cant stand still and spam loot.
				last_loot = this_loot
				
				$get._set_playing(true) 
				#tell the item controller that a new item was looted.
				itemframe.newitem()
				var itemgot = itemframe.get_item()
				if typeof(itemgot) == TYPE_ARRAY:
					$itembubble.get_item(itemgot[3])

				
		$AnimatedSprite.set_frame(0)
		$AnimatedSprite.set_animation("default")
		state = "idle"



func _on_Barbarian_hit():
	health.hit()
	state = "knockback"

	direction = distance_to_target(enemy)

func _on_health_death():
	dead = true

func get_facing():
	return facing
	
func get_state():
	return state

func _on_Fire_firehit():
	if state != "knockback":
		health.hit()
		state = "knockback"
		direction = distance_to_target(fire)


func _on_timer_timesup():
	dead = true
