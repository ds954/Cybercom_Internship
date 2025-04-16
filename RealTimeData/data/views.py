from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Comment
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse

# Create your views here.
def CommentView(request):
    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            new_comment = Comment.objects.create(comment_text=text)

            # Send to WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "comment",
                {
                    "type": "send_notification",
                    "message": new_comment.comment_text,
                }
            )
            return redirect('comment')  # Avoid form resubmission on refresh

    data = Comment.objects.all().order_by('-id')
    return render(request, 'comments.html', {'data': data})
    


def comment_page(request):
    comments = Comment.objects.all().order_by('-id')
    return render(request, 'comment_ajax.html', {'comments': comments})

def post_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment = Comment.objects.create(comment_text=comment_text)
            return JsonResponse({'comment': comment.comment_text})
    return JsonResponse({'error': 'Invalid request'}, status=400)