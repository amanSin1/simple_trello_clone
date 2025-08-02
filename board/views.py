# board/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Board

@login_required
def board_view(request, board_id):
    # Fetch the board first
    board = get_object_or_404(Board, id=board_id)
    
    # --- PERMISSION CHECK: Is the logged-in user a member of this board? ---
    # We use .all() on the ManyToManyField to get the list of members.
    if request.user not in board.members.all():
        # For now, we'll just show an error. A real app might redirect.
        # You could create a simple "access_denied.html" template.
        return render(request, 'board/access_denied.html', status=403)

    context = {
        'board': board,
    }
    return render(request, 'board/board_view.html', context)