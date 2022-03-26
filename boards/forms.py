from django import forms

from .models import Topic, Post, Banner


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is on your mind ?'}),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message', 'tag']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class BannerForm(forms.Form):
    image_url = forms.ImageField(label='MainPhoto', required=False, widget=forms.FileInput(attrs={'class': 'btn'}))

    class Meta:
        model = Banner
    #     fields = ['image_url',]
