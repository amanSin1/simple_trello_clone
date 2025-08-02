# board/models.py
from django.db import models
from django.conf import settings

class Board(models.Model):
    """A project board that contains lists and cards."""
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_boards')
    
    # --- NEW: Add a ManyToManyField for members ---
    # This allows a board to have many members, and a user to be a member of many boards.
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='boards')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class List(models.Model):
    """A list (column) on a board, e.g., 'To Do', 'In Progress'."""
    title = models.CharField(max_length=200)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Default order of lists

    def __str__(self):
        return f"{self.title} on {self.board.title}"

class Card(models.Model):
    """A card (task) within a list."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    position = models.PositiveIntegerField(default=0) # For ordering within a list
    created_at = models.DateTimeField(auto_now_add=True)
    # We can add assigned_users, due_date, etc. later.

    class Meta:
        ordering = ['position'] # Default order of cards

    def __str__(self):
        return self.title