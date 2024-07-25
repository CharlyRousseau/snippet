from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from snippet.admin import CustomUserCreationForm
from .models import CustomUser, languages, LikedSnippets, Snippet
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from .forms import SnippetSaveForm, UserEditForm
from .models import CustomUser, Snippet
import django_filters
import re
from django.http import JsonResponse
from django.conf import settings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from django.contrib import messages
from django.core.exceptions import PermissionDenied, BadRequest
import logging

logger = logging.getLogger(__name__)


# FilterViews


class SnippetFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains", label="Title"
    )
    language = django_filters.ChoiceFilter(
        field_name="language",
        choices=[language for language in languages],
        lookup_expr="iexact",
        label="Programming Language",
    )

    class Meta:
        model = Snippet
        fields = ["title"]


@login_required
def snippet_filter_list(request):
    f = SnippetFilter(request.GET, queryset=Snippet.objects.all())
    return render(request, "snippet/snippet_filter_list.html", {"filter": f})


@login_required
def is_snippet_liked(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    liked = LikedSnippets.objects.filter(user=request.user).first()
    is_snippet_liked = False

    if liked:
        # LikedSnippet already exists, we just need to verify if the snippet is liked or not
        is_snippet_liked = liked.snippets_liked.filter(id=snippet_id).exists()
        return JsonResponse({"likes": snippet.num_like, "is_liked": is_snippet_liked})
    else:
        return JsonResponse({"likes": snippet.num_like, "is_liked": is_snippet_liked})


@login_required
def like_snippet(request, snippet_id):
    # First, get the snippet
    snippet = get_object_or_404(Snippet, id=snippet_id)
    # Then, verify if we already liked this snippet or not (verify if the snippet is present in the LikedSnippet)
    liked = LikedSnippets.objects.filter(user=request.user).first()
    is_snippet_liked = False

    if liked:
        # LikedSnippet already exists, we just need to verify if the snippet is liked or not
        is_snippet_liked = liked.snippets_liked.filter(id=snippet_id).exists()

        if is_snippet_liked:
            snippet.num_like -= 1
            is_snippet_liked = False
            liked.snippets_liked.remove(snippet)
        else:
            snippet.num_like += 1
            is_snippet_liked = True
            liked.snippets_liked.add(snippet)

    else:
        liked = LikedSnippets.objects.create(user=request.user)
        snippet.num_like += 1
        is_snippet_liked = True
        liked.snippets_liked.add(snippet)

    snippet.save()
    liked.save()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"likes": snippet.num_like, "is_liked": is_snippet_liked})
    return redirect("home")


# Views


def home(request):
    snippets = Snippet.objects.all()
    return render(request, "snippet/home.html", {"snippets": snippets})


@login_required
def liked_snippet_list(request):
    liked = LikedSnippets.objects.filter(user=request.user).first()
    if liked:
        snippets = liked.snippets_liked.all()
        return render(
            request, "snippet/liked_snippet_list.html", {"snippets": snippets}
        )
    else:
        return redirect("home")


def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, "snippet/snippet_detail.html", {"snippet": snippet})


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect(reverse("snippet_filter_list"))
            else:
                return render(
                    request,
                    "registration/signup.html",
                    {"form": form, "error": "Authentication failed"},
                )
        else:
            return render(request, "registration/signup.html", {"form": form})
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def update_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserEditForm(instance=user)

    return render(request, "snippet/edit_profile.html", {"form": form})


# 4XX/5XX Handling


def custom_bad_request(request, exception):
    return render(request, "400.html", status=400)


def custom_permission_denied(request, exception):
    return render(request, "403.html", status=403)


def custom_page_not_found(request, exception):
    return render(request, "404.html", status=404)


def custom_internal_error(request, exception=None):
    logger.error("Internal Server Error: %s", exception, exc_info=True)
    return render(request, "500.html", {"error": exception}, status=500)


def test_403(request):
    raise PermissionDenied


def test_400(request):
    raise BadRequest


@login_required
def profile(request):
    return render(request, "snippet/profile.html")


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        else:
            return super().get(request, *args, **kwargs)


from .forms import SnippetGenerationForm


@login_required
def generate_snippet(request):
    form = SnippetGenerationForm()
    snippet = None
    snippet_content = ""

    if request.method == "POST":
        if "generate_snippet" in request.POST:
            form = SnippetGenerationForm(request.POST)
            if form.is_valid():
                language = form.cleaned_data["language"]
                problem_type = form.cleaned_data["problem_type"]
                explanation = form.cleaned_data["explanation"]

                api_key = settings.OPENAI_API_KEY
                model = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=api_key)

                TEMPLATE_PROMPT = """
                Answer the user query.

                You are a programming assistant. the only response you are able to give is code.
                \n{query}\n
                """
                query = f"Generate a {problem_type} snippet in {language} that {explanation}."

                prompt = PromptTemplate(
                    template=TEMPLATE_PROMPT,
                    input_variables=["query"],
                )
                chain = prompt | model

                try:
                    response = chain.invoke({"query": query})
                    snippetGenerated = response.content
                    code_block_pattern = re.compile(
                        r"^```(?:\w+)?\n(.*)\n```$", re.DOTALL
                    )

                    match = code_block_pattern.match(snippetGenerated)  # type: ignore

                    if match:
                        snippet_content = match.group(1).strip()

                    snippet = Snippet(
                        author=request.user, language=language, code=snippet_content
                    )

                    context = {
                        "snippet": snippet,
                        "form": form,
                        "snippet_form": SnippetSaveForm(
                            initial={"language": language, "code": snippet_content}
                        ),
                    }

                    return render(request, "snippet/generated_snippet.html", context)

                except Exception as e:
                    snippet = f"Error generating snippet: {str(e)}"
        else:
            snippet_form = SnippetSaveForm(request.POST)
            print(snippet_form.data)
            print("-------------------")
            print(snippet_form.errors)
            if snippet_form.is_valid():
                print("oui")
                snippet_instance = snippet_form.save(commit=True)
                snippet_instance.author = request.user
                snippet_instance.save()

                messages.success(request, "Snippet saved successfully!")

                return redirect("snippet_filter_list")

    context = {"form": form, "snippet": snippet, "snippet_form": SnippetSaveForm()}
    return render(request, "snippet/generate_snippet.html", context)