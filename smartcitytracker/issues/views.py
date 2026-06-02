from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, IssueForm
from .models import Issue, Notification

def home(request):
    issues = Issue.objects.all().order_by("-created_at")

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    status = request.GET.get("status", "")
    severity = request.GET.get("severity", "")

    if q:
        issues = issues.filter(title__icontains=q) | issues.filter(address__icontains=q)
    if category:
        issues = issues.filter(category=category)
    if status:
        issues = issues.filter(status=status)
    if severity:
        issues = issues.filter(severity=severity)

    context = {
        "issues": issues.distinct(),
        "categories": Issue.CATEGORY,
        "statuses": Issue.STATUS,
        "severities": Issue.SEVERITY,
    }
    stats = {
        "total": Issue.objects.count(),
        "resolved": Issue.objects.filter(status="resolved").count(),
        "in_progress": Issue.objects.filter(status="in_progress").count(),
        "reported": Issue.objects.filter(status="reported").count(),
    }
    context["stats"] = stats  # add to your existing context dict
    return render(request, "home.html", context)




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    issues = Issue.objects.filter(user=request.user).order_by('-created_at')
    notes = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'dashboard.html',
                  {'issues': issues, 'notes': notes})

@login_required
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            Notification.objects.create(
                user=request.user,
                message=f"Your issue '{issue.title}' was reported successfully.")
            messages.success(request, "Issue reported!")
            return redirect('dashboard')
    else:
        form = IssueForm()
    return render(request, 'report.html', {'form': form})

@login_required
def map_view(request):
    issues = Issue.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    return render(request, "map.html", {"issues": issues})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def upvote_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.user in issue.upvotes.all():
        issue.upvotes.remove(request.user)   # toggle off
    else:
        issue.upvotes.add(request.user)       # toggle on
    return redirect(request.META.get("HTTP_REFERER", "home"))
