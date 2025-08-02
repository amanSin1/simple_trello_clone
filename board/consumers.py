# board/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Card, List, Board

class BoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the board_id from the URL
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        self.board_group_name = f'board_{self.board_id}'

        # For now, we'll allow any authenticated user to connect.
        # A real app would have more complex permission checks here.
        if self.scope["user"].is_anonymous:
            await self.close()
            return
        
        # --- PERMISSION CHECK: Is the authenticated user a member of this board? ---
        # We need to hit the database, so we use a helper async method.
        is_member = await self.is_board_member(self.scope["user"], self.board_id)
        if not is_member:
            print(f"Connection rejected: User {self.scope['user'].email} is not a member of board {self.board_id}")
            await self.close()
            return
        # --- END PERMISSION CHECK ---

        # Join the board-specific group
        await self.channel_layer.group_add(
            self.board_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"User {self.scope['user'].email} connected to board {self.board_id}")

    async def disconnect(self, close_code):
        # Leave the board-specific group
        await self.channel_layer.group_discard(
            self.board_group_name,
            self.channel_name
        )
        print(f"User {self.scope['user'].username} disconnected from board {self.board_id}")

    # This method is called when we receive a message from a WebSocket client (the browser)
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'card_move':
            card_id = data.get('card_id')
            new_list_id = data.get('new_list_id')
            new_position = data.get('new_position')

            # --- Backend Logic ---
            # 1. Update the database with the new card position
            await self.update_card_position(card_id, new_list_id, new_position)

            # 2. Broadcast the move to all other clients in the same board group
            await self.channel_layer.group_send(
                self.board_group_name,
                {
                    'type': 'broadcast_card_move', # This will call the method below
                    'card_id': card_id,
                    'new_list_id': new_list_id,
                    'new_position': new_position,
                    'sender_channel': self.channel_name # To identify who made the move
                }
            )

    # This method is called by the channel layer to send the broadcast to clients
    async def broadcast_card_move(self, event):
        # Don't send the message back to the original sender
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps({
                'type': 'card_moved',
                'card_id': event['card_id'],
                'new_list_id': event['new_list_id'],
                'new_position': event['new_position'],
            }))

    # --- Database Helper Method ---
    @sync_to_async
    def update_card_position(self, card_id, new_list_id, new_position):
        try:
            card_to_move = Card.objects.get(id=card_id)
            new_list = List.objects.get(id=new_list_id)

            # --- This is a simplified reordering logic ---
            # A more robust solution would handle shifting other cards' positions
            card_to_move.list = new_list
            card_to_move.position = new_position
            card_to_move.save()
            print(f"Updated card {card_id} to list {new_list_id} at position {new_position}")
        except (Card.DoesNotExist, List.DoesNotExist) as e:
            print(f"Error updating card position: {e}")

    @sync_to_async
    def is_board_member(self, user, board_id):
        try:
            board = Board.objects.get(id=board_id)
            # Check if the user is in the list of members for this board
            return user in board.members.all()
        except Board.DoesNotExist:
            return False