extends Path2D

# state keeper
var state = "disabled"

# holds the location of our game elements that will be effected by the item
var level
var enemy
var hero
var fire
var stealth

var itemframe
var item
var timer
var timeremaining

var defdir = 1
var flipdir = -1
var posdef = 28
var posflip = -28
var throwpos
var staticpos

# hold location of point2d
var fallpos

var particle
var particletimer
var particlestate = "disabled"
var particlepos 
var particledefaultpos

#hold the sprite object and the sprites location
var sprite
var lastlocation

func _ready():
	
	# store the level node (so we can tell it things, like to make a new bush)
	level = get_parent().get_parent().get_parent()
	
	# get hero object and enemy
	hero = get_parent()
	enemy = get_parent().get_parent().get_node("Barbarian")
	sprite = $PathFollow2D/Sprite
	# record where the default position of our throw arc is.
	staticpos = get_position()
	
	fallpos = $Position2D
	
	# get the itemframe object
	itemframe = get_parent().get_parent().get_parent().get_node("itemframe")
	
	# record the default value of our timer.
	timer = $Timer.get_wait_time()
	
	
	# get the particle effect for splash (flask)
	particle = get_parent().get_parent().get_node("Barbarian/splash")
	particletimer = particle.get_node("Timer")
	particledefaultpos = particle.get_position()
	
	#get the stealth bar
	stealth = get_parent().get_parent().get_parent().get_node("stealth")

func _process(delta):
	# item is spawned at correct pos
	# when inactive state is disabled
	particledraw()
	
	lastlocation = fallpos.get_global_position()
	
	# if the item is not thrown yet.
	if state == "disabled":
		reset()

		particlepos = sprite.get_global_position()
	# when activated it determines what item it is, sets appropriate sprite, 
	# checks what direction we are facing and adjusts things
	if state == "assign":
		
		item = itemframe.use_item()
		
		if typeof(item) == TYPE_ARRAY:
			sprite.set_texture(item[4])
			throwpos = get_global_position()
			state = "ready"
			$Timer.start()
			checkfacing()
		else:
			state = "disabled"
		
	# once activated item follows path based on ratio of timeleft to time total.
	# if impacts barb effect triggered.
	if state == "ready":
		set_global_position(throwpos)
		visible = true
		var left = $Timer.get_time_left()
		var change = 1.0 - (left / timer)

		$PathFollow2D.set_unit_offset(change)
		
		visible = true
		
		if check_for_hit():
			particlepos = sprite.get_global_position()
			state = "hit"
		
		# once arc completed, set state keeper to "impact"
		if change == 1:
			state = "fell"
			visible = false
	
	# once hit check for impact.
	# if item has effects based on location of drop (pip/purse)
	# this is where they will go
	if state == "fell":
		
		if item[2] == 0: 
			effect()
		state = "disabled"
		
	if state == "hit":
		effect()
#	# Called every frame. Delta is time since last frame.
#	# Update game logic here.
#	pass

func check_for_hit(target = enemy):
	
	var itemcollider = $PathFollow2D/Sprite/Area2D
	var hit = false
	
	var object = target.find_node("standinghit")
	var thisobject = object.get_instance_id()

	var LapList = $PathFollow2D/Sprite/Area2D.get_overlapping_areas()
	var listlength = LapList.size()

	
	for i in range(listlength):
		if LapList[i].get_instance_id() == thisobject:
			hit = true

	return hit

func reset():
		# update spawn position to default (attached to nablin)
	set_position(staticpos)
	
	# flip the spawn point and arc horizontally based on movement
	checkfacing()
	
	# keep the item hidden
	visible = false

func checkfacing():
	
	var facing = hero.get_facing()
	
	if facing == "right":
		set_scale(Vector2(defdir,1))
		set_position(Vector2(posdef,-7))
	if facing == "left":
		set_scale(Vector2(flipdir,1))
		set_position(Vector2(posflip,-7))

func grow_bush():
	pass

func particledraw():
	var timeleft = particletimer.get_time_left()
	
	if particlestate == "disabled":
		particletimer.stop()
		particle.set_emitting(false)
	
	if particlestate == "initialize":
		#particle.set_global_position(particlepos)
		particlestate = "fire"
		print("starting timer")
		particletimer.start()

		
	if particlestate == "fire":
		#particle.set_global_position(particlepos)
		particle.set_emitting(true)
		particle.set_visible(true)
		
		print(timeleft)
		
		if timeleft > 0:
			print("drawing")
			print(timeleft)
			
		if timeleft == 0:
			particlestate = "disabled"
			#particle.set_position(particledefaultpos)
	
	
func effect():
	
	# if pip
	if item[2] == 0: 
		level.add_bush(lastlocation)
	
	# if flask
	if item[2] == 2:
		particlestate = "initialize"
		particledraw()
		enemy.magicstun()
		stealth.clear()
	
	# if purse
	if item[2] == 1:
		particlestate = "initialize"
		particledraw()
		enemy.hitstun()
		stealth.clear()

	state = "disabled"
	
func use():
	if state == "disabled":
		state = "assign"