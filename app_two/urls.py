from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUp.as_view()),
    path("signin/", views.SignIn.as_view()),
    path("signOut/", views.SignOut.as_view()),

    path("profile/", views.Profile.as_view()),
    path("profile_update/", views.UpdateUser.as_view()),

    path("post_list/", views.PostListView.as_view()),
    path("post_detail/<int:pk>/", views.PostDetailView.as_view()),

    path("post_search/", views.SearchPosts.as_view()),
    # http://127.0.0.1: 8000/post_search/?search=fantasy
    # http://127.0.0.1:8000/post_search/?category=category_name - Qidiruv uslublari
    # http://127.0.0.1:8000/post_search/?ordering=create_at

    path("comments/", views.CommentListView.as_view()),
    path("comments/<int:pk>/", views.CommentDetailView.as_view()),

    path("like/<int:pk>/", views.LikeView.as_view()),
]



