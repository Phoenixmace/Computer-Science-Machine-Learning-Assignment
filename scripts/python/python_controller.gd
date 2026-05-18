extends Node2D

@export var server_url: String = "ws://127.0.0.1:8765"

var peer := WebSocketPeer.new()
var initiated_session := false
var action := {}
func _ready() -> void:
	peer.connect_to_url(server_url)

func _process(delta):
	peer.poll()  # must call this every frame

	
func send_request(function_name: String, args:Dictionary):
	if peer.get_ready_state() == WebSocketPeer.STATE_OPEN:
		var request = {"function": function_name, "args":args}
		var json_string = JSON.stringify(request)
		peer.put_packet(json_string.to_utf8_buffer())
		return recieve_packets()
	else:
		return false
	

func recieve_packets():
	var state = peer.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		# connection is ready to send/receive packets
		while peer.get_available_packet_count() > 0:
			var packet = peer.get_packet().get_string_from_utf8()
			return packet
	elif state == WebSocketPeer.STATE_CONNECTING:
		# still connecting
		pass
	elif state == WebSocketPeer.STATE_CLOSING:
		# wait for close to complete
		pass
	elif state == WebSocketPeer.STATE_CLOSED:
		print("WebSocket closed")

func close_game():
	var closing_return_message = send_request("close_session",{})
	print(closing_return_message)
	peer.close(1000, "Normal closure")
