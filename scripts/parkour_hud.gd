extends CanvasLayer
var title: Label
var stats: Label
var status: Label
var message: Label
var finish_panel: PanelContainer
var finish_text: Label
var progress: ProgressBar
@onready var level = get_parent()

func label_at(parent: Node, text: String, size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	parent.add_child(label)
	return label

func panel(at: Vector2, dimensions: Vector2) -> PanelContainer:
	var p := PanelContainer.new()
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.035, 0.06, 0.10, 0.88)
	style.corner_radius_top_left = 12
	style.corner_radius_top_right = 12
	style.corner_radius_bottom_left = 12
	style.corner_radius_bottom_right = 12
	style.content_margin_left = 20
	style.content_margin_right = 20
	style.content_margin_top = 12
	style.content_margin_bottom = 12
	p.add_theme_stylebox_override("panel", style)
	p.position = at
	p.custom_minimum_size = dimensions
	p.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(p)
	return p

func _ready() -> void:
	var left := VBoxContainer.new()
	panel(Vector2(26, 24), Vector2(285, 97)).add_child(left)
	title = label_at(left, "S K Y L I N E", 26, Color("f5e9d6"))
	label_at(left, "R O O F T O P   R U N   /   0 1", 12, Color("65dacf"))
	var right := VBoxContainer.new()
	panel(Vector2(920, 24), Vector2(334, 110)).add_child(right)
	stats = label_at(right, "", 21, Color("f5e9d6"))
	status = label_at(right, "", 13, Color("83c9cc"))
	progress = ProgressBar.new()
	progress.max_value = 15
	progress.show_percentage = false
	progress.custom_minimum_size = Vector2(0, 5)
	right.add_child(progress)
	var help := VBoxContainer.new()
	panel(Vector2(26, 620), Vector2(685, 76)).add_child(help)
	label_at(help, "WASD  mover    /    ESPACIO  saltar    /    RATÓN  cámara    /    R  volver", 15, Color("e0e5df"))
	label_at(help, "ESC libera el cursor  ·  Clic para capturarlo  ·  F cambia el límite de FPS", 12, Color("83c9cc"))
	message = label_at(self, "", 19, Color("ffe0ac"))
	message.position = Vector2(320, 586)
	message.size.x = 640
	message.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	message.add_theme_color_override("font_shadow_color", Color(0,0,0,0.8))
	message.add_theme_constant_override("shadow_offset_y", 2)
	finish_panel = panel(Vector2(390, 235), Vector2(500, 230))
	var finish_box := VBoxContainer.new()
	finish_panel.add_child(finish_box)
	label_at(finish_box, "ENTREGA COMPLETADA", 28, Color("65dacf"))
	finish_text = label_at(finish_box, "", 20, Color("f5e9d6"))
	label_at(finish_box, "Pulsa R para intentarlo de nuevo", 16, Color("ffae75"))
	finish_panel.hide()

func _process(_delta: float) -> void:
	stats.text = "%02d:%05.2f   /   %02d de 15" % [int(level.elapsed / 60), fmod(level.elapsed, 60), level.crystals.size()]
	status.text = "AZOTEA %02d / 16     ·     %s" % [level.reached + 1, level.player.STATE_NAMES[level.player.state]]
	progress.value = level.reached
	message.text = level.notice if level.notice_time > 0.0 else ""
	finish_panel.visible = level.finished
	if level.finished:
		finish_text.text = "Tiempo  %.2f s\nCristales  %d / 15    ·    Caídas  %d\nMejor tiempo  %.2f s" % [level.elapsed, level.crystals.size(), level.falls, level.best]
