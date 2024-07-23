from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from langchain_core.messages.base import BaseMessage
from snippet.admin import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, languages, Snippet
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from .forms import SnippetSaveForm, UserEditForm
from .models import CustomUser, Snippet
import django_filters
import re
from django.conf import settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from django.contrib import messages


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


# Views


def home(request):
    return render(request, "snippet/home.html")


@login_required
def snippet_list(request):
    snippets = Snippet.objects.filter(author=request.user)
    return render(request, "snippet/snippet_list.html", {"snippets": snippets})


# @login_required
def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, "snippet/snippet_detail.html", {"snippet": snippet})


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))  # Redirect to your home URL name

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("snippet_list")
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


# Custom 404 Handling


def custom_404(request, exception):
    return render(request, "404.html", status=404)


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

                    match = code_block_pattern.match(snippetGenerated) # type: ignore

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
